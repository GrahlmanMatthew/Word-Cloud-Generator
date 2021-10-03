import sys
import random
from PIL import Image, ImageFont, ImageDraw
from wordcloud.stopwords import set_stopwords
from wordcloud.vocabulary import create_vocab
from aabbtree import AABB, AABBTree

# WORD CLOUD INPUT PARAMS
NUM_WORDS = 25
CONST_SCALE = 12
FONT_SIZE_MULTIPLIER = 7
IMAGE_WIDTH, IMAGE_HEIGHT = 500, 500
FONT_COLOUR = (0, 0, 0) # black
STOPWORDS_DATA_PATH = './lang/stopwords.txt'
stopwords = set_stopwords(STOPWORDS_DATA_PATH)

# NORMALIZE INPUT DATA FROM FILE AND BUILD WORD DICT
INPUT_DATA_PATH = './input/data.txt'
vocab = create_vocab(NUM_WORDS, INPUT_DATA_PATH, stopwords)
print("%d most common words; %s" % (NUM_WORDS, vocab))

# CREATES WORDCLOUD IMAGE
IMG_FILEPATH = './output/wordcloud.png'
img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='white')
draw = ImageDraw.Draw(img)

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

# DRAW WORDS
tree = AABBTree()
while len(vocab) > 0:
    # info about the word
    word_tuple = vocab.popitem()
    word = word_tuple[0]
    word_size = vocab_sizes[word]
    font = ImageFont.truetype("./fonts/PT_Sans-Regular.ttf", word_size)

    # while a valid placement for word hasn't been found
    valid = False
    while not valid:
        # Places each word on the canvas, draws a rectangle around it
        coords = (random.randint(0,500), random.randint(0,500))
        word_box_size = font.getsize(word)

        # Checks whether the box surrounding thwe word is within the bounds of the canvas
        word_box = (coords[0] - CONST_SCALE, coords[1]), (coords[0] + word_box_size[0] + CONST_SCALE, coords[1] + word_box_size[1])
        if word_box[0][0] < IMAGE_WIDTH and word_box[1][0] < IMAGE_WIDTH:
            if word_box[0][1] < IMAGE_HEIGHT and word_box[1][1] < IMAGE_HEIGHT:
                valid = True

        # AABB (Axis Aligned Bounding Box) Tree to determine whether word box collides with a word that's already been placed.
        limits = [(word_box[0][0], word_box[1][0]), (word_box[0][1], word_box[1][1])]
        aabb = AABB(limits)
        if tree.does_overlap(aabb):
            valid = False

    tree.add(aabb, word)

    draw.rectangle(word_box, outline=(255,0,0), width=1)
    draw.text(coords, word, FONT_COLOUR, font=font)
    #sys.exit()

img.save(IMG_FILEPATH)

