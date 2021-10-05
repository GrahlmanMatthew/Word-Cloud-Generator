import os
from wordcloud.stopwords import set_stopwords
from wordcloud.vocabulary import create_vocab
from wordcloud.grid import GridGenerator, center_word_in_square
from wordcloud.cloud import place_words
from aabbtree import AABB, AABBTree

# TO DO
# 1. RANDOMIZE FONT SELECTION
# 2. MAKE FONT SIZE MULTIPLIER DYNAMIC
# 3. MAKE WORD PLACEMENT FAVOUR THE CENTER OF THE CANVAS
# 4. CLEAN UP IMAGE GENERATION [wip]

# WORD CLOUD INPUT PARAMS
NUM_WORDS = 32
CONST_SCALE = 12
FONT_SIZE_MULTIPLIER = 7
IMAGE_WIDTH, IMAGE_HEIGHT = 500, 500
STOPWORDS_DATA_PATH = './lang/stopwords.txt'
stopwords = set_stopwords(STOPWORDS_DATA_PATH)

# NORMALIZE INPUT DATA FROM FILE AND BUILD WORD DICT
INPUT_DATA_PATH = './input/data.txt'
vocab = create_vocab(NUM_WORDS, INPUT_DATA_PATH, stopwords)
print("%d most common words; %s" % (NUM_WORDS, vocab))

# DETERMINE FONT SIZES - FIRST NEED TO GET TOTAL NUMBER OF OCCURENCES OF ALL WORDS IN OUR VOCAB
vocab_sizes = {}
num_vocab_occurences = 0
for word in vocab:
    vocab_sizes[word] = vocab[word]
    num_vocab_occurences += vocab[word]

# DETERMINE FONT SIZE FOR EACH WORD BASED ON FONT_SIZE_MULTIPLIER
for word in vocab_sizes:
    font_size = round((vocab_sizes[word] * FONT_SIZE_MULTIPLIER / num_vocab_occurences) * 100, 0)
    vocab_sizes[word] = int(font_size)

# Generates grid of grids and coords of potential positions to place words on these grids
grid_gen = GridGenerator(IMAGE_WIDTH, IMAGE_HEIGHT, NUM_WORDS)
grid_gen.draw_grid()
grid = grid_gen.get_grid()

# CREATES WORDLCOUD
WC_IMG_FILEPATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'output', 'wordcloud.png'))   
WC_BOUNDS_IMG_FILEPATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'output', 'word-bounds.png'))
place_words(vocab, vocab_sizes, grid, grid_gen)