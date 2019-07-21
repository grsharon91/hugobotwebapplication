import operator
from KarmaLego_Framework.RelationHandler import RelationHandler
from Utils.parse import *
from KarmaLego_Framework.Symbol import Symbol
from KarmaLego_Framework.TIRP import TIRP
from KarmaLego_Framework.Tindex import Tindex
from KarmaLego_Framework.StiInstance import StiInstance


class Karma(object):
    CALC_OFFSETS = False

    def __init__(self, min_ver_support, epsilon=0, num_relations=7, max_gap=50, label=0, selected_variables=[]):
        self._var_to_symbols = {}
        self._epsilon = epsilon
        self._num_relations = num_relations
        self._relation_handler_obj = RelationHandler(num_relations)
        self._label = label
        self._symbolic_interval_start_point = 0
        self._min_ver_support = min_ver_support
        self._max_gap = max_gap
        self._entities_map = {}
        self._symbols_map = {}
        self._karma_index = Tindex()
        self._entities = []
        self.selected_variables=selected_variables
        self.entities_times = []
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
                            datefmt='%d-%m-%Y %H:%M:%S')
        self._logger = logging.getLogger('Karma')
        self._logger.setLevel(logging.INFO)

    def fit(self, file_path, num_comma=3, entity_ids_num=1, skip_followers=False, symbol_type='int', index_same=False,
            semicolon_end=False, calc_offsets=False):
        """
        :param file_path: string, the path to the symbolic time intervals file
        :param num_comma: int, number of commas per time interval representation in the input file
        :param skip_followers: boolean, decide if to skip 2 followers symbols (from the same temporal variable)
        :param symbol_type: String, type of symbols - int/str
        :param entity_ids_num: int, #Numers in the entity id lines of the file
        :param index_same: Boolean, index same symbols or not
        :param semicolon_end: Boolean, if intervals line end with a semicolon after the last interval
        :param calc_offsets: Boolean, if we should calc offsets
        :return:
        """
        self._logger.debug('start fit')
        Karma.CALC_OFFSETS = calc_offsets
        self.parse_kml_input(file_path, num_comma, symbol_type, entity_ids_num, semicolon_end)
        self._logger.debug('done loading file')
        self.build_karma_index(skip_followers, index_same)
        self._logger.debug('done building karma index')
        self._logger.debug('done fit')

    def parse_kml_input(self, file_path, num_comma, symbol_type, entity_ids_num, semicolon_end):
        self.parse_temporal_var_dict(file_path)
        self.parse_file_into_symbolic_time_intervals_parts(file_path, self._symbolic_interval_start_point, symbol_type,
                                                           num_comma, entity_ids_num, semicolon_end)
        self._min_ver_support = self._min_ver_support * len(self._entities_map)

    def parse_temporal_var_dict(self, file_path):
        """
        The function constructs the mapping from symbols to the symbols they belong to.
        It stores the mapping inside self object that will be later used to skip following symbols
        belonging to the same feature.
        NOTE: It seems to be used only for single KL. When running KL on a complete abstracted file it only discovers
        the line in the file in which the intervals begin
        :param file_path: string, the path to the symbolic time intervals file
        :return:
        """
        curr_row_index = 0
        self._var_to_symbols = {}
        var_id = ""
        with open(file_path, newline='') as f:
            next(f)
            curr_row_index += 1
            for raw_line in f:
                line = raw_line.rstrip().split(",")
                curr_row_index += 1
                if "numberOfEntities" not in line:
                    if line[len(line) - 1].isdigit():
                        var_id = line[0]
                    else:
                        symbol = line[2]
                        self._var_to_symbols[symbol] = []
                        self._var_to_symbols[symbol].append(var_id)
                else:
                    self._symbolic_interval_start_point = curr_row_index
                    break

    def parse_file_into_symbolic_time_intervals_parts(self, file_path, start_index, symbol_type, num_comma,
                                                      entity_ids_num, semicolon_end):
        """
        Parse the file to a map of entities with their symbolic time intervals
        Constructing also a structure of symbols wit their corresponding intervals
        :param file_path: string, the path to the symbolic time intervals file
        :param start_index: int, the row from which to parse the symbolic time intervals
        :param symbol_type: String, type of symbols - int/str
        :param num_comma: if the file format is (start_time, end_time,var_id,state) then num_comma=3
                      if (start_time, end_time,state,var_id) then num_comma == 2
                      if (start_time, end_time,state) then num_comma == 2
        :param entity_ids_num: int, #Numers in the entity id lines of the file
        :param semicolon_end: Boolean, if intervals line end with a semicolon after the last interval
        :return:
        """
        with open(file_path) as f:
            lines = f.readlines()[start_index:]
        for i in range(0, len(lines), 2):
            if entity_ids_num == 1:
                entity_id = lines[i].replace(";", "")
            else:
                entity_id = lines[i][0: lines[i].find(',')].replace(";", "")
            if Karma.CALC_OFFSETS:
                win_start = int(lines[i].split(';')[1])
                win_end = int(lines[i].split(';')[2])
                self.entities_times.append({'win_start': win_start, 'win_end': win_end})
            self._entities_map[entity_id] = []
            sym_ti_ls = lines[i + 1].split(";")
            intervals_list = sym_ti_ls[: -1] if semicolon_end else sym_ti_ls
            for sym_ti in intervals_list:
                sym_ti_obj, symbol = parser_of_sym_ti_row_for_different_formats(sym_ti, num_comma)
                if len(self.selected_variables) == 0:
                    self._entities_map[entity_id].append(sym_ti_obj)
                    if symbol not in self._symbols_map:
                        self._symbols_map[symbol] = Symbol(symbol, len(self._symbols_map))
                    self._symbols_map[symbol].add_interval_to_entity(len(self._entities_map) - 1, sym_ti_obj)
                elif sym_ti_obj._var_id in self.selected_variables:
                    self._entities_map[entity_id].append(sym_ti_obj)
                    if symbol not in self._symbols_map:
                        self._symbols_map[symbol] = Symbol(symbol, len(self._symbols_map))
                    self._symbols_map[symbol].add_interval_to_entity(len(self._entities_map) - 1, sym_ti_obj)
        if symbol_type == 'int':
            for entity_id in self._entities_map:
                self._entities_map[entity_id].sort(key=Karma.sort_str_int)
        else:
            for entity_id in self._entities_map:
                self._entities_map[entity_id].sort(key=operator.attrgetter('start_time', 'end_time', 'symbol'))

    @staticmethod
    def sort_str_int(x):
        return x._start_time, x._end_time, float(x._symbol)

    def get_entities_map(self):
        return self._entities_map

    def get_entities_vector(self):
        return self._entities

    def get_symbols_map(self):
        return self._symbols_map

    def get_min_vertical_support(self):
        return self._min_ver_support

    def get_symbol_id_vertical_support(self, symbol_id):
        return len(self._symbols_map[symbol_id].get_toncept_horizontal_dic())

    def get_vertical_support_of_sym_to_sym_rel(self, sym1_index, sym2_index, rel):
        return len(self._karma_index.get_vertical_support_of_symbol_to_symbol_relation(sym1_index, sym2_index, rel))

    def get_symbol_by_id(self, symbol_id):
        return self._symbols_map[symbol_id]

    def get_entity_by_index(self, entity_index):
        return self._entities[entity_index]

    def get_stis_in_relation_with_key_sti_for_entity_by_relation_and_symbols(self, first_index, second_index, rel,
                                                                             entity_index, tis):
        return self._karma_index\
            .get_stis_in_relation_with_key_sti_for_entity_by_relation_and_symbols(first_index,
                                                                                  second_index, rel, entity_index, tis)

    def get_label(self):
        return self._label

    def get_max_gap(self):
        return self._max_gap

    def get_epsilon(self):
        return self._epsilon

    def add_symbol(self, entity_index, tis):
        if tis._symbol not in self._symbols_map:
            self._symbols_map[tis._symbol] = Symbol(tis._symbol, len(self._symbols_map))
        self._symbols_map[tis._symbol].add_interval_to_entity(entity_index, tis)

    def build_karma_index(self, skip_followers, index_same):
        """
        Build the Karma symbols index.
        :param skip_followers: bool, decide if to skip 2 followers symbols (from the same temporal variable)
        :param index_same: Boolean, index same symbols or not
        :return:
        """
        for entity_id in self._entities_map.keys():
            self._entities.append(entity_id)
        self._karma_index.build_tindex(len(self._symbols_map), len(self._entities_map), self._num_relations, True)
        for entity_index in range(len(self._entities)):
            tis_list = self._entities_map[self._entities[entity_index]]
            for ti1_index in range(len(tis_list)):
                first_tis = tis_list[ti1_index]
                self.add_symbol(entity_index, first_tis)
                for ti2_index in range(ti1_index + 1, len(tis_list)):
                    second_tis = tis_list[ti2_index]
                    if not index_same and first_tis._symbol == second_tis._symbol:
                        continue
                    if skip_followers and abs(float(first_tis._symbol) - float(second_tis._symbol)) == 1 and \
                            first_tis._var_id == second_tis._var_id:
                        continue
                    self.add_symbol(entity_index, second_tis)
                    relation = self._relation_handler_obj.check_relation(first_tis, second_tis, self._epsilon,
                                                                        self._max_gap)
                    if relation != RelationHandler.RELATION_NOT_DEFINED:
                        index1 = self._symbols_map[first_tis._symbol].symbol_index
                        index2 = self._symbols_map[second_tis._symbol].symbol_index
                        self._karma_index.\
                            add_sti_to_tindex_relation_entry_by_symbols(index1, index2,
                                                                        relation, entity_index, first_tis, second_tis)
                    else:
                        break

    def get_two_sized_tirp_for_symbols_and_rel(self, first_id, second_id, rel):
            two_sized_tirp = TIRP(first_id, second_id, rel)
            index1 = self._symbols_map[first_id].symbol_index
            index2 = self._symbols_map[second_id].symbol_index
            ti_list_dics_vec = self._karma_index.kindex[index1][index2].\
                get_sti_maps_in_array_indexed_by_entity_id_for_relation(rel)
            entities = ti_list_dics_vec.keys() if type(ti_list_dics_vec) is dict \
                else range(len(ti_list_dics_vec))
            for entity_index in entities:
                ti_list_ti_dic = ti_list_dics_vec[entity_index]
                for ti_list_ti_key, ti_list_ti_value in ti_list_ti_dic.items():
                    for tis in ti_list_ti_value:
                        sti = SymbolicTimeInterval(ti_list_ti_key._start_time, ti_list_ti_key._end_time,
                                                   ti_list_ti_key._symbol, ti_list_ti_key._var_id)
                        two_sized_tirp.add_entity(entity_index, self._entities[entity_index])
                        new_stii = StiInstance(sti, tis, entity_index, self._entities[entity_index])
                        two_sized_tirp._supporting_sequences_by_entity[self._entities[entity_index]].append(new_stii)
                        two_sized_tirp.supporting_instances.append(new_stii)
                        two_sized_tirp._mean_horizontal_support += 1
            two_sized_tirp._support_discovery = round(
                            len(two_sized_tirp._supporting_sequences_by_entity) / len(self._entities), 2)
            two_sized_tirp.set_mean_durations()
            if Karma.CALC_OFFSETS:
                two_sized_tirp.set_mean_offsets(self.entities_times)
            return two_sized_tirp
