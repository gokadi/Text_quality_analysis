from language_check import LanguageTool


class GrammMark:

    def __init__(self, obj):
        self.__value = 0.0
        self.__obj = obj
        self.__txt = obj.get_txt()
        self.__commas(obj)

    def __commas(self, obj):
        tool = LanguageTool("ru-RU")
        matches = tool.check(self.__txt)
        self.__value = len(matches) / obj.get_totalword()
        if self.__value >= 0.5:
            self.__value = 1.0
        else:
            self.__value *= 2

    def get_mark(self):
        return 1 - self.__value
