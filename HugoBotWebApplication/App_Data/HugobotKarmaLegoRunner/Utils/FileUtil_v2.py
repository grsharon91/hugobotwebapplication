from sklearn.model_selection import KFold
from KarmaLego_Framework.RunKarmaLego import *
from TIRPsDetection_Framework.TIRPsDetection import *
from KarmaLego_Framework.TIRPsFeatureExraction import *
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
import csv
import time
from Utils.Model import ClassificationModel
import operator

from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt
from yellowbrick.features.importances import FeatureImportances
import pickle
from Shared_paths import paths
import datetime


def max_tirp_size_calc(frequent_tirps):
    """
    calculate the max tirp size from all the frequent TIRP bag
    :param frequent_tirps:
    :return:
    """
    max_size = 2
    for tirp in frequent_tirps:
        tirp_length = len(tirp._symbols)
        if tirp_length > max_size:
            max_size = tirp_length
    return max_size

def get_file_indexes(lines):
    """
    return the number of lines as indexes from the first entity row
    each line in indexes is one entity and has two indexes,
    one for the the entity id and second for its time intervals.
    Moreover it returns the start lines from the original file before the first entity row
    :param lines: list of lines in the original file
    :return: start_lines - list of the start lines
             indexes -array of indexes to split
    """
    starts = [n for n, l in enumerate(lines) if l.startswith('numberOfEntities')]
    if len(starts)==0:
        start_index=0
    else:
        start_index=starts[0]
    start_lines=lines[0:start_index+1]
    indexes=np.array([[i,i+1] for i in range (start_index+1,len(lines),2)])
    return start_lines,indexes

def get_folds_files(indexes,train_indices,test_indices,start_lines,lines, iteration,prefix_matrix,num_class):
    """
    this method creates new files for discovery and detection of tirps (train and test) by the given indices
     for each file, the method returns the new files with suffix of train/test and number of iteration
    :param indexes: array of lines indexes from the original  file
    :param train_indices: the train indices indexes
    :param test_indices: the test indices indexes
    :param start_lines: list of strings - the start lines in the original file
    :param lines: the readed lines from the original file
    :param iteration: int, number of iteration
    :param file_path: string, the original file path
    :return: train_file - the path of the train data,test_file - the path for the test data
    """
    train_file=prefix_matrix+"class_"+num_class+"_train_rows_iteration_"+str(iteration)+".csv"
    test_file = prefix_matrix +"class_"+num_class+"_test_rows_iteration_"+ str(iteration)+".csv"

    train_indexes = [list(indexes[i]) for i in train_indices]
    test_indexes = [list(indexes[i]) for i in test_indices]

    train_indexes_flat = [item for sublist in train_indexes for item in sublist]
    test_indexes_flat = [item for sublist in test_indexes for item in sublist]

    train_lines=start_lines+[lines[i] for i in train_indexes_flat]
    test_lines = start_lines + [lines[i] for i in test_indexes_flat]

    with open(train_file, 'w') as f:
        f.writelines(train_lines)
    with open(test_file, 'w') as f:
        f.writelines(test_lines)
    return train_file,test_file

def drop_recurrences_of_tirps(list_with_recurences,num_of_relations):
    tirp_dictionary = {}
    tirps_list = []
    for tirp in (list_with_recurences):
        tirp_dictionary[tirp.get_tirp_name(num_of_relations)] = tirp
    for tirp_name,tirp in tirp_dictionary.items():
        tirps_list.append(tirp)
    return  tirps_list


