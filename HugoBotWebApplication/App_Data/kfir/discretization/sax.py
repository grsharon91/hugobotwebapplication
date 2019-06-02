from scipy.stats import norm
from discretization.decorators import prop_vals_only
from discretization.unsupervised import Unsupervised
from math import isnan


class SAX(Unsupervised):

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

    def generate_cutpoints(self, prop_df, nb_bins, *args, **kwargs):
        return SAX.sax(prop_df, nb_bins)
