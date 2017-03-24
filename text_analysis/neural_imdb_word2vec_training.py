import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk.data
from nltk.corpus import stopwords
import logging
from gensim.models import word2vec

# Read data from files
train = pd.read_csv( "D:/учеба_магистратура/6курс/Александров/нейросеть/labeledTrainData.tsv", header=0,
 delimiter="\t", quoting=3 )
test = pd.read_csv( "D:/учеба_магистратура/6курс/Александров/нейросеть/testData.tsv", header=0, delimiter="\t", quoting=3 )
unlabeled_train = pd.read_csv( "D:/учеба_магистратура/6курс/Александров/нейросеть/unlabeledTrainData.tsv", header=0,
 delimiter="\t", quoting=3 )

# Verify the number of reviews that were read (100,000 in total)
print("Read %d labeled train reviews, %d labeled test reviews, "
      "and %d unlabeled reviews" % (train["review"].size,  test["review"].size, unlabeled_train["review"].size))

def review_to_wordlist( review, remove_stopwords=False ):
    # Делим преложение на список слов (list of words)
    # 1. Очистка от html тегов и URLов
    review = re.sub(r'^https?:\/\/.*[\r\n]*', '', review, flags=re.MULTILINE)
    review_text = BeautifulSoup(review, "html.parser").get_text()
    # 2. Оставить только буквы
    review_text = re.sub("[^a-zA-Z]"," ", review_text)
    # 3. Привести текст к нижнему регистру и разделить на слова
    words = review_text.lower().split()
    # 4. Удалить стоп слова (по флагу)
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    # 5. Вернуть список слов
    return(words)

# Инициализация tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def review_to_sentences( review, tokenizer, remove_stopwords=False ):
    # Делим обзор на предложения. Обзор - > список предложений - > список слов
    # 1. Используем токенайзер для деления обзора на предложения
    raw_sentences = tokenizer.tokenize(review.strip())
    # 2. Для каждого предложения вызываем функцию преобразования в список слов
    sentences = []
    for raw_sentence in raw_sentences:
        # Пустые предложения пропускаем
        if len(raw_sentence) > 0:
            sentences.append( review_to_wordlist( raw_sentence,
              remove_stopwords ))
    # Возвращаем список предложений, каждое из которых - список слов. list of lists
    return sentences

sentences = []

print("Parsing sentences from training set")
for review in train["review"]:
    sentences += review_to_sentences(review, tokenizer)

print("Parsing sentences from unlabeled set")
for review in unlabeled_train["review"]:
    sentences += review_to_sentences(review, tokenizer) # если делать append, то только первый из
                                                        # списков прикрепится. (list of lists)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

# Обучение Word2Vec модели
num_features = 300    # Размерность вектора
min_word_count = 40   # Слово, встречающееся меньше этого числа не учитывать. (Фильтрует, например, инициалы)
num_workers = 4       # Число параллельных процессов, для ускорения обучения
context = 10          # Как много слов из окружения слова должно учитываться при обучении
downsampling = 1e-3   # Исключаем часто встречающиеся в тексте слова


print("Training model...")
model = word2vec.Word2Vec(sentences, workers=num_workers,
            size=num_features, min_count = min_word_count,
            window = context, sample = downsampling)

# Уменьшает количество используемой RAM
model.init_sims(replace=True)

# Сохраняем модель
model_name = "300features_40minwords_10context"
model.save(model_name)