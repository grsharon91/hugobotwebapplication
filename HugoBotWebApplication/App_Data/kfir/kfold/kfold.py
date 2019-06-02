from discretization.discretization import Discretization
from discretize import create_discretization
from files_manager.files_manager import FilesManager
from sklearn.model_selection import StratifiedKFold

from time_intervals_adapter.time_intervals_adapter import create_time_intervals, time_intervals_to_string


class KFoldTest:

    def __init__(self, nb_folds, dataset_name, method, nb_bins, paa_window_size=1, max_gap=1):
        self.dataset_name = dataset_name
        self.method = method
        self.nb_bins = nb_bins
        self.files_manager = FilesManager(dataset_name, method, nb_bins)
        self.nb_folds = nb_folds
        self.paa_window_size = paa_window_size
        self.max_gap = max_gap

    def divide_dataset(self):
        dataset = self.files_manager.read_dataset()
        entity_class_relations = self.files_manager.read_entity_class_relations()

        classes = dataset.EntityID.apply(lambda x: entity_class_relations.ClassID[
            entity_class_relations.EntityID == x
            ].values[0])

        k_fold = StratifiedKFold(n_splits=self.nb_folds, random_state=1)

        for fold_idx, (train_idx, test_idx) in enumerate(k_fold.split(dataset, classes)):
            self.files_manager.write_dataset_fold(self.nb_folds,
                                                  fold_idx,
                                                  dataset.iloc[train_idx],
                                                  dataset.iloc[test_idx])

    def discretize_folds(self):
        disc = create_discretization(self.method)

        folds = self.files_manager.read_folds(self.nb_folds)

        entity_class_relations = self.files_manager.read_entity_class_relations()

        for fold_idx, fold in enumerate(folds):
            states, dataset = disc.discretize_dataset(fold['train'], self.nb_bins, entity_class_relations)
            self.files_manager.create_fold_states_file(self.nb_folds, fold_idx, states)

            # train results
            train_entities_to_time_intervals = create_time_intervals(dataset, states, self.max_gap)
            train_time_intervals_str = time_intervals_to_string(train_entities_to_time_intervals)
            self.files_manager.create_fold_time_intervals_file(self.nb_folds, fold_idx, train_time_intervals_str,
                                                               is_train=True)

            # test results
            discretized_test_dataset = Discretization.discretize_df_knowledge_based(
                Discretization.extract_cutpoints_from_states(states), fold['test'])
            test_entities_to_time_intervals = create_time_intervals(discretized_test_dataset, states, self.max_gap)
            test_time_intervals_str = time_intervals_to_string(test_entities_to_time_intervals)
            self.files_manager.create_fold_time_intervals_file(self.nb_folds, fold_idx, test_time_intervals_str,
                                                               is_train=False)
