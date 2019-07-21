from sklearn.model_selection import KFold
from KarmaLego_Framework.RunKarmaLego import *
from sklearn.metrics import roc_curve, auc
from TIRPsDetection_Framework.TIRPsDetection import *
from KarmaLego_Framework.TIRPsFeatureExraction import *
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import label_binarize
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.multiclass import OneVsRestClassifier
import time
from os import listdir
from os.path import isfile, join


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

def get_folds_files(indexes,train_indices,test_indices,start_lines,lines, iteration,file_path):
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
    prefix=file_path.replace(".csv","")
    train_file=prefix+"_train_"+str(iteration)+".csv"
    test_file = prefix +"_test_"+ str(iteration)+".csv"

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
        tirps_list.append(tirp)########################
    return  tirps_list

def demi_tirps(list_tirp):
    '''
    The function creates copies all the specified list of tirps
    :param list_tirp: list of TIRP objects
    :return: list - the copied list of tirps specified
    '''
    demi_tirps=[]
    for tirp in list_tirp:
        demi_tirps.append(tirp.hollow_copy())
    return demi_tirps

def CV_example(file_path_class_0,file_path_class_1,prefix_matrix,k=3,num_of_relations=7,max_gap=1,representation='HS',min_ver_support=0.6,num_comma=3):
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
    tirp_detection_obj = TIRPsDetection()
    tirp_feature_ext_obj=TIRPsFeatureExtraction()
    #AUC
    LogisticRegression_AUC_list=[]
    SVM_AUC_list=[]
    RandomForest_AUC_list=[]
    #Accuracy
    LogisticRegression_accuracy = []
    SVM_accuracy = []
    RandomForest_accuracy = []
    #Precision
    LogisticRegression_precision = []
    SVM_precision = []
    RandomForest_precision = []
    #Recall
    LogisticRegression_recall = []
    SVM_recall = []
    RandomForest_recall = []
    for i in range(k):
        train_file_class_0,test_file_class_0=get_folds_files(indexes=indexes_class_0,
                                                             train_indices=class_0_folds[i][0],
                                                             test_indices=class_0_folds[i][1],
                                                             start_lines=start_lines_0,
                                                             lines=lines_class_0,iteration=i,file_path=file_path_class_0)
        train_file_class_1, test_file_class_1 = get_folds_files(indexes=indexes_class_1,
                                                                train_indices=class_1_folds[i][0],
                                                                test_indices=class_1_folds[i][1],
                                                                start_lines=start_lines_1, lines=lines_class_1,
                                                                iteration=i, file_path=file_path_class_1)
        lego_0, karma_o=runKarmaLego(time_intervals_path=train_file_class_0,min_ver_support=0.5,num_relations=7,max_gap=15,label=0,num_comma=3)
        tirps_class_0=lego_0.frequent_tirps
        lego_1, karma_1 = runKarmaLego(time_intervals_path=train_file_class_1, min_ver_support=0.5, num_relations=7,max_gap=15,label=0,num_comma=3)
        tirps_class_1 = lego_1.frequent_tirps
        demi_tirps_class_0 = demi_tirps(tirps_class_0)
        demi_tirps_class_1 = demi_tirps(tirps_class_1)
        #tirps matrix for train
        detected_tirps_class_0_in_train=tirp_detection_obj.Sequential_TIRPs_Detection_multiply_entities(frequent_tirps=drop_recurrences_of_tirps(tirps_class_0+tirps_class_1,num_of_relations),#############
                                                                                               time_intervals_entities_path=train_file_class_0,
                                                                                               max_gap=max_gap,
                                                                                               epsilon=0,num_comma=3)
        matrix_class_0_train=tirp_feature_ext_obj.getMatrixForModeling(tirps=drop_recurrences_of_tirps(demi_tirps_class_0+demi_tirps_class_1+detected_tirps_class_0_in_train,num_of_relations),
                                                  entities_list=list(tirp_detection_obj._entities_map_to_detect.keys()),
                                                  representation=representation,num_of_relations=7,label=0)

        detected_tirps_class_1_in_train = tirp_detection_obj.Sequential_TIRPs_Detection_multiply_entities(frequent_tirps=drop_recurrences_of_tirps(tirps_class_0+tirps_class_1,num_of_relations),
                                                                                                time_intervals_entities_path=train_file_class_1,
                                                                                                 max_gap=max_gap,
                                                                                                epsilon=0,num_comma=3)
        matrix_class_1_train=tirp_feature_ext_obj.getMatrixForModeling(tirps=drop_recurrences_of_tirps(demi_tirps_class_0+demi_tirps_class_1+detected_tirps_class_1_in_train,num_of_relations),
                                                  entities_list=list(tirp_detection_obj._entities_map_to_detect.keys()),
                                                  representation=representation,num_of_relations=7, label=1)

        tirps_matrix_for_train=tirp_feature_ext_obj.concat_matrix_classes([matrix_class_0_train,matrix_class_1_train])
        tirps_matrix_for_train.to_csv(prefix_matrix +'_' +'train'+'_' + str(i) + '.csv')
        #tirps matrix for test
        detected_tirps_class_0_in_test=tirp_detection_obj.Sequential_TIRPs_Detection_multiply_entities(frequent_tirps=drop_recurrences_of_tirps(tirps_class_0+tirps_class_1,num_of_relations),
                                                                                               time_intervals_entities_path=test_file_class_0,
                                                                                               max_gap=max_gap,
                                                                                               epsilon=0,num_comma=3)
        matrix_class_0_test=tirp_feature_ext_obj.getMatrixForModeling(tirps=drop_recurrences_of_tirps(demi_tirps_class_0+demi_tirps_class_1+detected_tirps_class_0_in_test,num_of_relations),
                                                  entities_list=list(tirp_detection_obj._entities_map_to_detect.keys()),
                                                  representation=representation,num_of_relations=7,label=0)
        detected_tirps_class_1_in_test = tirp_detection_obj.Sequential_TIRPs_Detection_multiply_entities(frequent_tirps=drop_recurrences_of_tirps(tirps_class_0+tirps_class_1,num_of_relations),
                                                                                                time_intervals_entities_path=test_file_class_1,
                                                                                                 max_gap=max_gap,
                                                                                                epsilon=0,num_comma=3)
        matrix_class_1_test=tirp_feature_ext_obj.getMatrixForModeling(tirps=drop_recurrences_of_tirps(demi_tirps_class_0+demi_tirps_class_1+detected_tirps_class_1_in_test,num_of_relations),
                                                  entities_list=list(tirp_detection_obj._entities_map_to_detect.keys()),
                                                  representation=representation,num_of_relations=7,label=1)
        tirps_matrix_for_test=tirp_feature_ext_obj.concat_matrix_classes([matrix_class_0_test,matrix_class_1_test])
        tirps_matrix_for_test.to_csv(prefix_matrix +'_' +'test'+ '_' + str(i) + '.csv')

        with open(prefix_matrix +'_' +'test'+ '_' + str(i) + '.csv') as f:
            h = f.readline()
            columns = h.count(',') + 1
            f.close()

        if columns>2:
            # pre-processing  for classifier
            X_train = tirps_matrix_for_train.iloc[:, :-1]
            y_train= tirps_matrix_for_train.iloc[:, -1]
            X_test = tirps_matrix_for_test.iloc[:, :-1]
            y_test= tirps_matrix_for_test.iloc[:, -1]

            #LogisticRegression
            model_obj = LogisticRegression()
            model_obj.fit(X_train, y_train)
            y_pred = model_obj.predict_proba(X_test)[:,1]
            y_pred_binary = model_obj.predict(X_test)
            #  classifier accuracy
            fpr, tpr, thresholds = metrics.roc_curve(y_true=y_test, y_score=y_pred)
            auc = np.trapz(tpr, fpr)
            LogisticRegression_AUC_list.append(auc)
            LogisticRegression_accuracy.append(accuracy_score(y_test, y_pred_binary))
            LogisticRegression_precision.append(precision_score(y_test, y_pred_binary))
            LogisticRegression_recall.append(recall_score(y_test, y_pred_binary))
            print('LogisticRegression_AUC_list, Fold: {}, AUC: {}'.format(i,auc))

            # SVM
            model_obj = svm.SVC(probability=True)
            model_obj.fit(X_train, y_train)
            y_pred = model_obj.predict_proba(X_test)[:,1]
            y_pred_binary = model_obj.predict(X_test)
            #  classifier accuracy
            fpr, tpr, thresholds = metrics.roc_curve(y_true=y_test, y_score=y_pred)
            auc = np.trapz(tpr, fpr)
            SVM_AUC_list.append(auc)
            SVM_accuracy.append(accuracy_score(y_test, y_pred_binary))
            SVM_precision.append(precision_score(y_test, y_pred_binary))
            SVM_recall.append(recall_score(y_test, y_pred_binary))
            print('SVM_AUC_list, Fold: {}, AUC: {}'.format(i, auc))

            # RandomForest
            model_obj = RandomForestClassifier(random_state=100)
            model_obj.fit(X_train, y_train)
            y_pred = model_obj.predict_proba(X_test)[:, 1]
            y_pred_binary = model_obj.predict(X_test)
            #  classifier accuracy
            fpr, tpr, thresholds = metrics.roc_curve(y_true=y_test, y_score=y_pred)
            auc = np.trapz(tpr, fpr)
            RandomForest_AUC_list.append(auc)
            RandomForest_accuracy.append(accuracy_score(y_test, y_pred_binary))
            RandomForest_precision.append(precision_score(y_test, y_pred_binary))
            RandomForest_recall.append(recall_score(y_test, y_pred_binary))
            print('RandomForest_AUC_list, Fold: {}, AUC: {}'.format(i, auc))

    if columns > 2:
        # LogisticRegression- the mean AUC and the 95% confidence interval
        print("LogisticRegression AUC: %0.2f (+/- %0.2f)" % (np.mean(LogisticRegression_AUC_list), np.std(LogisticRegression_AUC_list) * 2))
        # SVM- the mean AUC and the 95% confidence interval
        print("SVM AUC: %0.2f (+/- %0.2f)" % (np.mean(SVM_AUC_list), np.std(SVM_AUC_list) * 2))
        # RandomForest- the mean AUC and the 95% confidence interval
        print("RandomForest AUC: %0.2f (+/- %0.2f)" % (np.mean(RandomForest_AUC_list), np.std(RandomForest_AUC_list) * 2))
        # The mean accuracy and the 95% confidence interval
        print("LogisticRegression Accuracy: %0.2f (+/- %0.2f)" % (np.mean(LogisticRegression_accuracy), np.std(LogisticRegression_accuracy) * 2))
        # The mean accuracy and the 95% confidence interval
        print("SVM Accuracy: %0.2f (+/- %0.2f)" % (np.mean(SVM_accuracy), np.std(SVM_accuracy) * 2))
        # The mean accuracy and the 95% confidence interval
        print("RandomForest Accuracy: %0.2f (+/- %0.2f)" % (np.mean(RandomForest_accuracy), np.std(RandomForest_accuracy) * 2))
        # The mean Precision and the 95% confidence interval
        print("LogisticRegression Precision: %0.2f (+/- %0.2f)" % (np.mean(LogisticRegression_precision), np.std(LogisticRegression_precision) * 2))
        # The mean Precision and the 95% confidence interval
        print("SVM Precision: %0.2f (+/- %0.2f)" % (np.mean(SVM_precision), np.std(SVM_precision) * 2))
        # The mean Precision and the 95% confidence interval
        print("RandomForest Precision: %0.2f (+/- %0.2f)" % (np.mean(RandomForest_precision), np.std(RandomForest_precision) * 2))
        # The mean recall and the 95% confidence interval
        print("LogisticRegression Recall: %0.2f (+/- %0.2f)" % (np.mean(LogisticRegression_recall), np.std(LogisticRegression_recall) * 2))
        # The mean recall and the 95% confidence interval
        print("SVM Recall: %0.2f (+/- %0.2f)" % (np.mean(SVM_recall), np.std(SVM_recall) * 2))
        # The mean recall and the 95% confidence interval
        print("RandomForest Recall: %0.2f (+/- %0.2f)" % (np.mean(RandomForest_recall), np.std(RandomForest_recall) * 2))


