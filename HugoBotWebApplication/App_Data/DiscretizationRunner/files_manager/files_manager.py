import os
from abc import ABC
from functools import reduce

import pandas as pd
from pandas._libs.parsers import is_float_dtype

from constants import DatasetColumns, EntityClassRelationsColumns, FileNames, TimeIntervalsColumns
from time_intervals_adapter.time_intervals_adapter import TimeIntervalsAdapter


class FilesManager(ABC):
    CLASS_IDENTIFIER = -1

    def __init__(self, input_path, output_path, name=''):
        self.input_path = input_path
        self.output_path = output_path
        self.name = name if name == '' else f'{name}-'

    @staticmethod
    def read_csv(file_path):
        return pd.read_csv(file_path)

    def read_dataset(self):
        prop_data_path = self.__get_prop_data_path()
        entity_class_relations_path = self.__get_entity_class_relations_file_path()

        if not (os.path.exists(prop_data_path) and os.path.exists(entity_class_relations_path)):
            self.__extract_entity_class_relations()

        return pd.read_csv(prop_data_path)

    def read_states(self):
        return pd.read_csv(self.__get_states_path())

    def write_states(self, states):
        states.to_csv(self.__get_states_path(), index=False)

    def write_symbolic_time_series(self, sts):
        sts.to_csv(self.__get_symbolic_time_series_path(), index=False)

    def write_KL(self, symbolic_time_intervals):
        with open(self.__get_KL_path(), 'w') as f:
            f.write(FilesManager.parse_time_intervals_to_KL(symbolic_time_intervals))

        if symbolic_time_intervals.empty:
            return

        """ Handles writing of files per class """
        entity_class_relations = self.read_entity_class_relations()
        symbolic_time_intervals_with_classes = symbolic_time_intervals.merge(entity_class_relations)

        for class_id, class_df in symbolic_time_intervals_with_classes.groupby(by=EntityClassRelationsColumns.ClassID):
            with open(self.__get_KL_path(class_id), 'w') as class_f:
                class_f.write(FilesManager.parse_time_intervals_to_KL(class_df))

    def read_KL(self, class_id=None):
        with open(self.__get_KL_path(class_id), 'r') as f:
            return ''.join(f.readlines())

    def read_entity_class_relations(self):
        entity_class_relations_path = self.__get_entity_class_relations_file_path()
        return pd.read_csv(entity_class_relations_path)

    def write_entity_class_relations(self, entity_class_relations):
        entity_class_relations_path = self.__get_entity_class_relations_file_path()
        entity_class_relations.to_csv(entity_class_relations_path, index=False)

    def write_folds(self, folds):
        files_managers = []
        for idx, (train, test) in enumerate(folds):
            fold_name = f'{self.name}fold-{idx}'
            entity_class_relations = self.read_entity_class_relations()

            train_folder_path = os.path.join(self.output_path, fold_name, 'train')
            os.makedirs(train_folder_path)

            train_path = os.path.join(train_folder_path, f'train-{fold_name}.csv')
            train.to_csv(train_path, index=False)

            test_folder_path = os.path.join(self.output_path, fold_name, 'test')
            os.makedirs(test_folder_path)

            test_path = os.path.join(test_folder_path, f'test-{fold_name}.csv')
            test.to_csv(test_path, index=False)

            train_fm = FilesManager(train_path, train_folder_path, f'{fold_name}-train')
            train_fm.read_dataset()
            train_fm.write_entity_class_relations(entity_class_relations)

            test_fm = FilesManager(test_path, test_folder_path, f'{fold_name}-test')
            test_fm.read_dataset()
            test_fm.write_entity_class_relations(entity_class_relations)

            files_managers.append((train_fm, test_fm))
        return files_managers

    def __extract_entity_class_relations(self):
        prop_data_path = self.__get_prop_data_path()
        entity_class_relations_path = self.__get_entity_class_relations_file_path()

        dataset = pd.read_csv(self.input_path)

        entity_class_relations = dataset[
            dataset[DatasetColumns.TemporalPropertyID] == FilesManager.CLASS_IDENTIFIER].copy()

        dataset.drop(entity_class_relations.index, axis='index', inplace=True)
        dataset.to_csv(prop_data_path, index=False)
        del dataset

        entity_class_relations = entity_class_relations.drop(
            [DatasetColumns.TemporalPropertyID, DatasetColumns.TimeStamp],
            axis='columns')
        entity_class_relations = entity_class_relations.rename(
            columns={
                DatasetColumns.TemporalPropertyValue: EntityClassRelationsColumns.ClassID
            })

        entity_class_relations.to_csv(entity_class_relations_path, index=False)

        return

    @staticmethod
    def write_file(path, content):
        with open(path, 'w') as f:
            f.write(content)

    @staticmethod
    def read_file(path):
        with open(path, 'r') as f:
            return ''.join(f.readlines())

    def __get_prop_data_path(self):
        file_name = f'{self.name}{FileNames.PROP_DATA}.csv'
        return os.path.join(self.output_path, file_name)

    def __get_entity_class_relations_file_path(self):
        file_name = f'{self.name}{FileNames.ENTITY_CLASS_RELATIONS}.csv'
        return os.path.join(self.output_path, file_name)

    def __get_states_path(self):
        file_name = f'{self.name}{FileNames.STATES}.csv'
        return os.path.join(self.output_path, file_name)

    def __get_KL_path(self, class_id=None):
        class_str = '' if class_id is None else f'-class-{class_id}'
        file_name = f'{self.name}{FileNames.KL}{class_str}.txt'
        return os.path.join(self.output_path, file_name)

    def __get_symbolic_time_series_path(self):
        file_name = f'{self.name}{FileNames.SYMBOLIC_TIME_SERIES}.csv'
        return os.path.join(self.output_path, file_name)

    @staticmethod
    def parse_KL_to_time_intervals(kl_str):
        file_lines = kl_str.split('\n')[2:]
        entities_to_intervals = zip(list(map(lambda entity_line: entity_line.split(';')[0], file_lines[::2])),
                                    list(map(lambda entity_intervals: list(
                                        map(lambda interval: interval.split(','), entity_intervals.split(';')[:-1])),
                                             file_lines[1::2])))

        intervals = reduce(lambda x, y: x + y, map(lambda entity_to_intervals: list(map(lambda interval: pd.Series({
            TimeIntervalsColumns.EntityID: entity_to_intervals[0],
            TimeIntervalsColumns.TemporalPropertyID: interval[3],
            TimeIntervalsColumns.StateID: interval[2],
            TimeIntervalsColumns.Start: interval[0],
            TimeIntervalsColumns.End: interval[1],
        }), entity_to_intervals[1])), entities_to_intervals))

        return TimeIntervalsAdapter.set_columns_types(pd.DataFrame(intervals))

    @staticmethod
    def parse_time_intervals_to_KL(time_intervals_df):
        """
        convert the resulted time-intervals to a string matching the input format of KarmaLego
        :param time_intervals_df:
        :return: string representation of the time intervals in KarmaLego format
        """

        time_intervals_df = time_intervals_df.sort_values(
            by=[TimeIntervalsColumns.Start, TimeIntervalsColumns.End, TimeIntervalsColumns.StateID]).dropna()

        time_intervals_df = TimeIntervalsAdapter.set_columns_types(time_intervals_df)

        intervals_str = time_intervals_df.groupby(by=DatasetColumns.EntityID). \
            apply(
            lambda entity_df: ';'.join(map(lambda x: ','.join(x.split()), entity_df.to_string(
                header=False,
                index=False,
                index_names=False,
                columns=[TimeIntervalsColumns.Start,
                         TimeIntervalsColumns.End,
                         TimeIntervalsColumns.StateID,
                         TimeIntervalsColumns.TemporalPropertyID]).split('\n')))
        )

        nb_entities = intervals_str.size

        entities_intervals = ''
        for entity_id, entity_intervals in intervals_str.iteritems():
            entities_intervals += '{};\n{};\n'.format(
                entity_id,
                entity_intervals
            )
        entities_intervals = entities_intervals[:-1]  # to remove last redundant '\n'

        intervals_str = 'startToncepts\nnumberOfEntities,{}\n{}'.format(
            nb_entities,
            entities_intervals
        )

        return intervals_str
