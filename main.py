import sys
import random
from PIL import Image, ImageFont, ImageDraw
from wordcloud.stopwords import set_stopwords
from wordcloud.vocabulary import create_vocab
from aabbtree import AABB, AABBTree
from anytree import Node, RenderTree, AnyNode
from anytree.exporter import DotExporter


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

def center_square(square):
    width = square[1][0] - square[0][0] + square[0][0]
    height = square[1][1] - square[0][1] + square[0][1]
    return(width/2, height/2)

def center_word_in_square(square, word_box):
   # print(word_box)

    width = square[1][0] - square[0][0]
    height = square[1][1] - square[0][1]
    print("square w: %s\th:%s" % (width, height))

    word_width = word_box[0]
    word_height = word_box[1]
    print("word box w: %s\th:%s" % (word_width, word_height))



    new_width = ((width - word_width)/2) + square[0][0]
    new_height = ((height - word_height)/2) + square[0][1]
    #print(new_width, new_height)
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

#center_square(square)
#print(center_square(square))
#print("center: %s" % str(center_square(square)))

# root of tree - need to generate all coords dynamically
# root = Node(square_list.pop(0))
# root = Node(((0, 0), (IMAGE_WIDTH, IMAGE_HEIGHT)))    # root has max coords
# draw.rectangle(((0, 0), (IMAGE_WIDTH, IMAGE_HEIGHT)), outline=(255,0,0), width=2)
# num_squares = 1
# squares = [((0, 0), (IMAGE_WIDTH, IMAGE_HEIGHT))]
# new_squares = find_subsquares((0, 0), (IMAGE_WIDTH, IMAGE_HEIGHT))
# for square in new_squares:
#     draw.rectangle(square, outline=(0,255,0), width = 3)

# 2nd row in tree
# tl = Node(((0, 0), (IMAGE_WIDTH/2, IMAGE_HEIGHT/2)), parent=root)
# tr = Node(((IMAGE_WIDTH/2, 0), (IMAGE_WIDTH, IMAGE_HEIGHT/2)), parent=root)
# bl = Node(((0, IMAGE_HEIGHT/2), (IMAGE_WIDTH/2, IMAGE_HEIGHT)), parent=root)
# br = Node(((IMAGE_WIDTH/2, IMAGE_HEIGHT/2), (IMAGE_WIDTH, IMAGE_HEIGHT)), parent=root)

# # for pre, fill, node in RenderTree(root):
# #     print("%s%s" % (pre, node.name))

# print("\n%s" % RenderTree(root))

# DRAW WORDS
tree = AABBTree()
new_tree =  AABBTree()
while len(vocab) > 0:
    # info about the word
    word_tuple = vocab.popitem()
    word = word_tuple[0]
    word_size = vocab_sizes[word]
    font = ImageFont.truetype("./fonts/PT_Sans-Regular.ttf", word_size)

    # while a valid placement for word hasn't been found
    valid = False
    while not valid:

        # need to   change my  center square functiont o place a word there, not just return center...
        for sq in square_list:
            coords = center_square(sq)

            word_box_size = font.getsize(word)
           #print("wbs: %s" % str(word_box_size))

            new_coords = center_word_in_square(sq, word_box_size)
            print(word, new_coords, sq)
            
            word_box = (coords[0] - CONST_SCALE, coords[1]), (coords[0] + word_box_size[0] + CONST_SCALE, coords[1] + word_box_size[1])
            word_box = (new_coords[0] - CONST_SCALE, new_coords[1]), (new_coords[0] + word_box_size[0] + CONST_SCALE, new_coords[1] + word_box_size[1])

            limits = [(word_box[0][0], word_box[1][0]), (word_box[0][1], word_box[1][1])]
            aabb = AABB(limits)
            if not tree.does_overlap(aabb):
                #print(coords)
                if word_box[0][0] > 0 and word_box[1][0] < IMAGE_WIDTH:
                    if word_box[0][1] > 0 and word_box[1][1] < IMAGE_HEIGHT:
                        print("valid %s" %  str(new_coords))
                        valid = True
                        square_list.remove(sq)
                        tree.add(aabb, word)
                        break

            print("")

    draw.rectangle(word_box, outline=(255,0,0), width=1)
    draw.text(new_coords, word, FONT_COLOUR, font=font)
    
    img.save(IMG_FILEPATH)
    #sys.exit()
print(tree)

        # spatial indexing with quadtrees
        # Places each word on the canvas, draws a rectangle around it    
        # coords = (random.randint(0,500), random.randint(0,500))
        # word_box_size = font.getsize(word)

        # # Checks whether the box surrounding thwe word is within the bounds of the canvas
        # word_box = (coords[0] - CONST_SCALE, coords[1]), (coords[0] + word_box_size[0] + CONST_SCALE, coords[1] + word_box_size[1])
        # if word_box[0][0] < IMAGE_WIDTH and word_box[1][0] < IMAGE_WIDTH:
        #     if word_box[0][1] < IMAGE_HEIGHT and word_box[1][1] < IMAGE_HEIGHT:
        #         valid = True

        # # AABB (Axis Aligned Bounding Box) Tree to determine whether word box collides with a word that's already been placed.
        # limits = [(word_box[0][0], word_box[1][0]), (word_box[0][1], word_box[1][1])]
        # aabb = AABB(limits)
        # if tree.does_overlap(aabb):
        #     valid = False
        # else:
        #     valid = True

    #tree.add(aabb, word)


   # sys.exit()

img.save(IMG_FILEPATH)

