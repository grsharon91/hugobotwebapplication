from temporal_abstraction.discretization.decorators import prop_vals_only
from temporal_abstraction.discretization.unsupervised import Unsupervised


class EqualWidth(Unsupervised):

    @staticmethod
    @prop_vals_only
    def equal_width(prop_df, nb_bins):
        if prop_df.empty:
            return []
        min_value = prop_df.min()
        max_value = prop_df.max()
        diff = (max_value - min_value) / nb_bins
        cutpoints = [min_value + i * diff for i in range(1, nb_bins, 1)]
        cutpoints = sorted(list(set(cutpoints)))
        return cutpoints

    def _generate_cutpoints(self, prop_df):
        return EqualWidth.equal_width(prop_df, self._nb_bins)
