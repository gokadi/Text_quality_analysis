from language_check import LanguageTool


class GrammMark:

    def __init__(self, obj):
        self.__obj = obj
        self.__txt = obj.get_txt()
        self.__commas(obj)

    def __commas(self, obj):
        tool = LanguageTool("ru-RU")
        matches = tool.check(self.__txt)
        self.__value = len(matches) / obj.get_totalword()

    def get_mark(self):
        return self.__value
