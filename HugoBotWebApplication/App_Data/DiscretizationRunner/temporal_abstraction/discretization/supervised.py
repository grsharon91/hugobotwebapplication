from abc import abstractmethod

from temporal_abstraction.discretization.discretization import Discretization


class Supervised(Discretization):

    def __init__(self, nb_bins, entity_class_relations):
        """
        :param nb_bins: int, the number of bins
        :param entity_class_relations: Dataframe
        """
        super().__init__(nb_bins)
        self._entity_class_relations = entity_class_relations

    @abstractmethod
    def _generate_cutpoints(self, prop_df):
        """ this is an abstract method """
