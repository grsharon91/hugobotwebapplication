import pandas as pd
import dask.dataframe as dd
import os


class FilesManager:

    def __init__(self,
                 dataset_name,
                 method,
                 nb_bins,
                 paa_window_size=1,
                 max_gap=1,
                 gradient_window_size=None,
                 block_size=0,
                 use_dask=False,
                 dataset_path=None,
                 output_path=None,
                 ):
        print('creating files manager...')
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.dataset_name = dataset_name
        self.method = method
        self.nb_bins = nb_bins
        self.paa_window_size = paa_window_size
        self.max_gap = max_gap
        self.gradient_window_size = gradient_window_size
        self.use_dask = use_dask

        self.block_size = block_size
        self.loader = dd.read_csv if self.use_dask else pd.read_csv
        return

    def extract_entity_class_relations(self):
        dataset_path = self.get_dataset_file_path()
        prop_data_path = self.get_prop_data_path()
        entity_class_relations_path = self.get_entity_class_relations_file_path()

        dataset = pd.read_csv(dataset_path)

        entity_class_relations = dataset[dataset.TemporalPropertyID == -1].copy()

        dataset.drop(entity_class_relations.index, axis='index', inplace=True)
        dataset.to_csv(prop_data_path, index=False)
        del dataset

        entity_class_relations = entity_class_relations.drop(['TemporalPropertyID', 'TimeStamp'], axis='columns')
        entity_class_relations = entity_class_relations.rename(columns={'TemporalPropertyValue': 'ClassID'})

        entity_class_relations.to_csv(entity_class_relations_path, index=False)

        return

    def read_dataset(self):
        print('reading dataset...')
        prop_data_path = self.get_prop_data_path()
        entity_class_relations_path = self.get_entity_class_relations_file_path()

        if not (os.path.exists(prop_data_path) and os.path.exists(entity_class_relations_path)):
            self.extract_entity_class_relations()

        if self.use_dask and self.block_size != 0:
            return self.loader(prop_data_path, blocksize=self.block_size)
        else:
            return self.loader(prop_data_path)

    def read_entity_class_relations(self):
        print('reading entity-class relations...')
        entity_class_relations_path = self.get_entity_class_relations_file_path()
        return pd.read_csv(entity_class_relations_path)

    def create_entity_class_relations_file(self, entity_class_relations):
        entity_class_relations_path = self.get_entity_class_relations_file_path()
        entity_class_relations.to_csv(entity_class_relations_path, index=False)

    def create_states_file(self, states):
        print('creating states file...')
        states_file_path = self.get_states_file_path()
        states.to_csv(states_file_path, index=False)
        return

    def create_time_intervals_file(self, entities_to_time_intervals_str, class_id=''):
        print('creating time-intervals file...')
        time_intervals_file_path = self.get_time_intervals_file_path(class_id)
        open(time_intervals_file_path, 'w').write(entities_to_time_intervals_str)
        return

    def get_output_folder_path(self):
        if self.output_path is not None:
            folder_path = self.output_path
        else:
            folder_path = self.get_default_folder_path()
        return folder_path

    def get_default_folder_path(self):
        cwd = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir)
        folder_path = os.path.join(cwd, 'Datasets', self.dataset_name)
        return folder_path

    def get_running_config_folder_path(self):
        running_config_folder_path = os.path.join(self.get_output_folder_path(),
                                                  f'{self.method}_{self.nb_bins}bins_'
                                                  f'{self.paa_window_size}paa_{self.max_gap}max-gap'
                                                  f'{("_" + str(int(self.gradient_window_size)) + "gradient-window") if self.gradient_window_size != None else ""}')
        os.makedirs(running_config_folder_path, exist_ok=True)
        return running_config_folder_path

    def get_folds_running_config_folder_path(self, nb_folds):
        folds_running_config_folder_path = \
            os.path.join(self.get_output_folder_path(),
                         f'{nb_folds}folds_{self.method}_{self.nb_bins}bins'
                         f'_{self.paa_window_size}paa_{self.max_gap}max-gap')
        os.makedirs(folds_running_config_folder_path, exist_ok=True)
        return folds_running_config_folder_path

    def get_dataset_file_path(self):
        if self.dataset_path is not None:
            dataset_path = self.dataset_path
        else:
            dataset_folder_path = self.get_default_folder_path()
            dataset_path = os.path.join(dataset_folder_path, f'{self.dataset_name}.csv')
        return dataset_path

    def get_discretized_file_path(self):
        dataset_folder_path = self.get_output_folder_path()
        results_file_name = self.get_discretized_file_name()
        return os.path.join(dataset_folder_path, results_file_name)

    def get_discretized_file_name(self, nb_class=''):
        results_file_name = '{}_discretized_{}_{}bins_{}paa{}.csv'.format(
            self.dataset_name,
            self.method,
            self.nb_bins,
            self.paa_window_size,
            '_class' + str(nb_class) if nb_class != '' else '')
        return results_file_name

    def get_states_file_path(self):
        return os.path.join(self.get_running_config_folder_path(),
                            f'{self.dataset_name}_states_{self.method}_'
                            f'{self.nb_bins}bins_{self.paa_window_size}paa.csv')

    def get_entity_class_relations_file_path(self):
        dataset_folder_path = self.get_output_folder_path()
        return os.path.join(dataset_folder_path, f'{self.dataset_name}_entity-class-relations.csv')

    def get_time_intervals_file_path(self, class_id):
        return os.path.join(
            self.get_running_config_folder_path(),
            ('{dataset_name}_time-intervals_'
             '{method_name}_{nb_bins}bins_'
             '{paa_window_size}paa_{max_gap}max-gap_'
             '{gradient_window_size}{nb_class}.txt').format(
                dataset_name=self.dataset_name,
                method_name=self.method,
                nb_bins=self.nb_bins,
                paa_window_size=self.paa_window_size,
                max_gap=self.max_gap,
                gradient_window_size=('_' + str(int(self.gradient_window_size)) + 'gradient-window') if self.gradient_window_size != None else '',
                nb_class='_class' + str(int(class_id)) if class_id != '' else ''
            ))

    def get_prop_data_path(self):
        dataset_folder_path = self.get_output_folder_path()
        prop_data_path = os.path.join(dataset_folder_path, f'{self.dataset_name}_prop-data.csv')
        return prop_data_path

    def get_dataset_fold_path(self, nb_folds, fold_idx):
        dataset_folder_path = self.get_folds_running_config_folder_path(nb_folds)
        file_name = 'dataset_{}folds_%s_fold{}.csv'.format(nb_folds, fold_idx)
        train_file_name = file_name % ('train',)
        test_file_name = file_name % ('test',)

        train_file_path = os.path.join(dataset_folder_path, train_file_name)
        test_file_path = os.path.join(dataset_folder_path, test_file_name)

        return train_file_path, test_file_path

    def write_dataset_fold(self, nb_folds, fold_idx, train_dataset, test_dataset):
        train_file_path, test_file_path = self.get_dataset_fold_path(nb_folds, fold_idx)

        train_dataset.to_csv(train_file_path, index=False)
        test_dataset.to_csv(test_file_path, index=False)
        return

    def read_folds(self, nb_folds):
        folds = []

        for fold_idx in range(nb_folds):
            train_file_path, test_file_path = self.get_dataset_fold_path(nb_folds, fold_idx)
            train_dataset = pd.read_csv(train_file_path)
            test_dataset = pd.read_csv(test_file_path)

            folds.append({
                'train': train_dataset,
                'test': test_dataset
            })
        return folds

    def get_fold_states_file_path(self, nb_folds, fold_idx):
        return os.path.join(self.get_folds_running_config_folder_path(nb_folds),
                            ('{dataset_name}_{nb_folds}folds_states_{method_name}_{nb_bins}bins_' +
                             '{paa_window_size}paa_fold{fold_idx}.csv').format(
                                dataset_name=self.dataset_name,
                                nb_folds=nb_folds,
                                method_name=self.method,
                                nb_bins=self.nb_bins,
                                paa_window_size=self.paa_window_size,
                                fold_idx=fold_idx
                            ))

    def create_fold_states_file(self, nb_folds, fold_idx, states):
        fold_states_file_path = self.get_fold_states_file_path(nb_folds, fold_idx)
        states.to_csv(fold_states_file_path, index=False)
        return

    def create_fold_time_intervals_file(self, nb_folds, fold_idx, entities_to_time_intervals_str, is_train):
        print('creating time-intervals file...')
        time_intervals_file_path = self.get_fold_time_intervals_file_path(nb_folds, fold_idx, is_train)
        open(time_intervals_file_path, 'w').write(entities_to_time_intervals_str)
        return

    def get_fold_time_intervals_file_path(self, nb_folds, fold_idx, is_train):
        return os.path.join(
            self.get_folds_running_config_folder_path(nb_folds),
            ('{dataset_name}_{nb_folds}folds_{is_train}_time-intervals_{method_name}_' +
             '{nb_bins}bins_{paa_window_size}paa_{max_gap}max-gap_fold{fold_idx}.csv').format(
                dataset_name=self.dataset_name,
                nb_folds=nb_folds,
                is_train='train' if is_train else 'test',
                method_name=self.method,
                nb_bins=self.nb_bins,
                paa_window_size=self.paa_window_size,
                max_gap=self.max_gap,
                fold_idx=fold_idx
            ))

    @staticmethod
    def write_dataset(dataset_name, prop_data, entity_class_relations):
        folder_path = r'C:\Users\zvikf\PycharmProjects\temporali-python\Datasets\{}'.format(dataset_name)
        os.makedirs(folder_path)
        file_path = os.path.join(folder_path, 'paa.csv')
        entity_path = os.path.join(folder_path, 'entity-class-relations.csv')

        prop_data.to_csv(file_path)
        entity_class_relations.to_csv(entity_path)
        return

    @staticmethod
    def read_states_file(states_file_path):
        print('reading states file...')
        states = pd.read_csv(states_file_path)
        return states
