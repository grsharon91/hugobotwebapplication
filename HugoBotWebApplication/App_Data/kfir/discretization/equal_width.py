from discretization.decorators import prop_vals_only
from discretization.unsupervised import Unsupervised


class EqualWidth(Unsupervised):

    @staticmethod
    @prop_vals_only
    def equal_width(prop_df, nb_bins):
        min_value = prop_df.min()
        max_value = prop_df.max()
        diff = (max_value - min_value) / nb_bins
        cutpoints = [min_value + i * diff for i in range(1, nb_bins, 1)]
        cutpoints = sorted(list(set(cutpoints)))
        return cutpoints

    def generate_cutpoints(self, prop_df, nb_bins, *args, **kwargs):
        return EqualWidth.equal_width(prop_df, nb_bins)
