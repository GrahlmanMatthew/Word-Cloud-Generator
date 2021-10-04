import sys
import random
from PIL import Image, ImageFont, ImageDraw
from wordcloud.stopwords import set_stopwords
from wordcloud.vocabulary import create_vocab
from wordcloud.grid import GridGenerator, center_word_in_square
from aabbtree import AABB, AABBTree

# TO DO
# 1. RANDOMIZE FONT SELECTION
# 2. MAKE FONT SIZE MULTIPLIER DYNAMIC
# 3. MAKE WORD PLACEMENT FAVOUR THE CENTER OF THE CANVAS
# 4. CLEAN UP IMAGE GENERATION [wip]
# 5. REFACTOR WORD PLACEMENT GRID [wip]
# 6. REFACTOR WORD BOUNDS 
# 7. REFACTOR WORD CLOUD GENERATION

# WORD CLOUD INPUT PARAMS
NUM_WORDS = 32
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

# CREATES WORDCLOUD BOUNDS DETECTION IMAGE
IMG1_FILEPATH = './output/word-bounds.png'
img1 = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='white')
draw1 = ImageDraw.Draw(img1)

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


# REFACTORING TO BE DONE YET

# Generates grid of grids and coords of potential positions to place words on these grids
grid_gen = GridGenerator(IMAGE_WIDTH, IMAGE_HEIGHT, NUM_WORDS)
grid_gen.draw_grid()
grid = grid_gen.get_grid()

#sys.exit()

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
        for sq in grid:
            word_box_size = font.getsize(word)
            new_coords = center_word_in_square(sq, word_box_size)   # centers word in current sq
            word_box = (new_coords[0] - CONST_SCALE, new_coords[1]), (new_coords[0] + word_box_size[0] + CONST_SCALE, new_coords[1] + word_box_size[1])

            # Collision detection - check whether word box overlaps with any already placed words
            limits = [(word_box[0][0], word_box[1][0]), (word_box[0][1], word_box[1][1])]
            aabb = AABB(limits)
            if not tree.does_overlap(aabb):
                if word_box[0][0] > 0 and word_box[1][0] < IMAGE_WIDTH:
                    if word_box[0][1] > 0 and word_box[1][1] < IMAGE_HEIGHT:
                        valid = True
                        grid.remove(sq)
                        tree.add(aabb, word)
                        break

    draw1.rectangle(word_box, outline=(255,0,0), width=1)
    draw.text(new_coords, word, FONT_COLOUR, font=font)
    img.save(IMG_FILEPATH)
    img1.save(IMG1_FILEPATH)

img.save(IMG_FILEPATH)
