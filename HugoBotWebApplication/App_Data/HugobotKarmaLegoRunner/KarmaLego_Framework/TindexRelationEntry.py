from KarmaLego_Framework.SupportingInstancesVector import SupportingInstancesVector


class TindexRelationEntry (object):
    def __init__(self, entities, relations, h=False):
        self._entities = entities
        self.supporting_instances = {}
        self.h = h
        if not h:
            for i in range(relations):
                self.supporting_instances[i] = SupportingInstancesVector(entities)

    def get_sti_maps_in_array_indexed_by_entity_id_for_relation(self, rel):
        return self.supporting_instances[rel].get_sti_maps_in_array_indexed_by_entity_id()

    def add_sti_to_sti_map_for_relation_by_entity_id(self, rel, e_index, tis_key, tis_val):
        if self.h and rel not in self.supporting_instances:
            self.supporting_instances[rel] = SupportingInstancesVector(self._entities, self.h)
        self.supporting_instances[rel].add_sti_to_sti_map_for_entity(e_index, tis_key, tis_val)
