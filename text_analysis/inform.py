

class Informativity:

    def __init__(self, obj):
        self.__value = 0.0
        self.__obj = obj
        self.__vocab = obj.get_lsWord()
        self.__inf(obj)

    def __inf(self, obj):
        self.__value = len(self.__vocab) / obj.get_totalword()
        if self.__value >= 0.8:
            self.__value = 1
        elif self.__value < 0.3:
            self.__value = 0

    def get_mark(self):
        return self.__value