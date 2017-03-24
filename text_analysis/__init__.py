from text_analysis.preparat import PrepText
from text_analysis.gramm import GrammMark
from text_analysis.wateriness import Water
from text_analysis.orfogr import Orthography
from text_analysis.inform import Informativity
from text_analysis.tonalcy import Tonal
from text_analysis.neural_imdb_word2vec_using import Word2VecUsage
from text_analysis.neural_imdb_word2vec_training import Word2VecTrain

if __name__ == "__main__":
    w2v_train = Word2VecTrain()
    # w2v = Word2VecUsage()
    obj = PrepText("D://text")
    vocab = obj.get_lsWord()
    gramm = GrammMark(obj)
    water = Water(obj)
    orth = Orthography(obj)
    info = Informativity(obj)
    ton = Tonal(obj)
    print(water.get_mark())
    print(gramm.get_mark())
    print(orth.get_mark())
    print(info.get_mark())
    total_mark = (water.get_mark() + gramm.get_mark() + orth.get_mark() + info.get_mark())/4
    print("Общая оценка качества текста: ", total_mark)
