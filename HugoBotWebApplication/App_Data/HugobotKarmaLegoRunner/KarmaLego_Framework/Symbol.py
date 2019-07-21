class Symbol (object):
    def __init__(self, symbol, index):
        self.symbol = symbol
        self.symbol_index = index
        self._horizontal_support = 0
        self._supporting_instances = {}

    def add_interval_to_entity(self, entity_index, instance):
            if entity_index not in self._supporting_instances:
                str_lst = [instance]
                self._supporting_instances[entity_index] = str_lst
            else:
                if instance not in self._supporting_instances[entity_index]:
                    self._supporting_instances[entity_index].append(instance)
            self._horizontal_support += 1

    def get_symbol_vertical_support(self):
        return len(self._supporting_instances)

    def get_toncept_horizontal_dic(self):
        return self._supporting_instances

    def get_supporting_instances(self):
        return self._supporting_instances
