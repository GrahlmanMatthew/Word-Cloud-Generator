import sys
from wordcloud.stopwords import set_stopwords
from wordcloud.vocabulary import create_vocab

# WORD CLOUD INPUT PARAMS
NUM_WORDS = 25
STOPWORDS_DATA_PATH = './lang/stopwords.txt'
stopwords = set_stopwords(STOPWORDS_DATA_PATH)

# NORMALIZE INPUT DATA FROM FILE AND BUILD WORD DICT
INPUT_DATA_PATH = './input/data.txt'
vocab = create_vocab(NUM_WORDS, INPUT_DATA_PATH, stopwords)
print("%d most common words; %s" % (NUM_WORDS, vocab))


