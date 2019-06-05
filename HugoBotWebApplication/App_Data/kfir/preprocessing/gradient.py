from preprocessing.transformation import Transformation
import numpy as np
from tqdm import tqdm


class Gradient(Transformation):

    # @staticmethod
    # def derivative(df, step_size=1):
    #     idx = df.TimeStamp.argsort().values
    #     v = df.TemporalPropertyValue.iloc[idx].values
    #     t = df.TimeStamp.iloc[idx].values
    #
    #     def calc_step_diffs(arr):
    #         return np.diff(arr.reshape(-1, step_size), axis=0).reshape(-1)
    #
    #     def prefix_diffs(arr):
    #         return arr[:step_size] - arr[0]
    #
    #     pv = prefix_diffs(v)
    #     pt = prefix_diffs(t)
    #     pt[0] = 1  # just so we don't divide 0 by 0
    #
    #     tans = np.append(pv / pt, calc_step_diffs(v) / calc_step_diffs(t))
    #     df.TemporalPropertyValue.iloc[idx] = np.degrees(np.arctan(tans))
    #     return df
    #
    # def transform(self, df):
    #     df = df.groupby(by=['EntityID', 'TemporalPropertyID']).apply(Gradient.derivative)
    #     return df

    @staticmethod
    def derivative(df, window_size=1):
        df.sort_values(by='TimeStamp')

        def calc_derivative_of_sample(sample):
            samples_in_window = df[
                (df.TimeStamp <= sample.TimeStamp) &
                (df.TimeStamp >= sample.TimeStamp - window_size)
            ]

            y = samples_in_window.TemporalPropertyValue.values
            x = samples_in_window.TimeStamp.values
            nb_points = np.size(y)

            mean_x, mean_y = np.mean(x), np.mean(y)

            ss_xy = np.sum(x * y) - mean_x * sum(y) - mean_y * sum(x) + nb_points * mean_x * mean_y
            ss_xx = np.sum(x * x) - 2 * mean_x * np.sum(x) + nb_points * mean_x * mean_x

            if ss_xx != 0:
                b_1 = ss_xy / ss_xx
                return np.degrees(np.arctan(b_1))
            else:
                return

        df.TemporalPropertyValue = df.apply(calc_derivative_of_sample, axis=1)
        return df

    def transform(self, df, *args, **kwargs):
        print('performing gradient...')
        tqdm.pandas()
        df = df.groupby(by=['EntityID', 'TemporalPropertyID']).\
            progress_apply(Gradient.derivative, *args, **kwargs).dropna()
        return df