def run_classification(tirp_matrix_train,tirp_matrix_test,labels):
    '''
    Run random forest classifier based on tirp of trai nand test
    :param tirp_matrix_train: tirp matrix for training
    :param tirp_matrix_test: tirp matrix for testing
    :param labels: labels of the data
    :return: predcted test values and real test values - array like objects
    '''
    X_train = tirp_matrix_train.iloc[:, :-1]
    y_train = tirp_matrix_train.iloc[:, -1]
    X_test = tirp_matrix_test.iloc[:, :-1]
    y_test = tirp_matrix_test.iloc[:, -1]

    # binarize the data in order to compute metrices
    Y_All = y_train.append(y_test, ignore_index=True)
    train_size = y_train.size
    Y_All = label_binarize(Y_All, classes=labels)
    y_train_binarized = Y_All[0:train_size]
    y_test_binarized = Y_All[train_size:]

    model_obj = RandomForestClassifier(n_estimators=100, random_state=100)
    classifier = OneVsRestClassifier(model_obj)
    y_pred = classifier.fit(X_train, y_train_binarized).predict(X_test)
    return y_pred,y_test_binarized

def update_results(y_pred,y_test,auc_list,accuracy_list,precision_list,recall_list):
    auc_total = metrics.roc_auc_score(y_test, y_pred)
    auc_list.append(auc_total)
    accuracy_calc = accuracy_score(y_test, y_pred)
    accuracy_list.append(accuracy_calc)
    precision_calc = precision_score(y_test, y_pred, average='micro')
    precision_list.append(precision_calc)
    recall_calc = recall_score(y_test, y_pred, average='micro')
    recall_list.append(recall_calc)
    return auc_total,accuracy_calc,precision_calc,recall_calc

