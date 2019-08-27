import pandas as pd
import numpy as np

class TIRPsFeatureExtraction (object):

    def __init__(self,min_ver_support=0.5):
        self._min_ver_support=min_ver_support


    def create_feature_matrix(self, tirps, entities_list, representation, entities_class, entities_class_header='CLASS', entities_list_header='ID'):
        """
        Construct a feature matrix from a given arguments as a Data Frame.
        header name for each TIRP will be the value from TIRP`s 'to_string' method.
        :param entities_list_header: the value of the header of the entity id values, default is 'ID'
        :param entities_class_header: the value of the header of the class value, default is 'CLASS'
        :param tirps: TIRPs that will be converted to features per entity
        :param entities_list: the list od the entities that will be the features entities.
        :param representation: BIN (binary) or HS (Horizontal Support)or MD (Mean Duration)
        :param entities_class: the Class value of the given entities.
        :return: Data frame of features and class column from a given TIRPs.
        """

        features_matrix = {}

        features_matrix[entities_list_header] = entities_list
        for tirp in tirps:
            features_matrix[tirp.to_string()] = self.getFeaturesListByTIRP(tirp, entities_list, representation)
        features_matrix[entities_class_header] = [entities_class for x in range(0, len(entities_list))]

        return pd.DataFrame(data=features_matrix)

    def getFeaturesListByTIRP(self,tirp,entities_list,representation):
        """
        calculate the feature vector according to the tirp representation
        :param tirp: TIRP, creating the feature vector according to a given tirp
        :param representation: String, the relevent representation
        :param entities_list: the entities list in the population
        :return: list of double, the features list
        """
        feature_list=[]
        entities_list = entities_list
        if representation=='BIN':
            feature_list=[1  if( x in tirp._supporting_sequences_by_entity.keys()) else 0 for x in entities_list]
        elif representation=='HS' or representation=='HSN':
            for x in entities_list:
                if x in tirp._supporting_sequences_by_entity:
                    feature_list.append(len(tirp._supporting_sequences_by_entity[x]))
                else:
                    feature_list.append(0)
        elif representation == 'MD':
            for entity in entities_list:
                instances=[instances for entity_id, instances in tirp._supporting_sequences_by_entity.items() if entity_id==entity]
                if len(instances)==0:
                    feature_list.append(0)
                else:
                    instances=instances[0]
                    start_list=[]
                    end_list=[]
                    duration_list=[]
                    for i,instance in enumerate(instances):
                        start_list.extend([x._start_time for x in instance])
                        end_list.extend([x._end_time for x in instance])
                        min_start_time=min(start_list)
                        max_end_time=max(end_list)
                        duration=max_end_time-min_start_time
                        duration_list.append(duration)
                        start_list = []
                        end_list = []
                    mean_duration=sum(duration_list)/len(duration_list)
                    feature_list.append(mean_duration)
        return feature_list

    def getMatrixForModeling(self,tirps,entities_list,representation,num_of_relations,label):
        """
        create a features+class matrix for modeling according to the relevant representation
        :param tirps: list of tirps for creating the matrix
        :param entities_list: the entities list in the population
        :param representation: String, 'BIN' OR 'HS' OR 'MND'
        :return:
        """
        data = pd.DataFrame()
        labels=[]
        for i in entities_list:
            labels.append(label)
        for tirp in tirps:
            tirp_name=tirp.get_tirp_name(num_of_relations)
            values=self.getFeaturesListByTIRP(tirp,entities_list,representation)
            data[tirp_name] =pd.Series(np.array(values)).astype(float)
        if representation == 'HSN':
            data=self.HSN(entities_list, tirps, data, num_of_relations)
        data["class"] = pd.Series(np.array(labels))
        return data

    def concat_matrix_classes(self,matrixes):
        result=pd.concat(matrixes, ignore_index=True)
        result.fillna(0, inplace=True)
        return result

    def HSN(self,entities_list,tirps,data,num_of_relations):
        for entity_index in range(0, len(entities_list)):
            max = 1
            for tirp in tirps:
                if data[tirp.get_tirp_name(num_of_relations)][entity_index] > max:
                    max = data[tirp.get_tirp_name(num_of_relations)][entity_index]
            for tirp in tirps:
                data.loc[entity_index, tirp.get_tirp_name(num_of_relations)] = float(data.loc[entity_index, tirp.get_tirp_name(num_of_relations)] / max)
        return data
