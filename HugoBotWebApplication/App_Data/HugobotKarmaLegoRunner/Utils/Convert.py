def from_data_frame_to_sequence(data_frame):
    """
    Give a data frame with symbols as values, convert the data frame into karma lego symbolic time interval representation.
    when the length of each interval is fixed.
    when each interval is with the same length,
    :param data_frame: data frame with symbolic arrays.
    :return:  string representing the given data frame as symbolic time intervals in karma lego representation.

    """
    ans = ''
    for column in data_frame:
        ans += from_values_to_sequances(data_frame[column].values.tolist())
    return ans


def from_values_to_sequances(values):
    """
    Given an array of symbols, convert them into equal length time intervals.
    when the start time is 0 and with intervals of 1.
    :param values: array of symbols
    :return: string representing the given symbols as symbolic time intervals in karma lego representation.
    """
    ans = ''
    index = 0
    for symbol in values:
        ans += convert_to_sequence_unit(symbol, index)
        index += 1
    return ans


def convert_to_sequence_unit(symbol, start_time):
    """
    Given a symbol, format the symbol into time interval format, when start time is the given and the end time is start time + 1.
    :param symbol: symbol of the time interval.
    :param start_time: the value of the start time
    :return: symbolic time interval format.

    example:
    given A and 3 will return '3,4,A;'
    """
    return str(start_time) + ',' + str(start_time + 1) + ',' + str(symbol) + ';'


def from_data_frame_time_intervals(data_frame):
    """
    Given a data frame with symbols as values, convert the data frame into karma lego symbolic time intervals representation.
    when the length of each interval is aggregated for the same symbol.
    :param data_frame: data frame with symbolic arrays.
    :return: string representing the given data frame as symbolic time intervals in karma lego representation.
    """
    ans = ''
    for column in data_frame:
        ans += from_values_to_time_intervals(data_frame[column].values.tolist())
    return ans

def from_values_to_time_intervals(values):
    """
    Given an array of symbols as values, convert the symbols into karma lego symbolic time intervals representation.
    when the length of each interval is aggregated for the same symbol.
    :param values: symbols array
    :return: string representing the given symbols as symbolic time intervals in karma lego representation.
    """
    ans = ''
    index = 0
    last_symbol = None
    last_index = 0
    for symbol in values:
        if last_symbol is not None:
            if last_symbol != symbol:
                ans += convert_to_interval_unit(last_symbol, last_index, index)
                last_index = index

        last_symbol = symbol

        index += 1

        # handle the last interval.
        if index == len(values):
            ans += convert_to_interval_unit(last_symbol, last_index, index)

    return ans

def convert_to_interval_unit(symbol, start, end):
    """
    Given a symbol, format the symbol into time interval format, when start time and end time is given.
    :param symbol: symbol of the time interval.
    :param start: start time
    :param end: end time
    :return: format of a symbol and start and end time.

    example:
    given A and start 3 and end 6 will return '3,6,A;'
    """
    return str(start) + ',' + str(end) + ',' + str(symbol) + ';'