def print_final_kfold_results(auc_list,acc_list,precision_list,recall_list,kl_metric):
    '''
    Function prints final k-fold results of the entire k fold process
    :param auc_list: auc list size as number of folds
    :param acc_list: accuracy list size as number of folds
    :param precision_list: precision list size as number of folds
    :param recall_list: recall list size as number of folds
    :param kl_metric: metric used string: hs, binary or md
    :return:no return value
    '''
    # RandomForest- the mean AUC and the 95% confidence interval
    print("RandomForest AUC "+kl_metric+": %0.2f (+/- %0.2f)" % (
        np.mean(auc_list), np.std(auc_list) * 2))
    # The mean accuracy and the 95% confidence interval
    print("RandomForest Accuracy "+kl_metric+": %0.2f (+/- %0.2f)" % (
        np.mean(acc_list), np.std(acc_list) * 2))
    # The mean Precision and the 95% confidence interval
    print("RandomForest Precision "+kl_metric+": %0.2f (+/- %0.2f)" % (
        np.mean(precision_list), np.std(precision_list) * 2))
    # The mean recall and the 95% confidence interval
    print("RandomForest Recall "+kl_metric+": %0.2f (+/- %0.2f)\n" % (
        np.mean(recall_list), np.std(recall_list) * 2))

