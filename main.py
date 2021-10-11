import os
from wordcloud.stopwords import set_stopwords
from wordcloud.vocabulary import create_vocab
from wordcloud.grid import GridGenerator, center_word_in_square
from wordcloud.cloud import place_words

# INPUT DATA FILE PATHS
STOPWORDS_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'lang', 'stopwords.txt'))
INPUT_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'input', 'data.txt'))

# WORD CLOUD SETTINGS FOR OUTPUT IMAGE
NUM_WORDS = 24
IMAGE_WIDTH = 500
IMAGE_HEIGHT = 500

# TO DO
# 3. bug with small fonts on larger img sizes

# NORMALIZE INPUT DATA FROM FILE AND BUILD WORD DICT
stopwords = set_stopwords(STOPWORDS_DATA_PATH)
vocab = create_vocab(NUM_WORDS, INPUT_DATA_PATH, stopwords)

# Generates grid of grids and coords of potential positions to place words on these grids
grid_gen = GridGenerator(IMAGE_WIDTH, IMAGE_HEIGHT, NUM_WORDS)
grid_gen.draw_grid()
grid = grid_gen.get_grid()


# CREATES WORDLCOUD
WC_IMG_FILEPATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'output', 'wordcloud.png'))   
WC_BOUNDS_IMG_FILEPATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'output', 'word-bounds.png'))
place_words(vocab, grid, grid_gen)