import os
from PIL import Image, ImageDraw

# DEFAULT OUTPUT PATH
GRID_IMG_FILEPATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'output', 'word-placement-grid.png'))

# GRID GENERATOR
class GridGenerator:
    def __init__(self, image_width, image_height, num_words):
        self.grid_width = image_width
        self.grid_height = image_height
        self.num_words = num_words

        num_sq = calculate_num_squares(self.num_words)
        self.exponent = num_sq[0]
        self.num_squares = num_sq[1]

        self.grid = generate_grid_coords(self.grid_width, self.grid_height, self.num_squares)

    def draw_grid(self, grid_path=GRID_IMG_FILEPATH):
        GRID_IMG = Image.new('RGB', (self.grid_width, self.grid_height), color='white')
        draw = ImageDraw.Draw(GRID_IMG)

        count = 1
        for square in self.grid:
            if count <= pow(4, 0):
                draw.rectangle(square, outline=(255,0,0), width = 12)
            elif count <= pow(4, 1) + pow(4, 0):
                draw.rectangle(square, outline=(0,255,0), width = 6)
            elif count <= pow(4, 2) + pow(4, 1) + pow(4, 0):
                draw.rectangle(square, outline=(0,0,255), width = 3)
            else:
                draw.rectangle(square, outline=(255,0,255), width = 1)
            count += 1
        GRID_IMG.save(grid_path)

    def get_grid(self):
        return self.grid
    
    def get_grid_width(self):
        return self.grid_width

    def get_grid_height(self):
        return self.grid_height

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
    width, height = square[1][0] - square[0][0], square[1][1] - square[0][1]
    word_width, word_height = word_box[0], word_box[1]
    new_width, new_height = ((width - word_width)/2) + square[0][0], ((height - word_height)/2) + square[0][1]
    return (new_width, new_height)

def calculate_num_squares(num_words):
    exp = 1
    num_squares = 1
    while num_squares < num_words:
        num_squares += pow(4, exp)
        exp += 1
    return exp, num_squares

def generate_grid_coords(grid_width, grid_height, num_squares):
    square = ((0, 0), (grid_width, grid_height))
    square_list = []
    square_list.append(square)
    index = 0
    while len(square_list) > 0 and len(square_list) <  num_squares:
        subsquares = find_subsquares(square_list[index][0], square_list[index][1])
        for subsq in subsquares:
            square_list.append(subsq)
        index += 1
    return square_list
