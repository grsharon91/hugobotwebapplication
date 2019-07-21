from copy import copy


class TirpMatrix(object):
    """
        Class represents logic of "half TIRP matrix"
        holds the size of the symbol array corresponding to this half matrix.
        holds and array of relations.
        Half matrix logic definition:
        - the actual data needed for the relations is (|symbols| * (|symbols| -1)) / 2.
        - matrix row is all the symbols excluding the last one.
        - matrix column is all the symbols excluding the first one.
        - the matrix represented full size is (|symbols|-1)^2
        definition example:
            for symbols array = [A, B, C]
            and relations [r1, r2, r3], |relations| = 3*2/2
            the half matrix is

                | B | C
              -----------
              A | r1| r2
              B |   | r3
        self._size define as |symbols|-1
    """
    def __init__(self, relation=None):
        if relation is not None:
            self._size = 1
            self._relations = [relation]
        else:
            self._size = 0
            self._relations = []

    def get_relation(self, first_index, second_index):
        """
            Get the relation corresponds to the given indices from the representing symbols array.

            since the matrix logic as defined, then the second index must be subtracted by one.

            Constrains:
             - second_index >= first_index
             - self._size > first_index >= 0
             - self._size > second_index >= 0

             use the function n(a1 + an)/2 to calculate the offset in the relations array to be in the first place in
             the corresponding row data.

             subtract the "empty space" in the matrix is a function of row number and column index.

            for symbols array = [A, B, C]  and relations [r1, r2, r3]
            the half matrix is

                | B | C
              -----------
              A | r1| r2
              B |   | r3

              A as first index will be 0
              C as second index will be 2, but the index in the represented is 2-1 = 1.

        :param first_index: the first index of the symbol in the corresponding symbols array for the current relations
        :param second_index: the second index of the symbol in the corresponding symbols array for the current relations
        :return: the relation between symbols[first_index] and symbols[second_index]
        """
        row_index = first_index
        column_index = second_index - 1
        # offset = (row_index * (self._size + self._size - (row_index - 1))) / 2
        # index = int(offset + column_index - row_index)
        index = int(((1 + column_index) * column_index) / 2 + row_index)
        return self._relations[index]

    def extend(self, relation_column):
        """
            Extends the current matrix to support new symbol column.
            matrix size scales by 1 symbol representation.

            Example:
                Given
                relation_column = [r4,r5,r6]

            Current representation:

                relations = [r1, r2, r3]
                representing some [A, B, C] symbols order.

                | B | C  |
              --|---|----|
              A | r1| r2 |
              --|---|----|
              B |   | r3 |
              --|---|----|

            Becomes:

                relations = [r1, r2, r4, r3, r5, r6]
                representing some [A, B, C, D] symbols order.

                | B | C | D |
              --|---|---|---|
              A | r1| r2| r4|
              --|---|---|---|
              B |   | r3| r5|
              --|---|---|---|
              C |   |   | r6|

        :param relation_column: the column of relations as the new column in the "matrix"
        """
        for index in range(1, len(relation_column) + 1):
            # self.relations.insert(self.size * index, relation_column[index - 1])
            self._relations.append(relation_column[index - 1])
        self._size += 1

    def copy(self):
        ans = TirpMatrix()
        ans._size = self._size
        ans._relations = copy(self._relations)
        return ans

    def get_all_direct_relations(self):
        """
        extract the last relation column in the TirpMatrix
        :return: ans: list of int, the last relation column
        """
        return self._relations[len(self._relations) - self._size:]
        # ans = []
        # iterations = self._size
        # offset = 0
        # index = 0
        # while iterations > 0:
        #     ans.append(self._relations[index])
        #     offset += 1
        #     index += self._size - offset + 1
        #     iterations -= 1
        # return ans

    def get_relations(self):
        return self._relations

    def to_string(self):
        ans = ''
        for rel in self._relations:
            ans += str(rel) + '_'
        ans = ans[0: -1]
        return ans
