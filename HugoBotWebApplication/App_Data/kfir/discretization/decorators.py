import pandas as pd
import numpy as np


def prop_vals_only(foo):
    def new_foo(prop_values, *args, **kwargs):
        prop_values = prop_values.TemporalPropertyValue
        return foo(prop_values,
                   *args,
                   **kwargs)
    return new_foo