def drop_not_uniqe_tirps(tirps_class_0 , tirps_class_1,num_of_relations):
    tirp_dictionary_class_0={}
    tirp_dictionary_class_1={}
    tirps_list = []
    tirps_class_0_new=[]
    tirps_class_1_new=[]
    for tirp in (tirps_class_0):
        tirp_dictionary_class_0[tirp.get_tirp_name(num_of_relations)] = tirp
    for tirp in (tirps_class_1):
        tirp_dictionary_class_1[tirp.get_tirp_name(num_of_relations)] = tirp
    for tirp_name,tirp in tirp_dictionary_class_0.items():
        if tirp_name not in tirp_dictionary_class_1:
            tirps_list.append(tirp)
            tirps_class_0_new.append(tirp)
    for tirp_name,tirp in tirp_dictionary_class_1.items():
        if tirp_name not in tirp_dictionary_class_0:
            tirps_list.append(tirp)
            tirps_class_1_new.append(tirp)
    return  tirps_list,tirps_class_0_new,tirps_class_1_new

def mark_not_uniqe_tirps(tirps_class_0 , tirps_class_1,num_of_relations):
    tirp_dictionary_class_0={}
    tirp_dictionary_class_1={}
    tirps_list = []
    tirps_class_0_new=[]
    tirps_class_1_new=[]
    for tirp in (tirps_class_0):
        tirp_dictionary_class_0[tirp.get_tirp_name(num_of_relations)] = tirp
    for tirp in (tirps_class_1):
        tirp_dictionary_class_1[tirp.get_tirp_name(num_of_relations)] = tirp
    for tirp_name,tirp in tirp_dictionary_class_0.items():
        if tirp_name in tirp_dictionary_class_1:
            tirp._both_class='yes'
            tirps_list.append(tirp)
            tirps_class_0_new.append(tirp)
        else:
            tirp._both_class = 'no_0'
            tirps_list.append(tirp)
            tirps_class_0_new.append(tirp)
    for tirp_name,tirp in tirp_dictionary_class_1.items():
        if tirp_name  in tirp_dictionary_class_0:
            tirp._both_class = 'yes'
            tirps_list.append(tirp)
            tirps_class_1_new.append(tirp)
        else:
            tirp._both_class = 'no_1'
            tirps_list.append(tirp)
            tirps_class_1_new.append(tirp)

    return  tirps_list,tirps_class_0_new,tirps_class_1_new

def demi_tirps(list_tirp):
    demi_tirps=[]
    for tirp in list_tirp:
        demi_tirps.append(tirp.hollow_copy())
    return demi_tirps

def drop_tirps_length_two(tirps, num_of_entitites_train):
    long_tirps=[]
    for tirp in tirps:
        if len(tirp._symbols )>2: #or (len(tirp._symbols)==2 and tirp.get_vertical_support()/num_of_entitites_train>=drop_tirps_length_two_support):
            long_tirps.append(tirp)
    return long_tirps

