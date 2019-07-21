from cli import cli
from constants import MethodsNames

# The input path should point to a dataset file
input_path = r'Datasets/FAGender/FAGender.csv'
# The output path should be a folder path
output_path = r'Datasets/FAGender'
name = 'some-name-for-this-run'  # this name will show up in all the files created by this run in the output folder
method = MethodsNames.TD4CCosine  # method name can be chosen from MethodNames class
nb_bins = 3
max_gap = 1


path_to_preprocessing_params_df = r'Datasets/FAGender/temporal_abstraction.csv'
path_to_temporal_abstraction_params_df = r'Datasets/FAGender/temporal_abstraction.csv'

# running discretization per-dataset of TD4C-cosine
cli(['temporal-abstraction', '-n', name, input_path, output_path, 'per-dataset', str(max_gap), 'discretization',
     method, str(nb_bins)])

# running discretization per-dataset of TD4C-cosine with K-Fold of 5 folds
cli(['temporal-abstraction', '-n', name, '--kfold', '5', input_path, output_path, 'per-dataset', str(max_gap),
     'discretization',
     method, str(nb_bins)])

# running knowledge-based discretization per-dataset
cli(['temporal-abstraction', '-n', name, input_path, output_path, 'per-dataset', str(max_gap),
     MethodsNames.KnowledgeBased, path_to_states_file])

""" Note: states are in angles (from -90 to 90) """

# running gradient using a states file
cli(['temporal-abstraction', '-n', name, input_path, output_path, 'per-dataset', str(max_gap),
     MethodsNames.Gradient, gradient_window_size, '--states-path', path_to_states_file])

# running gradient using a list of cutoffs
cli(['temporal-abstraction', '-n', name, input_path, output_path, 'per-dataset', str(max_gap),
     MethodsNames.Gradient, gradient_window_size, '--states-list', '1 2 3'])

# running discretization per-property
cli(['temporal-abstraction', '-n', name, input_path, output_path, 'per-property', path_to_preprocessing_params_df,
     path_to_temporal_abstraction_params_df])

"""  running discretization per-property with a states file (to be used
     by knowledge-based algorithms such as gradient and knowledge-based) """
cli(['temporal-abstraction', '-n', name, input_path, output_path, 'per-property', path_to_preprocessing_params_df,
     path_to_temporal_abstraction_params_df, '--states-file', path_to_states_file])

# running results-union
cli(['results-union', path_to_states_file_1, path_to_KL_file_1, path_to_states_file_2, path_to_KL_file_2,
     path_to_output_dir])
