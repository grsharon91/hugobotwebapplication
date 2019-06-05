import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import numpy as np
from preprocessing.paa import paa


class TestPAA(unittest.TestCase):

    def setUp(self):
        pass

    def test_uniform_values(self):
        window_size = 5
        nb_values = 100
        df_values = {
            'TemporalPropertyID': np.repeat([1], nb_values),
            'TimeStamp': np.arange(0, nb_values, 1),
            'TemporalPropertyValue': np.full(nb_values, 1)
        }
        df = pd.DataFrame.from_dict(df_values)
        paa(df, window_size)
        expected_df_values = {
            'TemporalPropertyID': np.repeat([1], nb_values),
            'TimeStamp': np.arange(0, nb_values, 1),
            'TemporalPropertyValue': np.full(nb_values, 1)
        }
        expected_df = pd.DataFrame.from_dict(expected_df_values)
        assert_frame_equal(expected_df, df)

    def test_uniform_average(self):
        window_size = 5
        nb_values = 100
        arr = np.array([i for i in range(5)])
        df_values = {
            'TemporalPropertyID': np.repeat([1], nb_values),
            'TimeStamp': np.arange(0, nb_values, 1),
            'TemporalPropertyValue': np.tile(arr, int(nb_values / len(arr)))
        }
        df = pd.DataFrame.from_dict(df_values)
        paa(df, window_size)
        expected_df_values = {
            'TemporalPropertyID': np.repeat([1], nb_values),
            'TimeStamp': np.arange(0, nb_values, 1),
            'TemporalPropertyValue': np.tile(np.average(arr), nb_values)
        }
        expected_df = pd.DataFrame.from_dict(expected_df_values)
        assert_frame_equal(expected_df, df, check_dtype=False)

    def test_uniform_average_with_remainder(self):
        window_size = 3
        nb_values = 100
        arr = np.array([i for i in range(3)])
        df_values = {
            'TemporalPropertyID': np.repeat([1], nb_values),
            'TimeStamp': np.arange(0, nb_values, 1),
            'TemporalPropertyValue': np.concatenate((np.tile(np.average(arr), 99), np.array([0])))
        }
        df = pd.DataFrame.from_dict(df_values)
        paa(df, window_size)
        expected_df_values = {
            'TemporalPropertyID': np.repeat([1], nb_values),
            'TimeStamp': np.arange(0, nb_values, 1),
            'TemporalPropertyValue': np.concatenate((np.tile(np.average(arr), 99), np.array([0])))
        }
        expected_df = pd.DataFrame.from_dict(expected_df_values)
        assert_frame_equal(expected_df, df, check_dtype=False)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
