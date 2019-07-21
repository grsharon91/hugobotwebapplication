class SymbolicTimeInterval(object):
    """
     Symbolic time Interval representing a time interval with start time and end time and corresponds to a given symbol.
    """

    def __init__(self, start_time=None, end_time=None, symbol=None, var_id=None):
        if start_time is not None:
            self._start_time = start_time
            self._end_time = end_time
            self._symbol = symbol
            self._var_id = var_id

    def __hash__(self):
        return hash((self._start_time, self._end_time, self._symbol, self._var_id))

    def __eq__(self, other):
        return self._start_time == other._start_time and self._end_time == other._end_time and self._symbol == \
               other._symbol and self._var_id == other._var_id

    def getStartTime(self):
        return self._start_time

    def getEndTime(self):
        return self._end_time

    def getSymbol(self):
        return self._symbol

    def getVarID(self):
        return self._var_id

    def to_string(self):
        return 'SymbolicTimeInterval: { Symbol.py: ' + str(self._symbol) + ', startTime: ' + str(self._start_time) + \
               ', endTime: ' + str(self._end_time) + ', varID: ' + str(self._var_id) + '}'

    def copy(self):
        """
        create new SymbolicTimeInterval and copy all current variables
        :return: SymbolicTimeInterval,copy of this tirp
        """
        new_symbolic_time_interval = SymbolicTimeInterval()
        new_symbolic_time_interval._start_time = self._start_time
        new_symbolic_time_interval._end_time = self._end_time
        new_symbolic_time_interval._symbol = self._symbol
        new_symbolic_time_interval._var_id = self._var_id
        return new_symbolic_time_interval

    def compare(self, other):
        if self._start_time < other._start_time:
            return -1
        elif self._start_time == other._start_time and self._end_time < other._end_time:
            return -1
        elif self._start_time == other._start_time and self._end_time == other._end_time and self._symbol < \
                other._symbol:
            return -1
        else:
            return 1
