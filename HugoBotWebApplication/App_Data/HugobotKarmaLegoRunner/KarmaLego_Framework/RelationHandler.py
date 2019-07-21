

class AllenSevenRelationEngine(object):
    """
        Engine to handle all 7 Allen`s relations.
        the order of the relations is critical for transitivity table creation, do not change!!!
        implementation based on:
        https://www.ics.uci.edu/~alspaugh/cls/shr/allen.html
    """
    NOT_DEFINED_DESCRIPTION = 'NOT DEFINED'
    NOT_DEFINED = -1
    BEFORE = 0
    MEET = 1
    OVERLAP = 2
    FINISHBY = 3
    CONTAIN = 4
    STARTS = 5
    EQUAL = 6
    RELATION_CHARS = ['p', 'm', 'o', 'F', 'D', 's', 'e']
    RELATION_CHARS_FRESKA = ['<', 'm', 'o', 'f', 'c', 's', '=']
    RELATION_FULL_DESCRIPTION = ['BEFORE', 'MEETS', 'OVERLAPS', 'FINISH-BY', 'CONTAINS', 'STARTS', 'EQUALS']

    def __init__(self):
        """
        Construct the 7 allen relations transitivity table.
        """
        self._transitivity_table = {}
        # init the table to hold empty  arrays.
        for i in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.EQUAL + 1):
            self._transitivity_table[i] = {}
            for j in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.EQUAL + 1):
                self._transitivity_table[i][j] = []
        # handle BEFORE relation row
        row = AllenSevenRelationEngine.BEFORE
        for column in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.EQUAL + 1):
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.BEFORE)
        # handle MEET relation row
        row = AllenSevenRelationEngine.MEET
        for column in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.CONTAIN + 1):
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.BEFORE)
        for column in range(AllenSevenRelationEngine.STARTS, AllenSevenRelationEngine.EQUAL + 1):
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.MEET)
        # handle OVERLAP relation row
        row = AllenSevenRelationEngine.OVERLAP
        for column in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.MEET + 1):
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.BEFORE)
        for column in range(AllenSevenRelationEngine.STARTS, AllenSevenRelationEngine.EQUAL + 1):
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.OVERLAP)
        for column in range(AllenSevenRelationEngine.OVERLAP, AllenSevenRelationEngine.FINISHBY + 1):
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.BEFORE)
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.MEET)
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.OVERLAP)
        for relation in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.CONTAIN + 1):
            self._transitivity_table[row][AllenSevenRelationEngine.CONTAIN].append(relation)
        # handle FINISHBY relation row
        row = AllenSevenRelationEngine.FINISHBY
        for column in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.CONTAIN + 1):
            self._transitivity_table[row][column].append(column)
        self._transitivity_table[row][AllenSevenRelationEngine.STARTS].append(AllenSevenRelationEngine.OVERLAP)
        self._transitivity_table[row][AllenSevenRelationEngine.EQUAL].append(AllenSevenRelationEngine.FINISHBY)
        # handle CONTAIN relation row
        row = AllenSevenRelationEngine.CONTAIN
        for relation in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.CONTAIN + 1):
            self._transitivity_table[row][AllenSevenRelationEngine.BEFORE].append(relation)
        for relation in range(AllenSevenRelationEngine.OVERLAP, AllenSevenRelationEngine.CONTAIN + 1):
            self._transitivity_table[row][AllenSevenRelationEngine.MEET].append(relation)
            self._transitivity_table[row][AllenSevenRelationEngine.OVERLAP].append(relation)
            self._transitivity_table[row][AllenSevenRelationEngine.STARTS].append(relation)
        self._transitivity_table[row][AllenSevenRelationEngine.FINISHBY].append(AllenSevenRelationEngine.CONTAIN)
        self._transitivity_table[row][AllenSevenRelationEngine.CONTAIN].append(AllenSevenRelationEngine.CONTAIN)
        self._transitivity_table[row][AllenSevenRelationEngine.EQUAL].append(AllenSevenRelationEngine.CONTAIN)
        # handle STARTS relation row
        row = AllenSevenRelationEngine.STARTS
        for column in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.MEET + 1):
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.BEFORE)
        for column in range(AllenSevenRelationEngine.STARTS, AllenSevenRelationEngine.EQUAL + 1):
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.STARTS)
        for column in range(AllenSevenRelationEngine.OVERLAP, AllenSevenRelationEngine.FINISHBY + 1):
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.BEFORE)
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.MEET)
            self._transitivity_table[row][column].append(AllenSevenRelationEngine.OVERLAP)
        for relation in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.CONTAIN + 1):
            self._transitivity_table[row][AllenSevenRelationEngine.CONTAIN].append(relation)
        # handle EQUAL relation row
        row = AllenSevenRelationEngine.EQUAL
        for column in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.EQUAL + 1):
            self._transitivity_table[row][column].append(column)

    def print_transitivity_table(self):
        for i in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.EQUAL + 1):
            st = ''
            for j in range(AllenSevenRelationEngine.BEFORE, AllenSevenRelationEngine.EQUAL + 1):
                st += str([self.get_short_description(rel) for rel in self._transitivity_table[i][j]]) + '  '
            print(st)

    def get_transitivity_list(self, relation_ab, relation_bc):
        """
             return a List of transitive relations to the given ones.
               :param relation_ab: relation between two symbols AB.
               :param relation_bc: relation between two symbols BC.
               :return: list of possible relations between two symbols AC.
        """
        return self._transitivity_table[relation_ab][relation_bc]

    @staticmethod
    def check_relation(sym_ti1, sym_ti2, epsilon, max_gap):
        """
                check the relation between two symbolic time intervals
                :param sym_ti1:SymbolicTimeInterval, first object
                :param sym_ti2: SymbolicTimeInterval, second object
                :param epsilon: int, minimum time difference between two intervals that defines the relation
                :param max_gap: int,  maximum time difference between two time intervals for indexing to TIRP
                :return: the number of relation
                """
        relation = AllenSevenRelationEngine.NOT_DEFINED
        s2_minus_e1 = sym_ti2._start_time - sym_ti1._end_time
        if s2_minus_e1 > max_gap:
            return relation
        if sym_ti1._start_time > sym_ti2._start_time:
            return relation
        if epsilon < s2_minus_e1 < max_gap:
            relation = AllenSevenRelationEngine.BEFORE
        else:
            e1_minus_s2 = sym_ti1._end_time - sym_ti2._start_time
            s2_minus_s1 = sym_ti2._start_time - sym_ti1._start_time
            e1_minus_e2 = sym_ti1._end_time - sym_ti2._end_time
            e2_minus_e1 = sym_ti2._end_time - sym_ti1._end_time
            if s2_minus_s1 > epsilon >= abs(e1_minus_e2):
                relation = AllenSevenRelationEngine.FINISHBY
            elif s2_minus_s1 > epsilon >= abs(e1_minus_s2) and e1_minus_e2 < epsilon:
                relation = AllenSevenRelationEngine.MEET
            elif s2_minus_s1 > epsilon < e1_minus_s2 and e1_minus_e2 < epsilon:
                relation = AllenSevenRelationEngine.OVERLAP
            elif abs(s2_minus_s1) <= epsilon < e2_minus_e1:
                relation = AllenSevenRelationEngine.STARTS
            elif s2_minus_s1 > epsilon and e1_minus_e2 > epsilon:
                relation = AllenSevenRelationEngine.CONTAIN
            elif abs(s2_minus_s1) <= epsilon and abs(e1_minus_e2) <= epsilon:
                relation = AllenSevenRelationEngine.EQUAL
        return relation

    @staticmethod
    def get_full_description(relation):
        if relation == AllenSevenRelationEngine.NOT_DEFINED:
            return AllenSevenRelationEngine.NOT_DEFINED_DESCRIPTION
        return AllenSevenRelationEngine.RELATION_FULL_DESCRIPTION[relation]

    @staticmethod
    def get_short_description(relation):
        if relation == AllenSevenRelationEngine.NOT_DEFINED:
            return AllenSevenRelationEngine.NOT_DEFINED_DESCRIPTION
        return AllenSevenRelationEngine.RELATION_CHARS_FRESKA[relation]


