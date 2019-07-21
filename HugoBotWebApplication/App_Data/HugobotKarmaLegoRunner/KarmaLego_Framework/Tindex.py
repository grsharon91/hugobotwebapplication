from KarmaLego_Framework.TindexRelationEntry import TindexRelationEntry
from KarmaLego_Framework.SupportingInstancesVector import SupportingInstancesVector


class Tindex (object):
    def __init__(self):
        self.kindex = {}
        self.entities = 0
        self.rels = 0
        self.h = False

    def build_tindex(self, symbols, entities, rels, h=False):
        if not h:
            for i in range(symbols):
                row = {}
                for j in range(symbols):
                    row[j] = TindexRelationEntry(entities, rels)
                self.kindex[i] = row
        self.entities = entities
        self.h = h
        self.rels = rels

    def get_vertical_support_of_symbol_to_symbol_relation(self, first_index, second_index, rel):
        if self.h and (first_index not in self.kindex or second_index not in self.kindex[first_index] or
                       rel not in self.kindex[first_index][second_index].supporting_instances):
            return []
        return self.kindex[first_index][second_index].supporting_instances[rel].get_supporting_entities()

    def get_stis_in_relation_with_key_sti_for_entity_by_relation_and_symbols(self, first_index, second_index, rel,
                                                                             e_index, tis):
        if self.h and (first_index not in self.kindex or second_index not in self.kindex[first_index] or
                       rel not in self.kindex[first_index][second_index].supporting_instances):
            return None
        return self.kindex[first_index][second_index].supporting_instances[rel].\
            get_stis_in_relation_with_key_sti_for_entity(e_index, tis)

    def add_sti_to_tindex_relation_entry_by_symbols(self, first_toncept_index, second_toncept_index, rel, e_index,
                                                    tis_key, tis_val):
        if self.h:
            if first_toncept_index not in self.kindex:
                self.kindex[first_toncept_index] = {}
            if second_toncept_index not in self.kindex[first_toncept_index]:
                self.kindex[first_toncept_index][second_toncept_index] = TindexRelationEntry(self.entities, self.rels,
                                                                                             True)
        self.kindex[first_toncept_index][second_toncept_index].\
            add_sti_to_sti_map_for_relation_by_entity_id(rel, e_index, tis_key, tis_val)
