from abc import abstractmethod
from discretization.discretization import Discretization


class Unsupervised(Discretization):
    @abstractmethod
    def generate_cutpoints(self, prop_df, nb_bins, *args, **kwargs):
        return