def CV_example(file_path_class_0,file_path_class_1,prefix_matrix,discretization,prefix_matrix2,k,max_gap,representations,min_ver_support,num_of_relations,num_comma,symbol_type,skip_followers):
    """
    This method runs a k-fold cross-validation experiment, at each fold frequent TIRPs are found using KarmaLego framework
    for each class (class0, class1). Then, a feature matrix is generated from the train set and the classifier is fit to
     it. afterwards, a feature matrix is generated from the test for the classifier.
    :param file_path_class_0:  string, the path to the symbolic time intervals of calss 0
    :param file_path_class_1:  string, the path to the symbolic time intervals of calss 0
    :param prefix_matrix: string, part of the path to the train/test matrix
    :param k: number of folds
    :return: None
    """
    with open(file_path_class_0) as f:
        lines_class_0 = f.readlines()
        start_lines_0,indexes_class_0=get_file_indexes(lines_class_0)
    with open(file_path_class_1) as f:
        lines_class_1 = f.readlines()
        start_lines_1,indexes_class_1=get_file_indexes(lines_class_1)
    kf = KFold(n_splits=k)
    class_0_folds=list(kf.split(indexes_class_0))
    class_1_folds = list(kf.split(indexes_class_1))
    tirp_detection_obj = TIRPsDetection(num_of_relations,symbol_type)
    tirp_feature_ext_obj=TIRPsFeatureExtraction()
    sparse_matrix_list=[]
    detection_time=[]
    total_scores={}
    max_tirp_size_list = []
    num_frequent_tirp_list = []



    for i in range(k):
        train_file_class_0,test_file_class_0=get_folds_files(indexes=indexes_class_0,
                                                             train_indices=class_0_folds[i][0],
                                                             test_indices=class_0_folds[i][1],
                                                             start_lines=start_lines_0,
                                                             lines=lines_class_0,iteration=i, prefix_matrix=prefix_matrix,num_class='0')
        train_file_class_1, test_file_class_1 = get_folds_files(indexes=indexes_class_1,
                                                                train_indices=class_1_folds[i][0],
                                                                test_indices=class_1_folds[i][1],
                                                                start_lines=start_lines_1, lines=lines_class_1,
                                                                iteration=i, prefix_matrix=prefix_matrix,num_class='1')

        """runing the TIRPS DISCOVERY and detection"""
        print("runing the TIRPS DISCOVERY and detection")
        lego_0, karma_0=runKarmaLego(time_intervals_path=train_file_class_0,min_ver_support=min_ver_support,num_relations=num_of_relations, \
                                     skip_followers=skip_followers,max_gap=max_gap,label=0,max_tirp_length=5,num_comma=num_comma)
        entities_map_train_0 = karma_0._entities_map
        all_tirps_class_0 = lego_0.frequent_tirps

        lego_1, karma_1 = runKarmaLego(time_intervals_path=train_file_class_1, min_ver_support=min_ver_support, num_relations=num_of_relations, \
                                       skip_followers=skip_followers, max_gap=max_gap, label=1,max_tirp_length=5,num_comma=num_comma)
        entities_map_train_1 = karma_1._entities_map
        all_tirps_class_1 = lego_1.frequent_tirps

        del train_file_class_0
        del train_file_class_1

        num_of_entitites_train_o = len(entities_map_train_0)
        num_of_entitites_train_1 = len(entities_map_train_1)

        if drop_tirps_length_two_BOOL == True:
            all_tirps_class_0 = drop_tirps_length_two(all_tirps_class_0, num_of_entitites_train_o)
            all_tirps_class_1 = drop_tirps_length_two(all_tirps_class_1, num_of_entitites_train_1)


        if mark_not_uniqe_tirps_boolean==True:
            print("ff")
            tirps_list, all_tirps_class_0, all_tirps_class_1=mark_not_uniqe_tirps(all_tirps_class_0 , all_tirps_class_1,num_of_relations)

        demi_tirps_class_0 = demi_tirps(all_tirps_class_0)
        demi_tirps_class_1 = demi_tirps(all_tirps_class_1)

        if drop_not_uniqe_tirps_b == False:
            frequent_tirps = drop_recurrences_of_tirps(demi_tirps_class_0 + demi_tirps_class_1, num_of_relations)
        else:
            frequent_tirps,demi_tirps_class_0_unique,demi_tirps_class_1_unique = drop_not_uniqe_tirps(demi_tirps_class_0 , demi_tirps_class_1, num_of_relations)

        del all_tirps_class_0, all_tirps_class_1, lego_0,karma_0,lego_1,karma_1

        max_tirp_size = 0
        if max_tirp_size_nedded == True:
            max_tirp_size = max_tirp_size_calc(frequent_tirps)

        print("max_tirp_size {}".format(max_tirp_size))
        print("frequent_tirps size {}".format(len(frequent_tirps)))
        max_tirp_size_list.append(max_tirp_size)
        num_frequent_tirp_list.append(len(frequent_tirps))

        # checking the run time of the detection phase
        start_time = time.time()

        detected_tirps_class_0_in_train=tirp_detection_obj.Sequential_TIRPs_Detection_multiply_entities(frequent_tirps=frequent_tirps,
                                                                                               max_gap=max_gap, entities_map=entities_map_train_0,
                                                                                               epsilon=0,num_comma=num_comma)
        entities_class_0_train = list(tirp_detection_obj._entities_map_to_detect.keys())


        detected_tirps_class_1_in_train = tirp_detection_obj.Sequential_TIRPs_Detection_multiply_entities(frequent_tirps=frequent_tirps,
                                                                                                 max_gap=max_gap,  entities_map=entities_map_train_1,
                                                                                                epsilon=0,num_comma=num_comma)
        entities_class_1_train = list(tirp_detection_obj._entities_map_to_detect.keys())


        detected_tirps_class_0_in_test=tirp_detection_obj.Sequential_TIRPs_Detection_multiply_entities(frequent_tirps=frequent_tirps,
                                                                                               time_intervals_entities_path=test_file_class_0,
                                                                                               max_gap=max_gap,
                                                                                               epsilon=0,num_comma=num_comma)
        entities_class_0_test = list(tirp_detection_obj._entities_map_to_detect.keys())

        detected_tirps_class_1_in_test = tirp_detection_obj.Sequential_TIRPs_Detection_multiply_entities(frequent_tirps=frequent_tirps,
                                                                                                time_intervals_entities_path=test_file_class_1,
                                                                                                 max_gap=max_gap,
                                                                                                epsilon=0,num_comma=num_comma)
        entities_class_1_test = list(tirp_detection_obj._entities_map_to_detect.keys())

        seconds = (time.time() - start_time)
        detection_time.append(seconds)

        # drop_recurrences_of_tirps
        tirps_0_train = drop_recurrences_of_tirps(
            frequent_tirps + detected_tirps_class_0_in_train, num_of_relations)
        tirps_1_train = drop_recurrences_of_tirps(
            frequent_tirps+ detected_tirps_class_1_in_train, num_of_relations)
        tirps_0_test = drop_recurrences_of_tirps(
            frequent_tirps+ detected_tirps_class_0_in_test, num_of_relations)
        tirps_1_test = drop_recurrences_of_tirps(
            frequent_tirps+ detected_tirps_class_1_in_test, num_of_relations)

        del demi_tirps_class_0, demi_tirps_class_1,detected_tirps_class_0_in_train,detected_tirps_class_1_in_train,detected_tirps_class_0_in_test,detected_tirps_class_1_in_test

        for representation in representations:
            if representation not in total_scores:
                Scores = {
                    'logreg': {'AUC': [], 'accuracy': [], 'precision': [], 'recall': []},
                    'svm': {'AUC': [], 'accuracy': [], 'precision': [], 'recall': []},
                    'rf': {'AUC': [], 'accuracy': [], 'precision': [], 'recall': []}
                }
                total_scores[representation] = Scores
            matrix_class_0_train = tirp_feature_ext_obj.getMatrixForModeling(
                tirps=tirps_0_train,
                entities_list=entities_class_0_train,
                representation=representation, num_of_relations=num_of_relations, label=0)

            matrix_class_1_train = tirp_feature_ext_obj.getMatrixForModeling(
                tirps=tirps_1_train,
                entities_list=entities_class_1_train,
                representation=representation, num_of_relations=num_of_relations, label=1)

            matrix_class_0_train.to_csv(prefix_matrix + 'matrix_train_class_0_fold_' + '_' + str(i) + '.csv')
            matrix_class_1_train.to_csv(prefix_matrix + 'matrix_train_class_1_fold_' + '_' + str(i) + '.csv')

            tirps_matrix_for_train = tirp_feature_ext_obj.concat_matrix_classes(
                [matrix_class_0_train, matrix_class_1_train])
            tirps_matrix_for_train.to_csv(prefix_matrix + 'train_matrix_' + str(i) + '.csv')

            matrix_class_0_test = tirp_feature_ext_obj.getMatrixForModeling(
                tirps=tirps_0_test,
                entities_list=entities_class_0_test,
                representation=representation, num_of_relations=num_of_relations, label=0)

            matrix_class_1_test=tirp_feature_ext_obj.getMatrixForModeling(tirps=tirps_1_test,
                                                      entities_list=entities_class_1_test,
                                                      representation=representation,num_of_relations=num_of_relations,label=1)
            tirps_matrix_for_test=tirp_feature_ext_obj.concat_matrix_classes([matrix_class_0_test,matrix_class_1_test])
            tirps_matrix_for_test.to_csv(prefix_matrix +'test_matrix_' + str(i) + '.csv')

            # check sparsity
            non_zero_value = (tirps_matrix_for_test != 0.0).values.sum()
            zero_value = (tirps_matrix_for_test == 0.0).values.sum()
            sparse_matrix = zero_value / (non_zero_value + zero_value)

            sparse_matrix_list.append(sparse_matrix)
            # pre-processing  for classifier
            X_train = tirps_matrix_for_train.iloc[:, :-1]
            y_train= tirps_matrix_for_train.iloc[:, -1]
            X_test = tirps_matrix_for_test.iloc[:, :-1]
            y_test= tirps_matrix_for_test.iloc[:, -1]

            for classifier in classifiers:

                params = None
                if classifier == 'rf':
                    params = {"n_estimators": 50,
                              "max_depth": 5,
                              "bootstrap": True,
                              "criterion": "entropy",
                              "oob_score": True,
                              "n_jobs": -1,
                              'random_state': 2}

                elif classifier == 'gb':
                    params = {'n_estimators': 50, 'max_leaf_nodes': 4, 'max_depth': None, 'random_state': 2,
                              'min_samples_split': 5}

                model_obj = ClassificationModel(classifier, params)
                model_obj.fit(X_train, y_train)
                y_pred = model_obj.predict_proba(X_test)
                y_pred_binary = model_obj.predict(X_test)

                tirps_matrix_for_test["y_pred"]=y_pred
                tirps_matrix_for_test["y_pred_binary"] = y_pred_binary

                tirps_matrix_for_test.to_csv(prefix_matrix + 'test_matrix_' + str(i) + '.csv')

                #  classifier accuracy
                fpr, tpr, thresholds = metrics.roc_curve(y_true=y_test, y_score=y_pred)
                auc = np.trapz(tpr, fpr)
                print(auc)

                total_scores[representation][classifier]['AUC'].append(auc)
                total_scores[representation][classifier]['accuracy'].append(
                    accuracy_score(y_test, y_pred_binary))
                total_scores[representation][classifier]['precision'].append(
                    precision_score(y_test, y_pred_binary))
                total_scores[representation][classifier]['recall'].append(
                    recall_score(y_test, y_pred_binary))
                #Create a new matplotlib figure
                # fig = plt.figure()
                # ax = fig.add_subplot()
                #
                # viz = FeatureImportances(GradientBoostingClassifier(), ax=ax)
                # viz.fit(X_test, y_test)
                # viz.poof()
        print('Fold: {}'.format( i))

    for representation in representations:
        for classifier in classifiers:
            # The mean AUC and the 95% confidence interval
            print("representation: %s, Classifier: %s ,AUC: %0.2f (+/- %0.2f)" % (representation,classifier,np.mean(total_scores[representation][classifier]['AUC']), np.std(total_scores[representation][classifier]['AUC']) * 2))
            # The mean accuracy and the 95% confidence interval
            print("representation: %s, Classifier %s Accuracy: %0.2f (+/- %0.2f)" % (representation,classifier,np.mean(total_scores[representation][classifier]['accuracy']), np.std(total_scores[representation][classifier]['accuracy']) * 2))
            # The mean Precision and the 95% confidence interval
            print("representation: %s, Classifier %s Precision: %0.2f (+/- %0.2f)" % (representation,classifier,np.mean(total_scores[representation][classifier]['precision']), np.std(total_scores[representation][classifier]['precision']) * 2))
            # The mean recall and the 95% confidence interval
            print("representation: %s, Classifier %s Recall: %0.2f (+/- %0.2f)" % (representation,classifier,np.mean(total_scores[representation][classifier]['recall']), np.std(total_scores[representation][classifier]['recall']) * 2))


            log_list_test = [classifier,2,discretization,k, representation, min_ver_support, max_gap,num_of_relations,'not relevent',1,"Regular",np.mean(sparse_matrix_list),
                             np.mean(total_scores[representation][classifier]['AUC']),np.mean(detection_time),
                             np.mean(total_scores[representation][classifier]['accuracy']),np.mean(total_scores[representation][classifier]['precision']),
                             np.mean(total_scores[representation][classifier]['recall']),drop_tirps_length_two_support,\
                             drop_tirps_length_two_BOOL,drop_not_uniqe_tirps_b,observation_delay,np.mean(max_tirp_size_list)
                                ,np.mean(num_frequent_tirp_list),'not relevent',0.5,np.std(total_scores[representation][classifier]['AUC'])
                                 , datetime.datetime.now()]
            writer = csv.writer(open(prefix_matrix2 + "_results.csv", "a"), lineterminator='\n', dialect='excel')
            writer.writerow(log_list_test)


