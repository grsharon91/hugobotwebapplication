class DataTooDenseError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg
        return

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.__str__()
