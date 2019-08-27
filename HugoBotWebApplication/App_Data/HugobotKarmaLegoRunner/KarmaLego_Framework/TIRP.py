from copy import copy, deepcopy
from KarmaLego_Framework.TirpMatrix import TirpMatrix
from KarmaLego_Framework.RelationHandler import RelationHandler
import itertools
import numpy as np


class TIRP (object):
    def __init__(self, first_symbol=None, second_symbol=None, relation=None, label=0):
        if first_symbol is not None and second_symbol is not None and relation is not None:
            self.size = 2
            self._symbols = [first_symbol, second_symbol]
            self._tirp_matrix = TirpMatrix(relation)
        else:
            self.size = 0
            self._symbols = []
            self._tirp_matrix = {}
        self.supporting_instances = []
        self.supporting_entities = []
        self._supporting_sequences_by_entity = {}
        self._label = label
        self._name = ""
        self._both_class = ""
        self._support_discovery = 0.0
        self._mean_horizontal_support = 0
        self.mean_durations = []
        self.mean_offsets = []
        self.mean_duration = 0
        self.mean_start_offset = 0
        self.mean_end_offset = 0
        self._Artemis_by_entity = {}

    def extend_tirp(self, new_symbol, new_relations):
        new_tirp = self.copy_tirp()
        new_tirp._symbols.append(new_symbol)
        new_tirp._tirp_matrix.extend(new_relations)
        new_tirp.size = self.size + 1
        return new_tirp

    @staticmethod
    def get_one_sized_tirp(new_symbol):
        new_tirp = TIRP()
        new_tirp._symbols = [new_symbol]
        new_tirp._tirp_matrix = TirpMatrix()
        new_tirp.size = 1
        return new_tirp

    def add_entity(self, entity_index, entity_id):
        if entity_index not in self.supporting_entities:
            self.supporting_entities.append(entity_index)
            self._supporting_sequences_by_entity[entity_id] = []

    def get_vertical_support(self):
        return len(self.supporting_entities)

    def copy_tirp(self):
        """
        create new tirp and copy without instances
        :return: TIRP,copy of this tirp
        """
        new_tirp = TIRP()
        new_tirp.size = self.size
        new_tirp._symbols = copy(self._symbols)
        new_tirp._label = self._label
        new_tirp._tirp_matrix = self._tirp_matrix.copy()
        return new_tirp

    def copy(self):
        """
        create new tirp and copy all current variables
        :return: TIRP,copy of this tirp
        """
        new_tirp = TIRP()
        new_tirp.size = self.size
        new_tirp._symbols = copy(self._symbols)
        new_tirp._label = self._label
        new_tirp._tirp_matrix = self._tirp_matrix.copy()
        new_tirp.mean_duration = self.mean_duration
        new_tirp.mean_start_offset = self.mean_start_offset
        new_tirp.mean_end_offset = self.mean_end_offset
        new_tirp.mean_durations = copy(self.mean_durations)
        new_tirp.mean_offsets = copy(self.mean_offsets)
        new_tirp.supporting_entities = self.supporting_entities.copy()
        new_tirp.supporting_instances = deepcopy(self.supporting_instances)
        for entity_id in self._supporting_sequences_by_entity.keys():
            new_tirp._supporting_sequences_by_entity[entity_id] = \
                deepcopy(self._supporting_sequences_by_entity[entity_id])
        for entity_id in self._Artemis_by_entity.keys():
            new_tirp._Artemis_by_entity[entity_id] = deepcopy(self._Artemis_by_entity[entity_id])
        return new_tirp

    def hollow_copy(self):
        """
        create new tirp and copy all current variables
        :return: TIRP,copy of this tirp
        """
        new_tirp = TIRP()
        new_tirp._symbols = copy(self._symbols)
        new_tirp._label = self._label
        new_tirp._name = self._name
        new_tirp._tirp_matrix = self._tirp_matrix.copy()
        new_tirp._both_class = self._both_class
        new_tirp._support_discovery = self._support_discovery
        new_tirp._mean_horizontal_support = self._mean_horizontal_support
        new_tirp.mean_duration = self.mean_duration
        new_tirp.mean_start_offset = self.mean_start_offset
        new_tirp.mean_end_offset = self.mean_end_offset
        new_tirp.mean_durations = copy(self.mean_durations)
        new_tirp.mean_offsets = copy(self.mean_offsets)
        return new_tirp

    def get_last_symbol(self):
        """
        returns the last symbol of the tirp
        :return:int, last symbol
        """
        return self._symbols[-1]

    def set_mean_durations(self):
        for entity_index in self.supporting_entities:
            instances = [sti_inst for sti_inst in self.supporting_instances if sti_inst.entity_index ==
                         entity_index]
            duration_list = []
            for i, instance in enumerate(instances):
                duration = instance.get_duration()
                duration_list.append(duration)
            mean_duration = sum(duration_list) / len(duration_list)
            self.mean_durations.append(mean_duration)
        self.mean_duration = np.mean(self.mean_durations)

    def set_mean_offsets(self, entities_times):
        for entity_index in self.supporting_entities:
            instances = [sti_inst for sti_inst in self.supporting_instances if sti_inst.entity_index ==
                         entity_index]
            start_offsets_list = []
            end_offsets_list = []
            for i, instance in enumerate(instances):
                start_offset = instance.get_offset_from_start(entities_times)
                end_offset = instance.get_offset_until_end(entities_times)
                start_offsets_list.append(start_offset)
                end_offsets_list.append(end_offset)
            mean_start_offset = sum(start_offsets_list) / len(start_offsets_list)
            mean_end_offset = sum(end_offsets_list) / len(end_offsets_list)
            self.mean_offsets.append({'start_offset': mean_start_offset, 'end_offset': mean_end_offset})
        self.mean_start_offset = np.mean([mofs['start_offset'] for mofs in self.mean_offsets])
        self.mean_end_offset = np.mean([mofs['end_offset'] for mofs in self.mean_offsets])

    def get_mean_mean_duration(self):
        mean_duration_list = []
        for entity in self.supporting_entities:
            instances = [sti_inst.sti for sti_inst in self.supporting_instances if sti_inst.entity_index == entity]
            start_list = []
            end_list = []
            duration_list = []
            for i, instance in enumerate(instances):
                start_list.extend([x.getStartTime() for x in instance])
                end_list.extend([x.getEndTime() for x in instance])
                min_start_time = min(start_list)
                max_end_time = max(end_list)
                duration = max_end_time - min_start_time
                duration_list.append(duration)
                start_list = []
                end_list = []
            mean_duration = sum(duration_list) / len(duration_list)
            mean_duration_list.append(mean_duration)
        return np.mean(mean_duration_list)

    def calculate_mean_horizontal_support(self):
        """
        calculate the average horizontal support between all the supporting instances
        :return: double - the mean horizontal support value
        """
        if len(self._symbols) == 1:
            return len(self.supporting_entities)
        num_of_entities = len(self.supporting_entities)
        num_of_instances = len(self.supporting_instances)
        mean_horizontal_support = num_of_instances / num_of_entities
        # mean_horizontal_support = round(mean_horizontal_support, 14)
        # if mean_horizontal_support == int(mean_horizontal_support):
        #     mean_horizontal_support = int(mean_horizontal_support)
        self._mean_horizontal_support = mean_horizontal_support
        return mean_horizontal_support

    def print_tirp(self, path, entities_vector, num_relations, extended_putput=False, entities_times=None):
        """
        printing the TIRP into a file
        :param path: the output path to print the TIRP
        :param entities_vector: list of entities
        :param num_relations: number of relations used in the mining process
        :param extended_putput: print also mean durations and mean offsets
        :param entities_times: start and end window times per entity
        :return: None - a file with the TIRPs
        """
        rel_object = RelationHandler(num_relations)
        tirp_string = str(len(self._symbols))
        tirp_string = tirp_string + " "
        for sym in self._symbols:
            tirp_string = tirp_string + str(sym) + "-"
        tirp_string = tirp_string + " "
        for rel in self._tirp_matrix.get_relations():
            tirp_string = tirp_string + rel_object.get_short_description(rel) + "."
        tirp_string = tirp_string + " "
        if extended_putput:
            tirp_string = tirp_string + str(self.mean_duration) + " "
            tirp_string = tirp_string + str(self.mean_start_offset) + " "
            tirp_string = tirp_string + str(self.mean_end_offset) + " "
        tirp_string = tirp_string + str(len(self.supporting_entities)) + " "
        tirp_string = tirp_string + str(self.calculate_mean_horizontal_support()) + " "
        for i in range(len(self.supporting_instances)):
            tirp_string = tirp_string + str(entities_vector[self.supporting_instances[i].entity_index]) + " "
            for ti in range(self.size):
                tirp_string = tirp_string + "[" + str(self.supporting_instances[i].sti[ti]._start_time) + "-" + \
                              str(self.supporting_instances[i].sti[ti]._end_time) + "]"
            if extended_putput:
                tirp_string += " " + str(self.supporting_instances[i].get_duration()) + " "
                tirp_string += str(self.supporting_instances[i].get_offset_from_start(entities_times)) + " "
                tirp_string += str(self.supporting_instances[i].get_offset_until_end(entities_times))
            tirp_string = tirp_string + " "
        with open(path, 'a') as output_file:
            output_file.write(tirp_string + "\n")
            if extended_putput:
                tirp_extended_string = ""
                i = 0
                for entity_index in self.supporting_entities:
                    tirp_extended_string += str(entities_vector[entity_index]) + ", "
                    tirp_extended_string += "[" + str(entities_times[entity_index]['win_start']) + ", " + \
                                            str(entities_times[entity_index]['win_end']) + "]: "
                    tirp_extended_string += str(self.mean_durations[i]) + " "
                    tirp_extended_string += str(self.mean_offsets[i]['start_offset']) + " "
                    tirp_extended_string += str(self.mean_offsets[i]['end_offset']) + ", "
                    i += 1
                tirp_extended_string = tirp_extended_string[: -2]
                output_file.write(tirp_extended_string + "\n")

    def get_tirp_name(self, num_relations):
        rel_object = RelationHandler(num_relations)
        if len(self._symbols) == 1:
            return str(self._symbols[0])
        rel = 0
        name = ''
        for i, j in itertools.combinations(self._symbols, 2):
            name = name + str(i) + rel_object.get_short_description(self._tirp_matrix.get_relations()[rel]) + \
                   str(j) + '_'
            rel = rel + 1
        name = name[:-1]
        self._name = name
        return name

    def get_tirp_name_and_vertical_s(self, num_relations):
        rel_object = RelationHandler(num_relations)
        if len(self._symbols) == 1:
            return str(self._symbols[0])
        rel = 0
        name = ''
        for i, j in itertools.combinations(self._symbols, 2):
            name = name + str(i) + rel_object.get_short_description(self._tirp_matrix.get_relations()[rel]) + \
                   str(j) + '_'
            rel = rel + 1
        name = name[:-1]
        name = name + "support: " + str(len(self.supporting_entities))
        self._name = name
        return name

    def get_tirp_name_and_both_class(self, num_relations):
        rel_object = RelationHandler(num_relations)
        if len(self._symbols) == 1:
            return str(self._symbols[0])
        rel = 0
        name = ''
        for i, j in itertools.combinations(self._symbols, 2):
            name = name + str(i) + rel_object.get_short_description(self._tirp_matrix.get_relations()[rel]) + \
                   str(j) + '_'
            rel = rel + 1
        name = name[:-1]
        name = name + "both_class: " + self._both_class
        self._name = name
        return name

    def to_string(self):
        ans = ''
        for symbol in self._symbols:
            ans += str(symbol) + '_'
        ans += self._tirp_matrix.to_string()
        return ans
