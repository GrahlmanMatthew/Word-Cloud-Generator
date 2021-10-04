import sys
import random
from PIL import Image, ImageFont, ImageDraw
from wordcloud.stopwords import set_stopwords
from wordcloud.vocabulary import create_vocab
from aabbtree import AABB, AABBTree

# WORD CLOUD INPUT PARAMS
NUM_WORDS = 60
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



# LAND OF NO RETURN
# EVERYTHING BELOW THIS POINT NEEDS REFACTORED BADLY 

# Find 4 subsquares within a given square, just provide start/end coords for the initial square
def find_subsquares(start_coord, end_coord):
    startx, starty = start_coord[0], start_coord[1]
    endx, endy = end_coord[0], end_coord[1]
    width = endx - startx
    height = endy - starty
    if starty == 0:
        sq1 = ((startx, starty), (width/2 + startx, height/2))
        sq2 = ((width/2 + startx, starty), (endx, height/2))
        sq3 = ((startx, height/2), (width/2 + startx, height))
        sq4 = ((width/2 + startx, height/2 + starty), (endx, endy))
    elif startx == 0:
        sq1 = ((startx, starty), (width/2, height/2 + starty))
        sq2 = ((width/2 + startx, starty), (endx, height/2 + starty))
        sq3 = ((startx, height/2 + starty), (width/2 + startx, height  + starty))
        sq4 = ((width/2 + startx, height/2 + starty), (endx, endy))
    else:
        sq1 = ((startx, starty), (width/2 + startx, height/2 + starty))
        sq2 = ((width/2 + startx, height), (endx, height/2 + starty))
        sq3 = ((startx, height/2 + starty), (width/2 + startx, height  + starty))
        sq4 = ((width/2 + startx, height/2 + starty), (endx, endy))
    return (sq1, sq2, sq3, sq4)

def center_word_in_square(square, word_box):
    width = square[1][0] - square[0][0]
    height = square[1][1] - square[0][1]

    word_width = word_box[0]
    word_height = word_box[1]

    new_width = ((width - word_width)/2) + square[0][0]
    new_height = ((height - word_height)/2) + square[0][1]

    return (new_width, new_height)


# Draw grid of squares so that in future we can try placing each word in the center of a square
square = ((0, 0), (IMAGE_WIDTH, IMAGE_HEIGHT))
square_list = [square]

exp, num_squares = 1, 1
while num_squares < NUM_WORDS:
    num_squares += pow(4, exp)
    exp += 1

# Generate all square coords pairs for placement of words
index = 0
while len(square_list) > 0 and len(square_list) <  num_squares:
    subsquares = find_subsquares(square_list[index][0], square_list[index][1])
    for subsq in subsquares:
        square_list.append(subsq)
    index += 1

# Draw subsquares once they've all been calculated
count = 1
for sq in square_list:
    if count <= pow(4, 0):
        draw.rectangle(sq, outline=(255,0,0), width = 9)
    elif count <= pow(4, 1) + pow(4, 0):
        draw.rectangle(sq, outline=(0,255,0), width = 6)
    elif count <= pow(4, 2) + pow(4, 1) + pow(4, 0):
        draw.rectangle(sq, outline=(0,0,255), width = 3)
    else:
        draw.rectangle(sq, outline=(255,0,255), width = 1)
    count += 1


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
        for sq in square_list:
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
                        square_list.remove(sq)
                        tree.add(aabb, word)
                        break

    draw.rectangle(word_box, outline=(255,0,0), width=1)
    draw.text(new_coords, word, FONT_COLOUR, font=font)
    img.save(IMG_FILEPATH)

img.save(IMG_FILEPATH)

