from text_analysis.preparat import PrepText
from text_analysis.gramm import GrammMark

if __name__ == "__main__":
    obj = PrepText("D://text")
    vocab = obj.get_lsWord()
    gramm = GrammMark(obj)
    print(gramm.get_mark())