class KLRelationEngine(object):
    """
        Engine to handle all KL relations logic.
    """
    NOT_DEFINED = -1
    BEFORE = 0
    OVERLAP = 1
    CONTAIN = 2
    NOT_DEFINED_DESCRIPTION = 'NOT DEFINED'
    RELATION_CHARS = ['p', 'o', 'D']
    RELATION_CHARS_FRESKA = ['<', 'o', 'c']
    RELATION_FULL_DESCRIPTION = ['BEFORE', 'OVERLAPS', 'CONTAINS']

    def __init__(self):
        self._relation_map_kl = {'NOT_DEFINED': KLRelationEngine.NOT_DEFINED,
                                 'BEFORE': 0,
                                 'OVERLAP': 1,
                                 'CONTAIN': 2}
        self._transitivity_table = {}
        relation = KLRelationEngine.BEFORE
        self._transitivity_table[relation] = {}
        self._transitivity_table[relation][KLRelationEngine.BEFORE] = [KLRelationEngine.BEFORE]
        self._transitivity_table[relation][KLRelationEngine.OVERLAP] = [KLRelationEngine.BEFORE]
        self._transitivity_table[relation][KLRelationEngine.CONTAIN] = [KLRelationEngine.BEFORE]
        relation = KLRelationEngine.OVERLAP
        self._transitivity_table[relation] = {}
        self._transitivity_table[relation][KLRelationEngine.BEFORE] = [KLRelationEngine.BEFORE]
        self._transitivity_table[relation][KLRelationEngine.OVERLAP] = [KLRelationEngine.BEFORE,
                                                                        KLRelationEngine.OVERLAP]
        self._transitivity_table[relation][KLRelationEngine.CONTAIN] = [KLRelationEngine.BEFORE,
                                                                        KLRelationEngine.OVERLAP,
                                                                        KLRelationEngine.CONTAIN]
        relation = KLRelationEngine.CONTAIN
        self._transitivity_table[relation] = {}
        self._transitivity_table[relation][KLRelationEngine.BEFORE] = [KLRelationEngine.BEFORE,
                                                                       KLRelationEngine.OVERLAP,
                                                                       KLRelationEngine.CONTAIN]
        self._transitivity_table[relation][KLRelationEngine.OVERLAP] = [KLRelationEngine.OVERLAP,
                                                                        KLRelationEngine.CONTAIN]
        self._transitivity_table[relation][KLRelationEngine.CONTAIN] = [KLRelationEngine.CONTAIN]

    @staticmethod
    def check_relation(sym_ti1, sym_ti2, epsilon, max_gap):
        """
        check the relation between two symbolic time intervals.
        :param sym_ti1:SymbolicTimeInterval, first object
        :param sym_ti2: SymbolicTimeInterval, second object
        :param epsilon: int, minimum time difference between two intervals that defines the relation
        :param max_gap: int,  maximum time difference between two time intervals for indexing to TIRP
        :return: the number of relation
        """
        relation = KLRelationEngine.NOT_DEFINED
        s2_minus_e1 = sym_ti2._start_time - sym_ti1._end_time
        if s2_minus_e1 > max_gap:
            return relation
        if sym_ti1._start_time > sym_ti2._start_time:
            return relation
        e1_minus_s2 = sym_ti1._end_time - sym_ti2._start_time
        s2_minus_s1 = sym_ti2._start_time - sym_ti1._start_time
        e1_minus_e2 = sym_ti1._end_time - sym_ti2._end_time
        e2_minus_e1 = sym_ti2._end_time - sym_ti1._end_time
        if epsilon < s2_minus_e1 < max_gap:
            relation = KLRelationEngine.BEFORE
        if abs(s2_minus_e1) == epsilon and e2_minus_e1 > epsilon:
            relation = KLRelationEngine.BEFORE
        elif s2_minus_s1 > epsilon < e1_minus_s2 and e1_minus_e2 < epsilon:
            relation = KLRelationEngine.OVERLAP
        elif abs(s2_minus_s1) <= epsilon and abs(e1_minus_e2) <= epsilon:
            relation = KLRelationEngine.CONTAIN
        elif abs(s2_minus_s1) <= epsilon < e2_minus_e1:
            relation = KLRelationEngine.CONTAIN
        elif s2_minus_s1 > epsilon >= abs(e1_minus_e2):
            relation = KLRelationEngine.CONTAIN
        elif s2_minus_s1 > epsilon < e1_minus_e2:
            relation = KLRelationEngine.CONTAIN
        return relation

    def get_transitivity_list(self, relation_ab, relation_bc):
        """
             return a List of transitive relations to the given ones.
               :param relation_ab: relation between two symbols AB.
               :param relation_bc: relation between two symbols BC.
               :return: list of possible relations between two symbols AC.
        """
        return self._transitivity_table[relation_ab][relation_bc]

    @staticmethod
    def get_full_description(relation):
        if relation == KLRelationEngine.NOT_DEFINED:
            return KLRelationEngine.NOT_DEFINED_DESCRIPTION
        return KLRelationEngine.RELATION_FULL_DESCRIPTION[relation]

    @staticmethod
    def get_short_description(relation):
        if relation == KLRelationEngine.NOT_DEFINED:
            return KLRelationEngine.NOT_DEFINED_DESCRIPTION
        return KLRelationEngine.RELATION_CHARS_FRESKA[relation]


