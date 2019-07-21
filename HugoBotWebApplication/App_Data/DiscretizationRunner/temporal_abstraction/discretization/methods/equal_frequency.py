from sys import stderr

from constants import DatasetColumns
from temporal_abstraction.discretization.decorators import prop_vals_only
from temporal_abstraction.discretization.errors import DataTooDenseError
from temporal_abstraction.discretization.unsupervised import Unsupervised


class EqualFrequency(Unsupervised):
    """
        This method contains two approaches:
        #1: Sort the samples, and discretize according to indexes. In case there are too many samples with the same
            value, the number of bins created is smaller than the one requested. In this case we go to approach #2.
        #2: We look at unique values frequencies, and we add to the bin that is being
            created one unique value at a time. When the amount of samples reached the bin-size which was calculated
            in advance, we re-calculate the amount of samples for each bin according
            the (remaining samples / remaining bins), and only then go to the next bin.
            This allows us to create the requested amount of bins.
    """

    @staticmethod
    @prop_vals_only
    def equal_frequency_precise(prop_values, nb_bins):
        sorted_prop_values = prop_values.sort_values()
        sorted_prop_values.reset_index(inplace=True, drop=True)

        step_size = len(sorted_prop_values) / nb_bins

        if step_size == 0:
            return sorted_prop_values

        cutoffs = set()
        for i in range(1, nb_bins, 1):
            low_boundary_idx = int(i * step_size - 1)
            high_boundary_idx = int(i * step_size)
            low_boundary = sorted_prop_values[low_boundary_idx]
            high_boundary = sorted_prop_values[high_boundary_idx]

            # We add as a cutoff the average between the samples, so that there will be some kind of margin to the bin
            cutoffs.add((low_boundary + high_boundary) / 2)

        if len(cutoffs) < nb_bins - 1:
            raise DataTooDenseError(
                'EqualFrequency was requested to generate {} bins, but could only generate {} bins'.format(
                    nb_bins,
                    len(cutoffs) + 1
                ))

        return sorted(cutoffs)

    @staticmethod
    @prop_vals_only
    def equal_frequency_flexible(prop_values, nb_bins):
        counts = prop_values.value_counts().sort_index()
        values = counts.index

        data_size_left = len(prop_values)
        nb_bins_left = nb_bins
        vals_per_bin = int(data_size_left / nb_bins_left)

        if len(values) == 1:
            cutoffs = [values[0]]
        else:
            cutoffs = list()
            cumulative_count = 0
            for val, count, val_next in zip(values, counts, values[1:]):
                if nb_bins_left == 1:
                    break

                cumulative_count += count

                if cumulative_count >= vals_per_bin:
                    cutoffs.append((val + val_next) / 2)

                    data_size_left -= cumulative_count
                    nb_bins_left -= 1
                    vals_per_bin = int(data_size_left / nb_bins_left)
                    cumulative_count = 0

        return cutoffs

    def _generate_cutpoints(self, prop_df):
        try:
            return EqualFrequency.equal_frequency_precise(prop_df, self._nb_bins)
        except DataTooDenseError as e:
            prop_id = prop_df[DatasetColumns.TemporalPropertyID].values[0]
            print(f'warning in property #{prop_id}: {e}; changing to flexible version', file=stderr)
            return EqualFrequency.equal_frequency_flexible(prop_df, self._nb_bins)
