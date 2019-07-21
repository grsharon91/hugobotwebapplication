from KarmaLego_Framework.Karma import Karma
from KarmaLego_Framework.Lego import Lego
import time


def runKarmaLego(time_intervals_path, min_ver_support, num_relations, max_gap, label, epsilon, output_path=None,
                 incremental_output=False, max_tirp_length=10, num_comma=2, symbol_type='int',
                 skip_followers=False, entity_ids_num=1, index_same=False, semicolon_end=False, need_one_sized=False,
                 selected_variables=[], calc_offsets=False):
    """
    this method runs  the process of KarmaLego with all relevant inputs
    :param epsilon:
    :param time_intervals_path: String, the time intervals file
    :param min_ver_support: float, the minimum vertical support value
    :param num_relations: int, number of relations
    :param max_gap: int, the max_gap between the intervals for creating the index
    :param label: int, class label
    :param output_path: String, the output file
    :param incremental_output: Boolean, whether to print the output incrementally or not
    :param max_tirp_length: int, maximal length of tirp to discover
    :param num_comma: int, number of commas per time interval representation in the input file
    :param symbol_type: String, type of symbols - int/str
    :param skip_followers: Boolean, whether to skip followers or not
    :param entity_ids_num: int, #Numers in the entity id lines of the file
    :param index_same: Boolean, index same symbols or not
    :param semicolon_end: Boolean, if intervals line end with a semicolon after the last interval
    :param selected_variables: list, list of properties to use
    :param need_one_sized: Boolean, if we need to add the 1 sized tirps to the structure
    :param calc_offsets: Boolean, if we need to calculate offsets
    :return: lego and karma structs
    """
    st = time.time()
    karma = Karma(min_ver_support=min_ver_support, num_relations=num_relations, max_gap=max_gap, label=label,
                  selected_variables=selected_variables, epsilon=epsilon)
    karma.fit(file_path=time_intervals_path, num_comma=num_comma, index_same=index_same,
              skip_followers=skip_followers, symbol_type=symbol_type, entity_ids_num=entity_ids_num,
              semicolon_end=semicolon_end, calc_offsets=calc_offsets)
    lego = Lego(karma=karma, incremental_output=incremental_output, path=output_path, max_tirp_length=max_tirp_length,
                need_one_sized=need_one_sized)
    lego.fit(index_same=index_same, skip_followers=skip_followers)
    fin = time.time() - st
    return lego, karma

#
# start_time = time.time()
# print(time.time() - start_time)
# support_vec = 0.5
# num_relations = 3
# max_gap = 30
# path = '../KarmaLego_TestsData/ASL.txt'
# out_path = 'KL_Output.txt'
# print_output_incrementally = True
# entity_ids_num = 2
# index_same = True
# semicolon_end = True
# need_one_sized = True
# lego_0, karma_0 = runKarmaLego(time_intervals_path=path, output_path=out_path, index_same=index_same,
#                                incremental_output=print_output_incrementally, min_ver_support=support_vec,
#                                num_relations=num_relations, skip_followers=False, max_gap=max_gap, label=0,
#                                max_tirp_length=15, num_comma=2, entity_ids_num=entity_ids_num,
#                                semicolon_end=semicolon_end, need_one_sized=need_one_sized)
# if not print_output_incrementally:
#     lego_0.print_frequent_tirps(out_path)
# total_time = time.time() - start_time
# print(total_time)
