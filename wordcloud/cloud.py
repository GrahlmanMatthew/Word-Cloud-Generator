import os
import random
from copy import deepcopy
from aabbtree import AABB, AABBTree
from PIL import Image, ImageFont, ImageDraw
from wordcloud.grid import GridGenerator, center_word_in_square

# DEFAULT OUTPUT PATHS IF METHOD IS NOT PROVIDED OUTPUT PATHS
WC_IMG_FILEPATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'output', 'wordcloud.png'))   
WC_BOUNDS_IMG_FILEPATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'output', 'word-bounds.png'))  

# Place words in the vocabulary on the grid
def place_words(vocab, vocab_sizes, grid, grid_gen, wc_img_path=WC_IMG_FILEPATH, wc_bounds_img_path=WC_BOUNDS_IMG_FILEPATH):
    voc = deepcopy(vocab)
    voc_sizes = deepcopy(vocab_sizes)
    grd = deepcopy(grid)
    grd_width = grid_gen.get_grid_width()
    grd_height = grid_gen.get_grid_height()
    word_box_tree = AABBTree()      # for collision detection    

    # WORDCLOUD IMAGE TO OUTPUT
    WC_IMG = Image.new('RGB', (grd_width, grd_height), color='white')
    WC_DRAW = ImageDraw.Draw(WC_IMG)

    # CREATES WORDCLOUD BOUNDS DETECTION IMAGE
    WC_BOUNDS_IMG = Image.new('RGB', (grd_width, grd_height), color='white')
    WC_BOUNDS_DRAW = ImageDraw.Draw(WC_BOUNDS_IMG)

    while len(voc) > 0:
        # info about the word to be placed
        word_tuple = voc.popitem()
        word = word_tuple[0]
        word_size = voc_sizes[word]
        font = ImageFont.truetype(get_random_font_path(), word_size)

        # find valid placement for this word in the grid
        valid_placement = False
        while not valid_placement:
            for square in grd:
                word_box_size = font.getsize(word)
                coords = center_word_in_square(square, word_box_size)
                word_box = (coords[0], coords[1]), (coords[0] + word_box_size[0], coords[1] + word_box_size[1]) # add back constant here for word box padding

                aabb = AABB([(word_box[0][0], word_box[1][0]), (word_box[0][1], word_box[1][1])])   # potential node (word placement) in tree
                collides = word_box_tree.does_overlap(aabb)     # returns true if node (word placement) does not collide with already placed words

                if not collides:
                    if word_box[0][0] > 0 and word_box[1][0] < grd_width and word_box[0][1] > 0 and word_box[1][1] < grd_height:
                        valid_placement = True
                        grd.remove(square)      # removes square from grid so we can't place another word there
                        word_box_tree.add(aabb, word)
                        break  

        WC_BOUNDS_DRAW.rectangle(word_box, outline=(255,0,0), width=1)
        WC_DRAW.text(coords, word, (0, 0, 0), font=font)
        
    WC_BOUNDS_IMG.save(wc_bounds_img_path)
    WC_IMG.save(wc_img_path)

def get_random_font_path():
    FONT_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'fonts'))
    font_name = random.choice(os.listdir(FONT_DIR))
    font_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', FONT_DIR, font_name))
    return font_path
