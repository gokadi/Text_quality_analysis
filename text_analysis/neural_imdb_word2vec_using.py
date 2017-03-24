from gensim.models import Word2Vec
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re
from sklearn.ensemble import RandomForestClassifier


model = Word2Vec.load("300features_40minwords_10context")

# Read data from files
train = pd.read_csv( "D:/учеба_магистратура/6курс/Александров/нейросеть/labeledTrainData.tsv", header=0,
 delimiter="\t", quoting=3 )
test = pd.read_csv( "D:/учеба_магистратура/6курс/Александров/нейросеть/testData.tsv", header=0, delimiter="\t", quoting=3 )
unlabeled_train = pd.read_csv( "D:/учеба_магистратура/6курс/Александров/нейросеть/unlabeledTrainData.tsv", header=0,
 delimiter="\t", quoting=3 )

# в модели просто вектора для всех слов из всех обзоров.
# здесь для каждого обзора составляем усредненный вектор
def makeFeatureVec(words, model, num_features):
    # Усредняем вектора для всех слов в обзоре
    # Инициализируем массив
    featureVec = np.zeros((num_features,),dtype="float32")
    nwords = 0.
    # Index2word - список, содержащий слова из словаря модели. Конвертируем в set
    index2word_set = set(model.wv.index2word)
    # Для всех слова в обзоре, если они в словаре, суммируем вектора
    for word in words:
        if word in index2word_set:
            nwords = nwords + 1.
            featureVec = np.add(featureVec,model[word])
    # Усредняем получившийся вектор
    featureVec = np.divide(featureVec,nwords)
    return featureVec

def getAvgFeatureVecs(reviews, model, num_features):
    # Вычисляем усредненные вектора для набора обзоров
    # Инициализируем счетчик
    counter = int(0)
    # Инициализация массива усредненных векторов
    reviewFeatureVecs = np.zeros((len(reviews),num_features),dtype="float32")
    # Цикл по всем обзорам
    for review in reviews:
       # Статус вычислений
       if counter%1000. == 0.:
           print("Review %i of %d" % (counter, len(reviews)))
       # Для каждого обзора вычисляем его усредненный вектор
       reviewFeatureVecs[counter] = makeFeatureVec(review, model,
           num_features)
       # Счетчик ++
       counter = counter + 1
    # Возвращаем массив усредненных векторов
    return reviewFeatureVecs

num_features = int(300)   # Размерность вектора слов

def review_to_wordlist( review, remove_stopwords=False ):
    # Делим преложение на список слов (list of words)
    # 1. Очистка от html тегов и URLов
    review = re.sub(r'^https?:\/\/.*[\r\n]*', '', review, flags=re.MULTILINE)
    review_text = BeautifulSoup(review, "html.parser").get_text()
    # 2. Оставить только буквы
    review_text = re.sub("[^a-zA-Z]", " ", review_text)
    # 3. Привести текст к нижнему регистру и разделить на слова
    words = review_text.lower().split()
    # 4. Удалить стоп слова (по флагу)
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    # 5. Вернуть список слов
    return (words)


# ****************************************************************
# Вызов функций для набора данных

print("Creating average feature vecs for train reviews")
clean_train_reviews = []
for review in train["review"]:
    clean_train_reviews.append( review_to_wordlist( review,
        remove_stopwords=True ))

trainDataVecs = getAvgFeatureVecs( clean_train_reviews, model, num_features )

print("Creating average feature vecs for test reviews")
clean_test_reviews = []
for review in test["review"]:
    clean_test_reviews.append( review_to_wordlist( review,
        remove_stopwords=True ))

testDataVecs = getAvgFeatureVecs( clean_test_reviews, model, num_features )

forest = RandomForestClassifier( n_estimators = 100 ) # Число деревьев

print("Fitting a random forest to labeled training data...")
forest = forest.fit( trainDataVecs, train["sentiment"] )

# Test & extract results
result = forest.predict( testDataVecs )

# Write the test results
output = pd.DataFrame( data={"id":test["id"], "sentiment":result} )
output.to_csv( "D:/учеба_магистратура/6курс/Александров/нейросеть/Word2Vec_AverageVectors.tsv", index=False, sep="\t", quoting=3 )