class EqualRelationEngine(object):
    # TODO - get full description for this engine.
    """
        Engine to handle all KL relations logic.
    """
    NOT_DEFINED = -1
    EQUAL = 0
    BEFORE = 1
    RELATION_CHARS = ['e', 'p']
    RELATION_CHARS_FRESKA = ['=', '<']
    RELATION_FULL_DESCRIPTION = ['EQUALS', 'BEFORE']

    def __init__(self):
        self._relation_map_kl = {'NOT_DEFINED': EqualRelationEngine.NOT_DEFINED,
                                 'EQUAL': EqualRelationEngine.EQUAL,
                                 'BEFORE': EqualRelationEngine.BEFORE}
        self._transitivity_table = {}
        self._transitivity_table[EqualRelationEngine.EQUAL] = {}
        self._transitivity_table[EqualRelationEngine.BEFORE] = {}
        self._transitivity_table[EqualRelationEngine.EQUAL][EqualRelationEngine.EQUAL] = [EqualRelationEngine.EQUAL]
        self._transitivity_table[EqualRelationEngine.EQUAL][EqualRelationEngine.BEFORE] = [EqualRelationEngine.BEFORE]
        self._transitivity_table[EqualRelationEngine.BEFORE][EqualRelationEngine.EQUAL] = [EqualRelationEngine.BEFORE]
        self._transitivity_table[EqualRelationEngine.BEFORE][EqualRelationEngine.BEFORE] = [EqualRelationEngine.BEFORE]

    @staticmethod
    def check_relation(sym_ti1, sym_ti2, epsilon, max_gap):
        """
        check the relation between two symbolic time intervals.
        :param sym_ti1:SymbolicTimeInterval, first object
        :param sym_ti2: SymbolicTimeInterval, second object
        :param epsilon: int, minimum time difference between two intervals that defines the relation
        :param max_gap: int,  maximum time difference between two time intervals for indexing to TIRP
        :return: the number of relation
        """
        relation = EqualRelationEngine.NOT_DEFINED
        if sym_ti1._start_time > sym_ti2._start_time:
            return relation
        s2_minus_s1 = sym_ti2._start_time - sym_ti1._start_time
        e1_minus_e2 = sym_ti1._end_time - sym_ti2._end_time
        s2_minus_e1 = sym_ti2._start_time - sym_ti1._end_time
        if s2_minus_e1 > max_gap:
            return relation
        if abs(s2_minus_s1) <= epsilon and abs(e1_minus_e2) <= epsilon:
            relation = EqualRelationEngine.EQUAL
        elif epsilon < s2_minus_e1 < max_gap:
            relation = EqualRelationEngine.BEFORE
        return relation

    def get_transitivity_list(self, relation_ab, relation_bc):
        return self._transitivity_table[relation_ab][relation_bc]

    @staticmethod
    def get_full_description(relation):
        return EqualRelationEngine.RELATION_FULL_DESCRIPTION[relation]

    @staticmethod
    def get_short_description(relation):
        return EqualRelationEngine.RELATION_CHARS_FRESKA[relation]


