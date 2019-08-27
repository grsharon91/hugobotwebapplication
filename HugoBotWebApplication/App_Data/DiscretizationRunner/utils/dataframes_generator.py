import pandas as pd

from constants import DatasetColumns, EntityClassRelationsColumns, SymbolicTimeSeriesColumns, TimeIntervalsColumns, \
    StatesColumns, TemporalAbstractionParamsColumns, PreprocessingParamsColumns


class DataframesGenerator:

    @staticmethod
    def generate_symbolic_time_series(entities, properties, timestamps, symbols):
        return pd.DataFrame({
            SymbolicTimeSeriesColumns.EntityID: entities,
            SymbolicTimeSeriesColumns.TemporalPropertyID: properties,
            SymbolicTimeSeriesColumns.TimeStamp: timestamps,
            SymbolicTimeSeriesColumns.StateID: symbols
        })

    @staticmethod
    def generate_empty_symbolic_time_series():
        return DataframesGenerator.generate_symbolic_time_series(
            [], [], [], []
        )

    @staticmethod
    def generate_entity_class_relations(entities, classes):
        return pd.DataFrame({
            EntityClassRelationsColumns.EntityID: entities,
            EntityClassRelationsColumns.ClassID: classes
        })

    @staticmethod
    def generate_empty_dataset():
        return DataframesGenerator.generate_dataset(
            [],
            [],
            [],
            []
        )

    @staticmethod
    def generate_dataset(entities, properties, timestamps, values):
        df_values = {
            DatasetColumns.EntityID: entities,
            DatasetColumns.TemporalPropertyID: properties,
            DatasetColumns.TimeStamp: timestamps,
            DatasetColumns.TemporalPropertyValue: values
        }
        return pd.DataFrame.from_dict(df_values)

    """ may be useful in the future - creates a random dataset """
    # @staticmethod
    # def generate(nb_entities, nb_classes, nb_properties, nb_entries, save_on_disk=True):
    #     prop_data = DataframesGenerator.generate_dataset(
    #         np.random.randint(0, nb_entities, size=nb_entries),
    #         np.random.randint(0, nb_properties, size=nb_entries),
    #         np.arange(nb_entries),
    #         np.random.randn(nb_entries)
    #     )
    #     entity_class_relations = DataframesGenerator.generate_entity_class_relations(
    #         np.arange(nb_entities),
    #         np.random.choice(np.arange(nb_classes), size=nb_entities)
    #     )
    #
    #     if save_on_disk:
    #         dataset_name = 'random_dataset_({}-entities,{}-classes,{}-props,{}-entries)'.format(
    #             nb_entities,
    #             nb_classes,
    #             nb_properties,
    #             nb_entries
    #         )
    #         FilesManager.write_dataset(dataset_name, prop_data, entity_class_relations)
    #
    #     return prop_data, entity_class_relations

    @staticmethod
    def generate_empty_symbolic_time_intervals():
        return DataframesGenerator.generate_symbolic_time_intervals(
            [], [], [], [], []
        )

    @staticmethod
    def generate_symbolic_time_intervals(entities, properties, states, start_times, end_times):
        return pd.DataFrame({
            TimeIntervalsColumns.EntityID: entities,
            TimeIntervalsColumns.TemporalPropertyID: properties,
            TimeIntervalsColumns.StateID: states,
            TimeIntervalsColumns.Start: start_times,
            TimeIntervalsColumns.End: end_times,
        })

    @staticmethod
    def generate_states(states, properties, bins, bins_low, bins_high, bins_low_scores):
        return pd.DataFrame({
            StatesColumns.StateID: states,
            StatesColumns.TemporalPropertyID: properties,
            StatesColumns.BinID: bins,
            StatesColumns.BinLow: bins_low,
            StatesColumns.BinHigh: bins_high,
            StatesColumns.BinLowScore: bins_low_scores
        })

    @staticmethod
    def generate_temporal_abstraction_params(properties, methods, nb_bins,
                                             gradient_sizes):
        return pd.DataFrame({
            TemporalAbstractionParamsColumns.TemporalPropertyID: properties,
            TemporalAbstractionParamsColumns.Method: methods,
            TemporalAbstractionParamsColumns.NbBins: nb_bins,
            TemporalAbstractionParamsColumns.GradientWindowSize: gradient_sizes
        })

    @staticmethod
    def generate_preprocessing_params(properties, paa_sizes, stds, max_gaps):
        return pd.DataFrame({
            PreprocessingParamsColumns.TemporalPropertyID: properties,
            PreprocessingParamsColumns.PAAWindowSize: paa_sizes,
            PreprocessingParamsColumns.StdCoef: stds,
            PreprocessingParamsColumns.MaxGap: max_gaps
        })

    @staticmethod
    def generate_empty_states():
        return DataframesGenerator.generate_states(
            [],
            [],
            [],
            [],
            [],
            []
        )
