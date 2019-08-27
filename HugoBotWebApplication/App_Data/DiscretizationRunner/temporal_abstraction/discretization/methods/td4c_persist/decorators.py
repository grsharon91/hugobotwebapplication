from temporal_abstraction.discretization.methods.td4c_persist import candidate_selection


def make_facade(scoring_function):
    def scoring_function_as_facade(*args, **kwargs):
        return candidate_selection(scoring_function=scoring_function, *args, **kwargs)
    return scoring_function_as_facade