class BeforeRelationEngine(object):
    # TODO - get full description for this engine.
    """
        Engine to handle all KL relations logic.
    """
    NOT_DEFINED = -1
    BEFORE = 0
    MEET = 1
    RELATION_CHARS = ['p', 'm']
    RELATION_CHARS_FRESKA = ['<', 'm']
    RELATION_FULL_DESCRIPTION = ['BEFORE', 'MEETS']

    def __init__(self):
        self._relation_map_kl = {'NOT_DEFINED': BeforeRelationEngine.NOT_DEFINED,
                                 'BEFORE': 0}

    @staticmethod
    def check_relation(sym_ti1, sym_ti2, epsilon, max_gap):
        """
        check the relation between two symbolic time intervals.
        :param sym_ti1:SymbolicTimeInterval, first object
        :param sym_ti2: SymbolicTimeInterval, second object
        :param epsilon: int, minimum time difference between two intervals that defines the relation
        :param max_gap: int,  maximum time difference between two time intervals for indexing to TIRP
        :return: the number of relation
        """
        relation = BeforeRelationEngine.NOT_DEFINED
        if sym_ti1._start_time > sym_ti2._start_time:
            return relation
        e1_minus_s2 = sym_ti1._end_time - sym_ti2._start_time
        s2_minus_s1 = sym_ti2._start_time - sym_ti1._start_time
        e1_minus_e2 = sym_ti1._end_time - sym_ti2._end_time
        s2_minus_e1 = sym_ti2._start_time - sym_ti1._end_time
        if s2_minus_e1 > max_gap:
            return relation
        if epsilon < s2_minus_e1 < max_gap:
            relation = BeforeRelationEngine.BEFORE
        elif s2_minus_s1 > epsilon >= abs(e1_minus_s2) and e1_minus_e2 < epsilon:
            relation = BeforeRelationEngine.MEET
        return relation

    def get_transitivity_list(self, relation_ab, relation_bc):
        ans = [BeforeRelationEngine.BEFORE]
        return ans

    @staticmethod
    def get_full_description(relation):
        return BeforeRelationEngine.RELATION_FULL_DESCRIPTION[relation]

    @staticmethod
    def get_short_description(relation):
        return BeforeRelationEngine.RELATION_CHARS_FRESKA[relation]


