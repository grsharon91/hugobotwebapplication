class SupportingInstancesVector (object):
    def __init__(self, entities, h=False):
        self._supporting_entities = []
        self.supporting_instances = {}
        self.horizontal_support = 0
        self.h = h
        if not h:
            for i in range(entities):
                self.supporting_instances[i] = {}

    def add_entity(self, entity_index):
        if entity_index not in self._supporting_entities:
            self._supporting_entities.append(entity_index)

    def add_sti_to_sti_map_for_entity(self, entity_index, sti1, sti2):
        if self.h and entity_index not in self.supporting_instances:
            self.supporting_instances[entity_index] = {}
        if sti1 in self.supporting_instances[entity_index]:
            self.supporting_instances[entity_index][sti1].append(sti2)
        else:
            sti_list = [sti2]
            self.supporting_instances[entity_index][sti1] = sti_list
            self.add_entity(entity_index)
            self.horizontal_support += 1

    def get_stis_in_relation_with_key_sti_for_entity(self, entity_index, tis):
        if self.h and entity_index not in self.supporting_instances:
            return None
        if tis in self.supporting_instances[entity_index]:
            return self.supporting_instances[entity_index][tis]
        else:
            return None

    def get_supporting_entities(self):
        return self._supporting_entities

    def get_sti_maps_in_array_indexed_by_entity_id(self):
        return self.supporting_instances
