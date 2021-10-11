import os
import random
from PIL import Image, ImageDraw

GRID_IMG_FILEPATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'output', 'grid.png'))  # DEFAULT OUTPUT PATH

# GRID GENERATOR
class GridGenerator:
    def __init__(self, image_width, image_height, num_words):
        self.grid_width = image_width
        self.grid_height = image_height
        self.num_words = num_words

        num_sq = calculate_num_squares(self.num_words)
        self.exponent = num_sq[0]
        self.num_squares = num_sq[1]

        self.grid = generate_grid_coords(self.grid_width, self.grid_height, self.num_squares, self.exponent)

    # DRAWS GRID AND OUTPUTS IT
    def draw_grid(self, grid_path=GRID_IMG_FILEPATH):
        GRID_IMG = Image.new('RGB', (self.grid_width, self.grid_height), color='white')
        draw = ImageDraw.Draw(GRID_IMG)

        # Calculates sum some grid can be drawn dynamically
        sums = []
        for x in range(0, self.exponent):
            val = pow(4, x) if x == 0 else pow(4, x) + sums[x-1]
            sums.append(val)

        # Draws grid dynamically based on num words to be placed
        num_drawn = 1
        width = pow(2, len(sums))
        rand_colour = colour()
        for square in self.grid:
            for sum in sums:
                if(num_drawn <= sum):
                    draw.rectangle(square, outline=rand_colour, width=width) 
                    if num_drawn == sum:
                        width = int(width / 2)
                        rand_colour = colour()
                    num_drawn += 1
                    break
        GRID_IMG.save(grid_path)

    def get_grid(self):
        return self.grid
    
    def get_grid_width(self):
        return self.grid_width

    def get_grid_height(self):
        return self.grid_height

    def get_grid_exponent(self):
        return self.exponent

    def get_num_squares(self):
        return self.num_squares

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
        sq2 = ((width/2 + startx, starty), (endx, height/2 + starty))
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

def generate_grid_coords(grid_width, grid_height, num_squares, exponent):
    square = ((0, 0), (grid_width, grid_height))
    square_list = []
    square_list.append(square)
    index = 0
    while len(square_list) > 0 and len(square_list) <  num_squares:
        subsquares = find_subsquares(square_list[index][0], square_list[index][1])
        for subsq in subsquares:
            square_list.append(subsq)
        index += 1

    # orders/ prioritizes squares in the grid for future word placement
    ordered_squares = []
    val, prev_val = 0, 0
    for e in range(0, exponent):
        prev_val = val
        val += pow(4, e)

        if e == 0:  # 1rst grid layer
            ordered_squares.append(square_list[val-1])
        elif e == 1 or e == 2:      # 2nd/3rd grid layers
            sublist = square_list[prev_val:val]
            for item in sublist:
                ordered_squares.append(item)
        else:       # randomize order of all other box on other grid layers
            sublist = square_list[prev_val:val]
            random.shuffle(sublist)
            for item in sublist:
                ordered_squares.append(item)
    return ordered_squares

# Generates a random RGB Colour tuple
def colour():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