def get_all_kl_num_of_columns(file_path_hs,file_path_binary,file_path_md):
    '''
    The function gets all number of columns for 3 kl metrics.
    Afterwards the number of columns will be used to check if it is possible to preform classification process
    :param file_path_hs: string, path to hs matrix
    :param file_path_binary: string, path to binary matrix
    :param file_path_md: string, path to md matrix
    :return: 3 column counts columns_hs,columns_binary,columns_md
    '''
    with open(file_path_hs) as f_hs:
        h = f_hs.readline()
        columns_hs = h.count(',') + 1
        f_hs.close()

    with open(file_path_binary) as f_binary:
        h = f_binary.readline()
        columns_binary = h.count(',') + 1
        f_binary.close()

    with open(file_path_md) as f_md:
        h = f_md.readline()
        columns_md = h.count(',') + 1
        f_md.close()

    return columns_hs,columns_binary,columns_md



def CV_example_multi_label(file_paths, prefix_matrix, k=3, num_of_relations=7, max_gap=1, representation='HS',
                           min_ver_support=0.6, num_comma=3,num_bins=3,symbol='int'):
    '''
    This method runs a k-fold cross-validation experiment. This function is similiar to cv_example
    but it incorporates the karma lego process for multi label classification.
    :param file_paths: list, the paths to the symbolic time intervals of the classes
    :param prefix_matrix: string, part of the path to the train/test matrix
    :param k: int, number of folds to run
    :param num_of_relations: int, number of time interval related relations
    :param max_gap: int, maximal gap for karma lego algorithm
    :param representation: string, which pattern metric to use {HS, Binary, MD}
    :param min_ver_support: float, minimal vertical support for karma lego algorithm
    :return: No return value
    '''
    labels = [100, 200, 300, 400, 500, 600]
    tirp_detection_obj = TIRPsDetection()
    tirp_feature_ext_obj = TIRPsFeatureExtraction()
    num_of_classes = len(file_paths)
    kf = KFold(n_splits=k)

    start_lines_classes = []#a list containing the start lines for each class
    lines_class_classes = []#a list containing all of the rows of all classes
    indexes_classes = []#a list containing the indexes of each class
    class_folds = []# a list containing every fold option for each class
    train_file_classes = []#list of train file paths for current fold
    test_file_classes = []#list of test file paths for curent fold

    #all_matrices_train = []
    # addition for now
    all_matrices_train_hs = []
    all_matrices_train_binary = []
    all_matrices_train_md = []

    #all_matrices_test = []
    # addition for now
    all_matrices_test_hs = []
    all_matrices_test_binary = []
    all_matrices_test_md = []

    # RandomForest_AUC_list = []#auc value for each fold
    # RandomForest_accuracy = []#accuracy value for each fold
    # RandomForest_precision = []#precision value for each fold
    # RandomForest_recall = []#recall value for each fold

    RandomForest_AUC_list_hs = []
    RandomForest_AUC_list_binary = []
    RandomForest_AUC_list_md = []

    RandomForest_accuracy_list_hs = []
    RandomForest_accuracy_list_binary = []
    RandomForest_accuracy_list_md = []

    RandomForest_precision_list_hs = []
    RandomForest_precision_list_binary = []
    RandomForest_precision_list_md = []

    RandomForest_recall_list_hs = []
    RandomForest_recall_list_binary = []
    RandomForest_recall_list_md = []



    # data folding preperation
    for raw_file in file_paths:
        with open(raw_file) as f:
            lines_curr_class = f.readlines()
            start_lines_curr, indexes_class_curr = get_file_indexes(lines_curr_class)
            lines_class_classes.append(lines_curr_class)
            start_lines_classes.append(start_lines_curr)
            indexes_classes.append(indexes_class_curr)

    # create folds for each class
    for indexes in indexes_classes:
        curr_class_fold = list(kf.split(indexes))
        class_folds.append(curr_class_fold)

    start_time = time.time()

    # Main for loop: Run folds - each fold contains all m (user specified input) classes
    for i in range(k):
        print("Starting fold number %i"%(i))
        train_file_classes.clear()
        test_file_classes.clear()
        #all_matrices_train.clear()

        all_matrices_train_hs.clear()
        all_matrices_train_binary.clear()
        all_matrices_train_md.clear()

        #all_matrices_test.clear()

        all_matrices_test_hs.clear()
        all_matrices_test_binary.clear()
        all_matrices_test_md.clear()

        # This loop creates for each class file its train and test files
        for a in range(0, num_of_classes):
            train_file_class_curr, test_file_class_curr = get_folds_files(indexes=indexes_classes[a],
                                                                          train_indices=class_folds[a][i][0],
                                                                          test_indices=class_folds[a][i][1],
                                                                          start_lines=start_lines_classes[a],
                                                                          lines=lines_class_classes[a], iteration=i,
                                                                          file_path=file_paths[a])
            train_file_classes.append(train_file_class_curr)
            test_file_classes.append(test_file_class_curr)

        all_demi_tirps = []
        all_tirps_classes = []

        # This loop mines for each train file created for each class the frequent tirps using the KarmaLego algorithm
        for b in range(0, num_of_classes):
            lego_curr_class = runKarmaLego(time_intervals_path=train_file_classes[b],
                                           min_ver_support=min_ver_support, num_relations=num_of_relations, max_gap=max_gap, label=labels[b],num_of_bins=num_bins,
                                           num_comma=num_comma, symbol_type=symbol)
            tirps_curr_class = lego_curr_class.frequent_tirps
            all_tirps_classes += tirps_curr_class
            demi_tirps_curr_class = demi_tirps(tirps_curr_class)
            all_demi_tirps += demi_tirps_curr_class

        # train tirps
        for c in range(0, num_of_classes):
            detected_tirps_class_curr_in_train = tirp_detection_obj.Sequential_TIRPs_Detection_multiply_entities(
                frequent_tirps=drop_recurrences_of_tirps(all_tirps_classes, num_of_relations),  #############
                time_intervals_entities_path=train_file_classes[c],
                max_gap=max_gap,
                epsilon=0, num_comma=num_comma)

            # matrix_class_curr_train = tirp_feature_ext_obj.getMatrixForModeling(
            #     tirps=drop_recurrences_of_tirps(all_demi_tirps + detected_tirps_class_curr_in_train,
            #                                     num_of_relations),
            #     entities_list=list(tirp_detection_obj._entities_map_to_detect.keys()),
            #     representation=representation, num_of_relations=7, label=labels[c])

            matrix_class_curr_train_hs = tirp_feature_ext_obj.getMatrixForModeling(
                tirps=drop_recurrences_of_tirps(all_demi_tirps + detected_tirps_class_curr_in_train,
                                                num_of_relations),
                entities_list=list(tirp_detection_obj._entities_map_to_detect.keys()),
                representation='HS', num_of_relations=num_of_relations, label=labels[c])

            matrix_class_curr_train_binary = tirp_feature_ext_obj.getMatrixForModeling(
                tirps=drop_recurrences_of_tirps(all_demi_tirps + detected_tirps_class_curr_in_train,
                                                num_of_relations),
                entities_list=list(tirp_detection_obj._entities_map_to_detect.keys()),
                representation='BIN', num_of_relations=num_of_relations, label=labels[c])

            matrix_class_curr_train_md = tirp_feature_ext_obj.getMatrixForModeling(
                tirps=drop_recurrences_of_tirps(all_demi_tirps + detected_tirps_class_curr_in_train,
                                                num_of_relations),
                entities_list=list(tirp_detection_obj._entities_map_to_detect.keys()),
                representation='MD', num_of_relations=num_of_relations, label=labels[c])



            #all_matrices_train.append(matrix_class_curr_train)
            #addition for now
            all_matrices_train_hs.append(matrix_class_curr_train_hs)
            all_matrices_train_binary.append(matrix_class_curr_train_binary)
            all_matrices_train_md.append(matrix_class_curr_train_md)

        #tirps_matrix_for_train = tirp_feature_ext_obj.concat_matrix_classes(all_matrices_train)

        tirps_matrix_for_train_hs = tirp_feature_ext_obj.concat_matrix_classes(all_matrices_train_hs)
        tirps_matrix_for_train_binary = tirp_feature_ext_obj.concat_matrix_classes(all_matrices_train_binary)
        tirps_matrix_for_train_md = tirp_feature_ext_obj.concat_matrix_classes(all_matrices_train_md)

        #f_name_train_matrix = prefix_matrix + '_' + 'train' + '_' + str(i) + '.csv'

        f_name_train_matrix_hs = prefix_matrix + '_' + 'train' + '_' + 'hs' + '_' + str(i) + '.csv'
        f_name_train_matrix_binary = prefix_matrix + '_' + 'train' + '_' + 'binary' + '_' + str(i) + '.csv'
        f_name_train_matrix_md = prefix_matrix + '_' + 'train' + '_' + 'md' + '_' + str(i) + '.csv'

        #tirps_matrix_for_train.to_csv(f_name_train_matrix)

        tirps_matrix_for_train_hs.to_csv(f_name_train_matrix_hs)
        tirps_matrix_for_train_binary.to_csv(f_name_train_matrix_binary)
        tirps_matrix_for_train_md.to_csv(f_name_train_matrix_md)


        # test tirps
        for d in range(0, num_of_classes):
            detected_tirps_class_curr_in_test = tirp_detection_obj.Sequential_TIRPs_Detection_multiply_entities(
                frequent_tirps=drop_recurrences_of_tirps(all_tirps_classes, num_of_relations),
                time_intervals_entities_path=test_file_classes[d],
                max_gap=max_gap,
                epsilon=0, num_comma=num_comma)


            matrix_class_curr_test_hs = tirp_feature_ext_obj.getMatrixForModeling(tirps=drop_recurrences_of_tirps(
                all_demi_tirps + detected_tirps_class_curr_in_test, num_of_relations),
                entities_list=list(
                    tirp_detection_obj._entities_map_to_detect.keys()),
                representation='HS',
                num_of_relations=num_of_relations, label=labels[d])

            matrix_class_curr_test_binary = tirp_feature_ext_obj.getMatrixForModeling(tirps=drop_recurrences_of_tirps(
                all_demi_tirps + detected_tirps_class_curr_in_test, num_of_relations),
                entities_list=list(
                    tirp_detection_obj._entities_map_to_detect.keys()),
                representation='BIN',
                num_of_relations=num_of_relations, label=labels[d])

            matrix_class_curr_test_md = tirp_feature_ext_obj.getMatrixForModeling(tirps=drop_recurrences_of_tirps(
                all_demi_tirps + detected_tirps_class_curr_in_test, num_of_relations),
                entities_list=list(
                    tirp_detection_obj._entities_map_to_detect.keys()),
                representation='MD',
                num_of_relations=num_of_relations, label=labels[d])

            #all_matrices_test.append(matrix_class_curr_test)

            all_matrices_test_hs.append(matrix_class_curr_test_hs)
            all_matrices_test_binary.append(matrix_class_curr_test_binary)
            all_matrices_test_md.append(matrix_class_curr_test_md)




        tirps_matrix_for_test_hs = tirp_feature_ext_obj.concat_matrix_classes(all_matrices_test_hs)
        tirps_matrix_for_test_binary = tirp_feature_ext_obj.concat_matrix_classes(all_matrices_test_binary)
        tirps_matrix_for_test_md = tirp_feature_ext_obj.concat_matrix_classes(all_matrices_test_md)


        f_name_test_matrix_hs = prefix_matrix + '_' + 'test' + '_'+ 'hs' + "_" + str(i) + '.csv'
        f_name_test_matrix_binary = prefix_matrix + '_' + 'test' + '_'+ 'binary' + "_" + str(i) + '.csv'
        f_name_test_matrix_md = prefix_matrix + '_' + 'test' + '_'+ 'md' + "_" + str(i) + '.csv'



        tirps_matrix_for_test_hs.to_csv(f_name_test_matrix_hs)
        tirps_matrix_for_test_binary.to_csv(f_name_test_matrix_binary)
        tirps_matrix_for_test_md.to_csv(f_name_test_matrix_md)



        col_hs,col_bin,col_md = get_all_kl_num_of_columns(f_name_test_matrix_hs,f_name_test_matrix_binary,f_name_test_matrix_md)

        if col_hs > 2:
            y_pred_hs, y_test_hs = run_classification(tirps_matrix_for_train_hs, tirps_matrix_for_test_hs, labels)
            auc_hs, acc_hs, precision_hs, recall_hs = update_results(y_pred_hs, y_test_hs,
                                                                     RandomForest_AUC_list_hs,
                                                                     RandomForest_accuracy_list_hs,
                                                                     RandomForest_precision_list_hs,
                                                                     RandomForest_recall_list_hs)
            print("Finished fold number %i, results for horizontal support, auc:%0.2f, accuracy:%0.2f, precision:%0.2f, recall:%0.2f" % (
                    i, auc_hs, acc_hs, precision_hs, recall_hs))
        if col_bin > 2:
            y_pred_binary, y_test_binary = run_classification(tirps_matrix_for_train_binary,tirps_matrix_for_test_binary, labels)
            auc_binary, acc_binary, precision_binary, recall_binary = update_results(y_pred_binary, y_test_binary,
                                                                                     RandomForest_AUC_list_binary,
                                                                                     RandomForest_accuracy_list_binary,
                                                                                     RandomForest_precision_list_binary,
                                                                                     RandomForest_recall_list_binary)
            print("Finished fold number %i, results for binary, auc:%0.2f, accuracy:%0.2f, precision:%0.2f, recall:%0.2f" % (
                    i, auc_binary, acc_binary, precision_binary, recall_binary))

        if col_md > 2:
            y_pred_md, y_test_md = run_classification(tirps_matrix_for_train_md, tirps_matrix_for_test_md, labels)
            auc_md, acc_md, precision_md, recall_md = update_results(y_pred_md, y_test_md,
                                                                     RandomForest_AUC_list_md,
                                                                     RandomForest_accuracy_list_md
                                                                     ,RandomForest_precision_list_md,
                                                                     RandomForest_recall_list_md)
            print("Finished fold number %i, results for mean duration, auc:%0.2f, accuracy:%0.2f, precision:%0.2f, recall:%0.2f \n" % (
                    i, auc_md, acc_md, precision_md, recall_md))



    print("Program finished for current working directory.")
    program_rtime_seconds = time.time() - start_time
    program_rtime_minutes = program_rtime_seconds/60.0
    program_rtime_hours = program_rtime_minutes/60.0
    programrtime_days = program_rtime_hours/24.0
    print("--- %s seconds ---" % (program_rtime_seconds))
    print("--- %s minutes ---" % (program_rtime_minutes))
    print("--- %s hours ---" % (program_rtime_hours))
    print("--- %s days ---" % (programrtime_days))

    if col_hs > 2:
        print_final_kfold_results(RandomForest_AUC_list_hs,RandomForest_accuracy_list_hs,
                                  RandomForest_precision_list_hs,RandomForest_recall_list_hs,'horizontal support')
    if col_bin > 2:
        print_final_kfold_results(RandomForest_AUC_list_binary, RandomForest_accuracy_list_binary,
                                  RandomForest_precision_list_binary, RandomForest_recall_list_binary,'binary')
    if col_md > 2:
        print_final_kfold_results(RandomForest_AUC_list_md, RandomForest_accuracy_list_md,
                                  RandomForest_precision_list_md, RandomForest_recall_list_md,'mean duration')



def cv_process(path,folds):
    '''
    The function runs the entire cv process on a given subfolders that contai ndiscretized data.
    :param path: string, path to general data folder
    :return: No return value
    '''
    subfolders = [entry.path for entry in os.scandir(path) if entry.is_dir()]
    list_of_current_folders = []
    for folder in subfolders:
        list_of_current_folders.clear()
        for file in os.listdir(folder):
            full_file_path = (os.path, join(folder, file))[1]
            list_of_current_folders.append(full_file_path)
        prefix_matrix_current_path = folder+"\\matrix_mea"
        print("Current working directory: %s" %folder)
        CV_example_multi_label(sorted(list_of_current_folders),prefix_matrix_current_path,k=folds)

#CV_example('C:/Users/user/PycharmProjects/similarityKarmalEGO/data_sets/icu/SAX_OUT_TEST_Class0.txt','C:/Users/user/PycharmProjects/similarityKarmalEGO/data_sets/icu/SAX_OUT_TEST_Class1.txt',
#            'C:/Users/user/PycharmProjects/similarityKarmalEGO/data_sets/icu/matrix',max_gap=1,representation='HS',min_ver_support=0.8)
cv_process('D:\python_projects\\bgukarmalego\KarmaLego_TestsData\mea_fake',5)