##----------------------------------------------------------------------------Main--------------------------------------------------------------------------------------------------
# Parameters
max_gap=[20]
min_ver_support=[0.4]
classifiers = ['logreg','rf']
drop_tirps_length_two_BOOL = False
drop_tirps_length_two_support=0.5
representations= ['MD','BIN','HS']
K=10
num_comma=3
num_of_relations_list=[7]
max_tirp_size_nedded=True
drop_not_uniqe_tirps_b=False
mark_not_uniqe_tirps_boolean=False
observation_delay='deb'
skip_followers=True


data_sets_path=[paths['deb']['folder_path']]
EWD_class0_data_path=[paths['deb']['class0']['EWD']]
EWD_class1_data_path=[paths['deb']['class1']['EWD']]
SAX_class0_data_path=[paths['deb']['class0']['SAX']]
SAX_class1_data_path=[paths['deb']['class1']['SAX']]
TD4Ccosin_class0_data_path=[paths['deb']['class0']['TD4C']]
TD4Ccosin_class1_data_path=[paths['deb']['class1']['TD4C']]
data_result_path=[paths['deb']['results']]


for i,data_set_results_path in enumerate(data_sets_path):
    log_list_header = ['classifier', 'num_of_bins',  'discretization','k', 'representation', 'min_ver_support'
        ,'max_gap','num_of_relations', 'simple_artemis','similarity_limit', 'detection_type', 'Sparsity', 'AUC',
                       'seconds','Accuracy','Precision','Recall','drop_tirps_length_two_support','drop_tirps_length_two_BOOL',\
                       'drop_not_uniqe_tirps_b','observation_delay','max_tirp_size','num_frequent_tirp','threshold','std','date']
    writer = csv.writer(open(data_set_results_path + "_results.csv", "a"), lineterminator='\n', dialect='excel')
    writer.writerow(log_list_header)

    CV_example(file_path_class_0=EWD_class0_data_path[i],file_path_class_1=EWD_class1_data_path[i],
               prefix_matrix=data_result_path[i], discretization='EWD', prefix_matrix2=data_set_results_path, k=K, max_gap=max_gap[i], \
     representations=representations, min_ver_support=min_ver_support[i],num_of_relations=num_of_relations_list[i], num_comma=num_comma,symbol_type='int',skip_followers=skip_followers)

    CV_example(file_path_class_0=SAX_class0_data_path[i],file_path_class_1= SAX_class1_data_path[i],
              prefix_matrix=data_result_path[i], discretization='SAX',   prefix_matrix2=data_set_results_path, k=K, \
               max_gap=max_gap[i], representations=representations, min_ver_support=min_ver_support[i],num_of_relations=num_of_relations_list[i], num_comma=num_comma,symbol_type='int',skip_followers=skip_followers)

    CV_example(file_path_class_0=TD4Ccosin_class0_data_path[i],  file_path_class_1=TD4Ccosin_class1_data_path[i],
                prefix_matrix=data_result_path[i], discretization='TD4Ccosin', prefix_matrix2=data_set_results_path, k=K,\
                max_gap=max_gap[i], representations=representations, min_ver_support=min_ver_support[i], num_of_relations=num_of_relations_list[i],num_comma=num_comma,symbol_type='int',skip_followers=skip_followers)






