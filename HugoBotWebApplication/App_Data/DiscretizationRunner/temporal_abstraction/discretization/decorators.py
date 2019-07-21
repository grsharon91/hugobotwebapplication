from constants import DatasetColumns


def prop_vals_only(foo):
    def new_foo(prop_values, *args, **kwargs):
        prop_values = prop_values[DatasetColumns.TemporalPropertyValue]
        return foo(prop_values,
                   *args,
                   **kwargs)
    return new_foo
