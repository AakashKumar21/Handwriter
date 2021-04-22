from PIL import ImageFont, Image, ImageDraw
from random import randrange
from math import log, sin
from os import listdir

# Font and Page
font_size = 34
page_res = {"normal":(800,1128), "high":(1200,1692)}
page_color = (255,255,255)
text_color = (0,0,0)
word_space = 3
letter_space = 4
line_gap = 7
line_gap_entropy_percent = 15
line_gap_min = font_size + line_gap
line_gap_entropy_max = 10
current_page = 0
margin_x = 10
margin_y = 10
margin_y_bottom = 80
# line_gap_entropy_max = int(line_gap_entropy_percent/100) * font_size

# Line Related
line_slope = 3
line_var_a = 0
line_sin_para_div = 10
line_sin_div = 2
line_slope_x_power = 1/3
line_slope_entropy_percent = 5
line_slope_entropy_font_div = 3.5
line_slope_entropy_max = int((line_slope_entropy_percent/100) * font_size/line_slope_entropy_font_div)

# Letter and Word Entropy
letter_entropy_percent = 3
word_entropy_percent = 3
letter_gap = 1
letter_entropy_max = int((letter_entropy_percent/100) * font_size)
word_entropy_max = int((word_entropy_percent/100) * font_size)

# Check entropy
if line_gap_entropy_max == 0:
    line_gap_entropy_max = 1
if line_slope_entropy_max == 0:
    line_slope_entropy_max = 1
if letter_entropy_max == 0:
    letter_entropy_max = 1
if word_entropy_max == 0:
    word_entropy_max = 1

# Starting pos
pos_x = margin_x
pos_y = margin_y

# Counters
count_page = 0
count_lines = 1

# Random Noise
max_dot_rad = 10
num_of_dots = 100

# Background
background_entropy = 4
path = "images\\random_bg\\"


def create_bg():
    global img
    # Get file names
    bg_parts = []
    if background_entropy == 4:
        all_parts = listdir(path)
        for part in all_parts:
            if "cross_4" in part:
                bg_parts.append(part)

    pos_x = 0
    pos_y = 0
    for i in range(background_entropy*background_entropy):
        bg_img = Image.open(path + bg_parts[randrange(len(bg_parts))])
        img.paste(bg_img, (pos_x, pos_y))
        width, height = bg_img.size
        pos_x += width
        pos_y += height
    img.show()

# Create Objects and page
font = ImageFont.truetype('myfont.ttf', font_size)
img = Image.new('RGB', page_res["normal"], color = page_color)
draw = ImageDraw.Draw(img)
create_bg()

def add_dots():
    for i in range(num_of_dots):
        coordinate = (randrange(page_res["normal"][0]), randrange(page_res["normal"][0]), randrange(max_dot_rad), randrange(max_dot_rad))
        print(coordinate)
        # draw.ellipse(coordinate, fill=(255, 0, 0), outline=(0, 0, 0))
        draw.t
# add_dots()
# draw.ellipse((20, 20, 180, 180), fill = 'blue', outline ='blue')


def create_page():
    global pos_x
    global pos_y
    global img
    global draw
    global count_page
    img = Image.new('RGB', page_res["normal"], color = page_color)
    draw = ImageDraw.Draw(img)
    create_bg()
    pos_x = margin_x
    pos_y = margin_y
    count_page += 1
    


def start_writing(_filename):
    f = open(_filename, 'r')
    file_lines_list = f.read().split('\n') # GET LINES
    for line in file_lines_list:
        # print("LINE: ")
        for word in line.split():
            # print("WORD: ")
            write_word(word)
        insert_new_line()

# returns a y point for x input
def get_ypos(_x):
    # y = line_slope*(_x**(1/5)) - ( sin(_x/line_sin_para_div) / line_sin_div)
    # y = line_slope*(_x**(line_slope_x_power) - sin(-_x/200) ) - sin(_x)
    y = line_slope*(_x**(1/4) - (sin((_x+60)/15))/4)
    return y 

def insert_new_line():
    global pos_x
    global pos_y
    global count_lines
    pos_y += line_gap_min + randrange(-line_gap_entropy_max, line_gap_entropy_max)
    pos_x = margin_x
    count_lines += 1

def print_info():
    print("HANDWRITER")
    print("Page Res: ", page_res)
    print("page_color:",page_color)
    print("text_color:", text_color)
    print("word_space:", word_space)
    print("letter_space:",letter_space )
    print("letter_entropy_max:",letter_entropy_max)
    print("word_entropy_max:",word_entropy_max)
    print("line_slope:", line_slope)
    print("line_var_a:", line_var_a)
    print("line_sin_para_div", line_sin_div)
    print("line_slope_entropy_percent:", line_slope_entropy_percent)
    print("line_slope_entropy_font_div:", line_slope_entropy_font_div)
    print("line_slope_entropy_max:", line_slope_entropy_max)
    print("line_slope_x_power", line_slope_x_power)
    # print("",)

def test1():
    print_info()
    test_str = "A pixel font is a font that looks crisp/aliased on the screen; a pixel is either black (or any other color) or white (or any other color); not shaded in between - maximum contrast. A bitmap font is by definition a pixel font, but an outline font can be a pixel font as well."
    test_str = test_str.split()
    for word in test_str:
        write_word(word)
    save_image("test" + str(current_page))
    # Writeline test


def write_word(_word):
    # print(_word)
    global pos_x
    global pos_y
    global current_page
    # Check if line if full
    width, height = draw.textsize(_word)
    if (width + pos_x) >= page_res["normal"][0]: # Width full go to next line
        insert_new_line()
        # print("LINE FULL")
    
    # Check if page is full
    if (pos_y + margin_y_bottom) >= page_res["normal"][1]:
        save_image("test" + str(current_page))
        current_page += 1
        create_page()
        # print("PAGE FULL")

    word_ypos_entropy = randrange(-word_entropy_max, word_entropy_max) + log(pos_y) + get_ypos(pos_x)
    # Write the word
    for letter in _word:
        letter_height_entropy = randrange(-letter_entropy_max,letter_entropy_max)
        total_ent = word_ypos_entropy + letter_height_entropy
        width, height = draw.textsize(letter)
        draw.text((pos_x, pos_y + word_ypos_entropy + total_ent), letter, font=font, fill=text_color)
        pos_x += width + letter_space
        # pos_y += height
    # Give space after word
    space = ' '*word_space
    draw.text((pos_x, pos_y), space, font=font, fill=text_color)
    width, height = draw.textsize(space)
    pos_x += width
    # pos_y += height
    return 0


def save_image(_filename):
    img.save('images/'+_filename+'.png')

create_page()
# test1()
start_writing("as1.txt")
save_image("test"+str(current_page))
print("Created: Pages:{}, Lines:{}".format(str(count_page), str(count_lines)))