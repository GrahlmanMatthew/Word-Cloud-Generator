import os
from input import user_input_filename, user_input_integer
from wordcloud.stopwords import set_stopwords
from wordcloud.vocabulary import create_vocab
from wordcloud.grid import GridGenerator, center_word_in_square
from wordcloud.cloud import place_words

STOPWORDS_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'lang', 'stopwords.txt'))  # path to stopwords file

# Collect input parameters from user
print("Welcome to WordCloud Generator!")
input_file = user_input_filename("Please enter the .txt file to generate the WordCloud image for")
num_words = user_input_integer("Please enter the # of words to try to place in the WordCloud", 5, 100)
image_dim = user_input_integer("Please enter the dimension of the image to generate (e.g. 500 for a 500x500 img)", 100, 1000)

# NORMALIZE INPUT DATA FROM FILE AND BUILD WORD DICT
stopwords = set_stopwords(STOPWORDS_DATA_PATH)
print("\nGenerated vocabulary:")
vocab = create_vocab(num_words, input_file, stopwords)

# Generates grid of grids and coords of potential positions to place words on these grids
grid_gen = GridGenerator(image_dim, image_dim, num_words)
grid_gen.draw_grid()
grid = grid_gen.get_grid()

# CREATES WORDLCOUD
WC_IMG_FILEPATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'output', 'wordcloud.png'))   
WC_BOUNDS_IMG_FILEPATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'output', 'word-bounds.png'))
place_words(vocab, grid, grid_gen)