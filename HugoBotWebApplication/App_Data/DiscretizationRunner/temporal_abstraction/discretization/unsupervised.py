from abc import abstractmethod
from temporal_abstraction.discretization.discretization import Discretization


class Unsupervised(Discretization):

    @abstractmethod
    def _generate_cutpoints(self, prop_df):
        """ this is an abstract method """
