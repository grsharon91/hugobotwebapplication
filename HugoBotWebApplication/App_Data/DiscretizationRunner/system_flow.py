from abstraction_per_property.abstraction_per_property import AbstractionPerProperty
from constants import TemporalAbstractionParamsColumns, MethodsNames
from kfold.kfold import KFold


def regular_system_flow(files_manager, preprocessing_params_df, temporal_abstraction_params_df, states=None):
    """
    Running the system without K-Fold
    :param files_manager: FilesManager object, needs to get input and output paths
    :param preprocessing_params_df: Dataframe, contains parameters per property with no duplicates in property
    :param temporal_abstraction_params_df: Dataframe, contains parameters per property with possible duplicates
    :param states: Dataframe, contains known states (knowledge-based)
    :return:
    """
    dataset = files_manager.read_dataset()
    entity_class_relations = files_manager.read_entity_class_relations()

    # abstraction per property
    app = AbstractionPerProperty(preprocessing_params_df, temporal_abstraction_params_df)

    dataset = app.preprocessing_per_property(dataset)
    states, symbolic_time_series = app.temporal_abstraction_per_property(dataset,
                                                                         entity_class_relations,
                                                                         states)
    symbolic_time_intervals = app.intervalization_per_property(symbolic_time_series)

    files_manager.write_states(states)
    files_manager.write_symbolic_time_series(symbolic_time_series)
    files_manager.write_KL(symbolic_time_intervals)


def kfold_system_flow(nb_folds, files_manager, preprocessing_params_df, temporal_abstraction_params_df, states=None):
    """
    Running the system using k-fold
    :param nb_folds: int, the amount of folds to divide the data into
    :param files_manager: see above
    :param preprocessing_params_df: see above
    :param temporal_abstraction_params_df: see above
    :param states: see above
    :return:
    """
    kfold = KFold(nb_folds, files_manager.read_entity_class_relations())
    folds = kfold.divide_dataset(files_manager.read_dataset())

    fms = files_manager.write_folds(folds)

    for (train_fm, test_fm) in fms:
        # running the system on the train set
        regular_system_flow(train_fm, preprocessing_params_df, temporal_abstraction_params_df, states)

        """ making a copy of the params df, changing the method to knowledge-based so
            we can run the system on the test set with the states of the train set
        """
        knowledge_based_temporal_abstraction_params_df = temporal_abstraction_params_df.copy()
        knowledge_based_temporal_abstraction_params_df[TemporalAbstractionParamsColumns.Method] = \
            knowledge_based_temporal_abstraction_params_df[TemporalAbstractionParamsColumns.Method].apply(
                lambda x: MethodsNames.KnowledgeBased)

        # running the system on the test set with knowledge-based states taken from the train set
        regular_system_flow(test_fm, preprocessing_params_df, knowledge_based_temporal_abstraction_params_df,
                            train_fm.read_states())


def system_flow(files_manager, preprocessing_params_df, temporal_abstraction_params_df, states=None, kfold=None):
    if kfold:
        kfold_system_flow(kfold, files_manager, preprocessing_params_df, temporal_abstraction_params_df, states)
    else:
        regular_system_flow(files_manager, preprocessing_params_df, temporal_abstraction_params_df, states)
