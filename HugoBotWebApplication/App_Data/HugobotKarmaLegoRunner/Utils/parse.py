import logging
from KarmaLego_Framework.SymbolicTimeInterval import SymbolicTimeInterval


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('KarmaTests')
logger.setLevel(20)


def parser_of_sym_ti_row_for_different_formats(sym_ti, num_comma):
    """
    Parse the format that the symbolic time interval is represented with.
    :param sym_ti: text that represent STI
    :param num_comma: if the file format is (start_time, end_time,var_id,state) then num_comma=3
                      if (start_time, end_time,state,var_id) then num_comma == 2
                      if (start_time, end_time,state) then num_comma == 2
    :return: SymbolicTimeInterval, symbol
    """
    parts = sym_ti.split(",")
    st = int(parts[0])
    et = int(parts[1])
    symbol = parts[num_comma]
    if len(parts) == 3:
        var_id = None
    elif num_comma == 2:
        var_id = parts[3]
    else:
        var_id = parts[2]
    sym_ti_obj = SymbolicTimeInterval(start_time=st, end_time=et, symbol=symbol, var_id=var_id)
    return sym_ti_obj, symbol

