class FileNames:
    PROP_DATA = 'prop-data'
    ENTITY_CLASS_RELATIONS = 'entity-class-relations'
    STATES = 'states'
    SYMBOLIC_TIME_SERIES = 'symbolic-time-series'
    KL = 'KL'


class DatasetColumns:
    EntityID = 'EntityID'
    TemporalPropertyID = 'TemporalPropertyID'
    TimeStamp = 'TimeStamp'
    TemporalPropertyValue = 'TemporalPropertyValue'


class EntityClassRelationsColumns:
    EntityID = DatasetColumns.EntityID
    ClassID = 'ClassID'


class StatesColumns:
    StateID = 'StateID'
    TemporalPropertyID = DatasetColumns.TemporalPropertyID
    BinID = 'BinID'
    BinLow = 'BinLow'
    BinHigh = 'BinHigh'
    BinLowScore = 'BinLowScore'


class TimeIntervalsColumns:
    EntityID = DatasetColumns.EntityID
    TemporalPropertyID = DatasetColumns.TemporalPropertyID
    StateID = StatesColumns.StateID
    Start = 'Start'
    End = 'End'


class SymbolicTimeSeriesColumns:
    EntityID = DatasetColumns.EntityID
    TemporalPropertyID = DatasetColumns.TemporalPropertyID
    TimeStamp = DatasetColumns.TimeStamp
    StateID = StatesColumns.StateID


class PreprocessingParamsColumns:
    TemporalPropertyID = DatasetColumns.TemporalPropertyID
    PAAWindowSize = 'PAAWindowSize'
    StdCoef = 'StdCoefficient'
    MaxGap = 'MaxGap'


class TemporalAbstractionParamsColumns:
    TemporalPropertyID = DatasetColumns.TemporalPropertyID
    Method = 'Method'
    NbBins = 'NbBins'
    GradientWindowSize = 'GradientWindowSize'


class DefaultValues:
    PAA_WINDOW = 1
    MAX_GAP = 1
    GRADIENT_WINDOW = None
    CLASS_ID = None
    STD_COEF = None


class MethodsNames:
    Gradient = 'gradient'
    KnowledgeBased = 'knowledge-based'
    SAX = 'sax'
    KMeans = 'kmeans'
    EqualWidth = 'equal-width'
    EqualFrequency = 'equal-frequency'
    TD4CKullbackLeibler = 'td4c-skl'
    TD4CEntropy = 'td4c-entropy'
    TD4CCosine = 'td4c-cosine'
    Persist = 'persist'


def get_supervised_methods_names():
    return [MethodsNames.TD4CCosine,
            MethodsNames.TD4CEntropy,
            MethodsNames.TD4CKullbackLeibler]


def get_unsupervised_methods_names():
    return [MethodsNames.EqualWidth,
            MethodsNames.EqualFrequency,
            MethodsNames.SAX,
            MethodsNames.KMeans,
            MethodsNames.Persist]


def get_discretization_methods_names():
    return get_unsupervised_methods_names() + get_supervised_methods_names()
