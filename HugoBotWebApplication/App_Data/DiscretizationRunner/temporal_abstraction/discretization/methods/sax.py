from scipy.stats import norm
from temporal_abstraction.discretization.decorators import prop_vals_only
from temporal_abstraction.discretization.unsupervised import Unsupervised
from math import isnan


class SAX(Unsupervised):
    """
        We use a statistics library in order to generate bins so that
        the area of each bin under the normal distribution function created from the samples
        will be equal
    """

    @staticmethod
    @prop_vals_only
    def sax(prop_values, nb_bins):
        mean = prop_values.mean()
        std = prop_values.std()

        if std == 0 or isnan(std):
            return []

        rv = norm(loc=mean, scale=std)
        cutpoints = [rv.ppf(bin_id / nb_bins) for bin_id in range(1, nb_bins, 1)]
        cutpoints = sorted(list(set(cutpoints)))
        return cutpoints

    def _generate_cutpoints(self, prop_df):
        return SAX.sax(prop_df, self._nb_bins)
