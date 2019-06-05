import numpy as np

from discretization.decorators import prop_vals_only
from discretization.errors import DataTooDenseError
from discretization.unsupervised import Unsupervised


class EqualFrequency(Unsupervised):

    @staticmethod
    @prop_vals_only
    def equal_frequency(prop_values, nb_bins):
        sorted_prop_values = prop_values.sort_values()
        sorted_prop_values.reset_index(inplace=True, drop=True)

        step_size = len(sorted_prop_values) / nb_bins

        cutoffs = set()
        for i in range(1, nb_bins, 1):
            low_boundary_idx = int(i * step_size - 1)
            high_boundary_idx = int(i * step_size)
            low_boundary = sorted_prop_values[low_boundary_idx]
            high_boundary = sorted_prop_values[high_boundary_idx]

            cutoffs.add((low_boundary + high_boundary) / 2)

        if len(cutoffs) < nb_bins - 1:
            # raise DataTooDenseError(
            #     'EqualFrequency was requested to generate {} bins, but could only generate {} bins'.format(
            #         nb_bins,
            #         len(cutoffs) + 1
            #     ))
            print('ERROR: Data Too Dense')

        return sorted(cutoffs)

    def generate_cutpoints(self, prop_df, nb_bins, *args, **kwargs):
        return EqualFrequency.equal_frequency(prop_df, nb_bins)
