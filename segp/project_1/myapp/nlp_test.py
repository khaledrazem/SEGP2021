# created with reference from https://www.nltk.org/

# Import libraries for text preprocessing
import re
import nltk
# You only need to download these resources once. After you run this
# the first time--or if you know you already have these installed--
# you can comment these two lines out (with a #)
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

# Sample the returned vector encoding the length of the entire vocabulary
# print(list(cv.vocabulary_.keys())[:10])

def disc(arr):
    discription = ""
    for i in arr:
        temp = ""
        if i['discription'] is not None:
            temp = " " + i['discription']
            discription += temp
    
    top_word = related_word(discription)
    
    return top_word


def related_word(txt):
    nltk.download('stopwords')
    nltk.download('wordnet')
    # Create a list of stop words from nltk
    stop_words = set(stopwords.words("english"))
    dataset={}
    dataset['data'] = txt
    # Pre-process dataset to get a cleaned and normalised text corpus
    corpus = []
    dataset['word_count'] = len(str(dataset['data']).split(" "))
    # Remove punctuation
    text = re.sub('[^a-zA-Z]', ' ', dataset['data'])
    # Convert to lowercase
    text = text.lower()
    # Remove tags
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
    # Remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)
    # Convert to list from string
    text = text.split()
    ps = PorterStemmer()
    # Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in stop_words]
    text = " ".join(text)
    corpus.append(text)
    top_words = get_top_n_words(corpus, n=5)
    top2_words = get_top_n2_words(corpus, n=5)
    top3_words = get_top_n3_words(corpus, n=5)
    top_words.extend(top2_words)
    top_words.extend(top3_words)
    unzipped_top_words= zip(*top_words)
    unzipped_top_words_list = list(unzipped_top_words)
    unzipped_top_words_list[1] = data_norm(unzipped_top_words_list[1])
    
    temp_word = []
    temp_size = []
    word = []
    size = []
    
    for x in unzipped_top_words_list[0]:
        temp_word.append(x)

    for y in unzipped_top_words_list[1]:
        temp_size.append(y)

    i = 0
    
    N = len(temp_size)
    largest = sorted(range(N), key=lambda sub: temp_size[sub])[-N:]
    
    while i < len(largest):
        word.append(temp_word[largest[i]])
        size.append(temp_size[largest[i]])
        i += 1
        
    word.reverse()
    word = [x.title() for x in word]
    size.reverse()
    
    result = {
        "words": zip(word,size)
    }

    #print(unzipped_top_words_list)
    return result

def get_top_n_words(corpus, n=None):
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in
                   vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1],
                       reverse=True)
    return words_freq[:n]

# Most frequently occuring bigrams
def get_top_n2_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(2,2),
            max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in
                  vec1.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1],
                reverse=True)
    return words_freq[:n]

# Most frequently occuring Tri-grams
def get_top_n3_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(3,3),
           max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in
                  vec1.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1],
                reverse=True)
    return words_freq[:n]


def data_norm(arr):
    max_val = float(max(arr)) * 1.05
    min_val = float(min(arr)) * 0.95
    score = []

    for x in arr:
        point = ((float(x) - min_val) / (max_val - min_val)) * (3 - 1) + 1
        score.append(round(point,1))
    return score

