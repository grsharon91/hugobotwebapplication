from abc import abstractmethod

from discretization.discretization import Discretization


class Supervised(Discretization):

    def generate_cutpoints(self, prop_df, nb_bins, *args, **kwargs):
        return self.generate_cutpoints_supervised(prop_df, nb_bins, *args, **kwargs)

    @abstractmethod
    def generate_cutpoints_supervised(self, prop_df, nb_bins, class_relations):
        pass