class RelationHandler(object):
    RELATION_NOT_DEFINED = -1
    RELATION_EQUALS_BEFORE = 1
    RELATION_BEFORE = 2
    RELATION_KL = 3
    RELATION_ALLEN_7 = 7

    def __init__(self, num_of_relations):
        self._num_of_relations = num_of_relations
        self._relations_handler_engine = None
        # set the current engine based on the given relations number.
        if self._num_of_relations == RelationHandler.RELATION_ALLEN_7:
            self._relations_handler_engine = AllenSevenRelationEngine()
        elif self._num_of_relations == RelationHandler.RELATION_KL:
            self._relations_handler_engine = KLRelationEngine()

    def check_relation(self, sym_ti1, sym_ti2, epsilon, max_gap):
        """
            check the relation between two symbolic time intervals using the current relation engine.
            :param sym_ti1:SymbolicTimeInterval, first object
            :param sym_ti2: SymbolicTimeInterval, second object
            :param epsilon: int, minimum time difference between two intervals that defines the relation
            :param max_gap: int,  maximum time difference between two time intervals for indexing to TIRP
            :return: the number of relation
        """
        return self._relations_handler_engine.check_relation(sym_ti1, sym_ti2, epsilon, max_gap)

    def get_transitivity_list(self, relation_ab, relation_bc):
        """
           return a List of transitive relations to the given relations from the current engine.
           :param relation_ab: relation between two symbols AB.
           :param relation_bc: relation between two symbols BC.
           :return: list of possible relations between two symbols AC.
        """
        return self._relations_handler_engine.get_transitivity_list(relation_ab, relation_bc)

    def get_full_description(self, relation):
        """
            Get full name of a given relation from the current engine.
            :param relation: numeric representation of a relation
            :return: full name of a given relation
        """
        return self._relations_handler_engine.get_full_description(relation)

    def get_short_description(self, relation):
        """
            Get short name/char of a given relation from the current engine.
            :param relation: numeric representation of a relation
            :return: short name/char of a given relation
        """
        return self._relations_handler_engine.get_short_description(relation)
