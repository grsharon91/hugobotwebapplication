import os
from KarmaLego_Framework.LegoTree import LegoTreeNode
from KarmaLego_Framework.StiInstance import StiInstance
from KarmaLego_Framework.TIRP import TIRP
from KarmaLego_Framework.Karma import Karma


class Lego(object):
    def __init__(self, karma, incremental_output=False, path=None, max_tirp_length=10, need_one_sized=False):
        self._karma = karma
        self.frequent_tirps = []
        self._max_tirp_length = max_tirp_length
        self.tirps_tree_root = LegoTreeNode(None)
        self.path = path
        self.incremental_output = incremental_output
        self.need_one_sized = need_one_sized

    def fit(self, index_same=False, skip_followers=False):
        """
        creating two-sized tirps and send them to extend-tirp
        finally all frequent tirps are created
        :return: None
        """
        if self.incremental_output:
            try:
                os.remove(self.path)
            except OSError:
                pass
        index = 0
        for symbol1_id, symbol1 in self._karma.get_symbols_map().items():
            index += 1
            # print(str(index) + '\\' + str(len(self._karma.get_symbols_map())) + ', symbol: ' + symbol1_id)
            if self._karma.get_symbol_id_vertical_support(symbol1_id) < self._karma.get_min_vertical_support():
                continue
            if self.need_one_sized:
                one_sized_tirp = TIRP.get_one_sized_tirp(symbol1_id)
                self.add_instances_to_one_sized_tirp(one_sized_tirp)
                one_sized_tirp.set_mean_durations()
                if Karma.CALC_OFFSETS:
                    one_sized_tirp.set_mean_offsets(self._karma.entities_times)
                self.tirps_tree_root.add_node(one_sized_tirp)
                self.frequent_tirps.append(one_sized_tirp)
                if self.incremental_output:
                    one_sized_tirp.print_tirp(self.path, self._karma.get_entities_vector(), self._karma._num_relations,
                                              Karma.CALC_OFFSETS, self._karma.entities_times)
            for symbol2_id, symbol2 in self._karma.get_symbols_map().items():
                for rel in range(self._karma._num_relations):
                    if self._karma.get_vertical_support_of_sym_to_sym_rel(
                            symbol1.symbol_index, symbol2.symbol_index, rel) < \
                            self._karma.get_min_vertical_support():
                        continue
                    tirp = self._karma.get_two_sized_tirp_for_symbols_and_rel(symbol1_id, symbol2_id, rel)
                    if self.incremental_output:
                        tirp.print_tirp(self.path, self._karma.get_entities_vector(), self._karma._num_relations,
                                        Karma.CALC_OFFSETS, self._karma.entities_times)
                    root_node = self.tirps_tree_root
                    if self.need_one_sized:
                        root_node = LegoTreeNode(tirp)
                    root_node.add_node(self.extend_tirp(tirp, index_same, skip_followers))
        print('Lego fit complete')

    def add_instances_to_one_sized_tirp(self, tirp):
        sym = tirp._symbols[0]
        sup_insts = self._karma.get_symbols_map()[sym].get_supporting_instances()
        for entity_index, instances in sup_insts.items():
            for inst in instances:
                instance = StiInstance(set_first=inst, set_entity_index=entity_index,
                                       set_entity_id=self._karma.get_entities_vector()[entity_index])
                tirp.add_entity(entity_index, self._karma.get_entities_vector()[entity_index])
                tirp.supporting_instances.append(instance)
                tirp._supporting_sequences_by_entity[self._karma.get_entities_vector()[entity_index]]. \
                    append(instance)

    def print_one_symbol_tirp(self, sym_id):
        description = " "
        for entity_index, instances in self._karma.get_symbol_by_id(sym_id).get_toncept_horizontal_dic().items():
            for instance in instances:
                description += str(self._karma.get_entity_by_index(entity_index)) + " [" + str(instance._start_time) \
                               + "-" + str(instance._end_time) + "] "
        description = "1 " + str(sym_id) + "- -. " + str(self._karma.get_symbol_id_vertical_support(sym_id)) + " " + \
                      str(self._karma.get_symbol_id_vertical_support(sym_id)) + description
        with open(self.path, 'a') as output_file:
            output_file.write(description + "\n")

    def extend_tirp(self, tirp, index_same, skip_followers):
        """
         extending recursively the tirp and appending the frequent tirps to self.frequent_tirps
         :param tirp: TIRP, the tirp to extend
         :param index_same: Boolean, prevents multiple instances of same symbol in a tirp if true
         :param skip_followers: Boolean, prevents multiple instances of same var in a tirp if true
         :return: None
        """
        root_node = LegoTreeNode(tirp)
        self.frequent_tirps.append(tirp)
        for symbol_id, symbol in self._karma.get_symbols_map().items():
            if not index_same and symbol_id in tirp._symbols:
                continue
            for seed_relation in range(self._karma._num_relations):
                if (self._karma.get_vertical_support_of_sym_to_sym_rel(
                        self._karma.get_symbol_by_id(tirp._symbols[tirp.size - 1]).symbol_index, symbol.symbol_index,
                        seed_relation) >= self._karma.get_min_vertical_support()):
                    candidates = self.generate_candidates(tirp, seed_relation)
                    for candidate_relations in candidates:
                        new_tirp = self.extend_single_tirp(tirp, symbol_id, candidate_relations, skip_followers)
                        if len(new_tirp.supporting_entities) >= self._karma.get_min_vertical_support():
                            new_tirp._support_discovery = round(
                                len(new_tirp._supporting_sequences_by_entity) / len(self._karma._entities), 2)
                            if self.incremental_output:
                                new_tirp.print_tirp(self.path,
                                                    self._karma.get_entities_vector(), self._karma._num_relations,
                                                    Karma.CALC_OFFSETS, self._karma.entities_times)
                            if new_tirp.size < self._max_tirp_length:
                                root_node.add_node(self.extend_tirp(new_tirp, index_same, skip_followers))
        return root_node

    def generate_candidates(self, tirp, seed_relation):
        column_size = tirp.size
        top_cnd_rel_index = 0
        btm_rel_index = column_size - 2
        candidates_list = []
        candidate = []
        for i in(range(column_size)):
            candidate.append(i)
        candidate[column_size - 1] = seed_relation
        candidates_list.append(candidate)
        rng = list(range(top_cnd_rel_index, btm_rel_index + 1))
        rng.reverse()
        for rel_index_to_set in rng:
            left_tirp_index = int(((rel_index_to_set + 1) * rel_index_to_set / 2) + rel_index_to_set)
            below_cnd_index = rel_index_to_set + 1
            cand_list_size = len(candidates_list)
            for cand_index in range(cand_list_size):
                candidate = candidates_list[cand_index]
                transitivity_list = self._karma._relation_handler_obj.\
                    get_transitivity_list(tirp._tirp_matrix.get_relations()[left_tirp_index], candidate[below_cnd_index])
                for rel in transitivity_list:
                    if rel > transitivity_list[0]:
                        new_candidate = []
                        for i in (range(column_size)):
                            new_candidate.append(i)
                        tmp_rng = list(range(rel_index_to_set + 1, column_size))
                        tmp_rng.reverse()
                        for r_index in tmp_rng:
                            new_candidate[r_index] = candidate[r_index]
                        new_candidate[rel_index_to_set] = rel
                        candidates_list.append(new_candidate)
                    else:
                        candidate[rel_index_to_set] = rel
        return candidates_list

    def generate_candidates_previous(self, tirp, relation):
        """
        generate the relations candidates for the new symbol,new relation column in TirpMatrix
        :param tirp: TIRP, the base TIRP to extend
        :param relation: int, the relation between the new symbol and the last symbol in the tirp
        :return: candidates, list of int , the relations between the new symbol and the current symbols in the tirp
        """
        # TODO use symbol to minimize candidates by query karma if symbols and relation exist/relevant?
        # ans: we use only existing relations between the symbols
        candidates = self.generate_candidates_helper(tirp._tirp_matrix.get_all_direct_relations(),
                                                     relation, len(tirp._symbols) - 2)
        # adding the relation between the new symbol and the last symbol for each candidate
        for can in candidates:
            can.append(relation)
        return candidates

    def generate_candidates_helper(self, tirp_last_relation_column, first_relation, index):
        """
        generate a list of candidates relations for the new symbol without the relation between the new symbol and the
        last symbol in the tirp
        :param tirp_last_relation_column: list of int, the last relation column in the current TirpMatrix
        :param first_relation: int, the relation between the new symbol and previous symbol of the tirp, starts with the
        last symbol and ends with the first symbol
        :param index: int, the index of the current relation to check in the tirp_last_relation_column, starts with the
        last index and ends with the first
        :return: ans: list of candidates, each candidate is array of int
        """
        ans = []
        if index < 0:
            ans.append([])
            return ans
        transitivity_list = self._karma._relation_handler_obj.get_transitivity_list(tirp_last_relation_column[index],
                                                                                   first_relation)
        for relation in transitivity_list:
            results = self.generate_candidates_helper(tirp_last_relation_column, relation, (index - 1))
            for res in results:
                res.append(relation)
                ans.append(res)
        return ans

    def extend_single_tirp(self, tirp, new_symbol, new_relations, skip_followers):
        """
        Extends the pattern and then fills the supporting instances for the extended pattern
        :param tirp: TIRP, the current tirp to extend
        :param new_symbol: int, the new symbol to extend the tirp
        :param new_relations: the candidate relations for the tirp
        :param skip_followers: Boolean, prevents multiple instances of same var in a tirp if true
        :return: TIRP, the new extended tirp
        """
        new_tirp = tirp.extend_tirp(new_symbol, new_relations)
        top_rel_index = int((new_tirp.size - 1) * (new_tirp.size - 2) / 2)
        seed_rel_index = int(new_tirp.size * (new_tirp.size - 1) / 2 - 1)
        seed_relation = new_tirp._tirp_matrix.get_relations()[seed_rel_index]
        sym_last = new_tirp._symbols[-2]
        sym_new = new_tirp._symbols[-1]
        sym_last_index = self._karma.get_symbol_by_id(sym_last).symbol_index
        sym_new_index = self._karma.get_symbol_by_id(sym_new).symbol_index
        for i in range(len(tirp.supporting_instances)):
            tis_list = self._karma.get_stis_in_relation_with_key_sti_for_entity_by_relation_and_symbols(
                sym_last_index, sym_new_index, seed_relation, tirp.supporting_instances[i].entity_index,
                tirp.supporting_instances[i].sti[new_tirp.size - 2])
            if tis_list is None:
                continue
            for tis in tis_list:
                did_break = False
                for rel_index in range(top_rel_index, seed_rel_index):
                    second_tis = tirp.supporting_instances[i].sti[rel_index - top_rel_index]
                    if skip_followers and abs(float(tis._symbol) - float(second_tis._symbol)) == 1 and \
                            tis._var_id == second_tis._var_id:
                        did_break = True
                        break
                    found_rel = self._karma._relation_handler_obj.check_relation(
                            second_tis, tis, self._karma.get_epsilon(),
                            self._karma.get_max_gap())
                    expected_rel = new_tirp._tirp_matrix.get_relations()[rel_index]
                    if found_rel != expected_rel:
                        did_break = True
                        break
                if not did_break:
                    entity_index = tirp.supporting_instances[i].entity_index
                    new_instance = \
                        self.extend_instance(new_tirp.size,
                                             tirp.supporting_instances[i].sti, tis, entity_index,
                                             tirp.supporting_instances[i].start, tirp.supporting_instances[i].end)
                    new_tirp.add_entity(entity_index, self._karma.get_entities_vector()[entity_index])
                    new_tirp.supporting_instances.append(new_instance)
                    new_tirp._supporting_sequences_by_entity[self._karma.get_entities_vector()[entity_index]].\
                        append(new_instance)
        new_tirp.set_mean_durations()
        if Karma.CALC_OFFSETS:
            new_tirp.set_mean_offsets(self._karma.entities_times)
        return new_tirp

    def extend_instance(self, size, instance, last, entity_index, start, end):
        return StiInstance.extend_instance(size, instance, last, entity_index,
                                           self._karma.get_entities_vector()[entity_index], start, end)

    def print_frequent_tirps(self, path):
        """
        printing all the frequent TIRPs into a file
         :param path: the output path to print the TIRP
        :return: None - a file with the TIRPs
        """
        try:
            os.remove(path)
        except OSError:
            pass
        for tirp in self.frequent_tirps:
            tirp.print_tirp(path, self._karma.get_entities_vector(), self._karma._num_relations, Karma.CALC_OFFSETS,
                            self._karma.entities_times)
