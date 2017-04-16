from text_analysis.preparat import PrepText
from text_analysis.gramm import GrammMark
from text_analysis.wateriness import Water
from text_analysis.orfogr import Orthography
from text_analysis.inform import Informativity
from text_analysis.tonalcy import Tonal
from text_analysis.neural_imdb_word2vec_using import Word2VecUsage
from text_analysis.neural_imdb_word2vec_training import Word2VecTrain

if __name__ == "__main__":
    # w2v_train = Word2VecTrain()
    obj = PrepText("D://text")
    vocab = obj.get_lsWord()
    gramm = GrammMark(obj)
    water = Water(obj)
    orth = Orthography(obj)
    info = Informativity(obj)
    # o = Word2VecUsage()
    # print("оценка пробная:")
    #print(o.pred("Естественно в фильме, кто главные темы, имеют смертность, ностальгию и потерю невиновности, возможно, не удивительно, что это оценено более высоко зрителями старшего возраста, чем младшие. Однако, есть мастерство и полнота к фильму, которым любой может наслаждаться.","RU"))
    # print(o.pred("Фильм был замечательный"))
    ton = Tonal(obj)
    print(water.get_mark())
    print(gramm.get_mark())
    print(orth.get_mark())
    print(info.get_mark())
    # print(ton.get_mark())
    total_mark = (water.get_mark() + gramm.get_mark() + orth.get_mark() + info.get_mark())/4
    print("Общая оценка качества текста: %.2f" % total_mark)
