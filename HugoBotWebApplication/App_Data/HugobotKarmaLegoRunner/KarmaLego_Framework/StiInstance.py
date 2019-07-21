class StiInstance (object):
    def __init__(self, set_first=None, set_second=None, set_entity_index=None, set_entity_id=None):
        if set_first is not None:
            self.entity_index = set_entity_index
            self.entity_id = set_entity_id
            self.sti = [set_first]
            self.start = set_first._start_time
            self.end = set_first._end_time
            if set_second is not None:
                self.sti.append(set_second)
                self.start = min(self.start, set_second._start_time)
                self.end = max(self.end, set_second._end_time)

    @staticmethod
    def extend_instance(size, sti_vec, last_tis, set_entity_index, set_entity_id, start, end):
        stii = StiInstance()
        stii.entity_index = set_entity_index
        stii.entity_id = set_entity_id
        stii.sti = []
        for i in range(size - 1):
            stii.sti.append(sti_vec[i])
        stii.sti.append(last_tis)
        stii.start = start
        stii.end = end
        stii.start = min(stii.start, last_tis._start_time)
        stii.end = max(stii.end, last_tis._end_time)
        return stii

    def get_duration(self):
        return self.end - self.start

    def get_offset_from_start(self, entities_times):
        return self.start - entities_times[self.entity_index]['win_start']

    def get_offset_until_end(self, entities_times):
        return entities_times[self.entity_index]['win_end'] - self.end
