from PIL import ImageFont, Image, ImageDraw
from random import randrange
from math import log, sin
from os import listdir, curdir
from config import *

# Font and Page
page_res = {"normal": (800, 1128), "high": (1200, 1692)}
line_gap_min = FONT_SIZE + LINE_GAP
line_gap_entropy_max = LINE_GAP_ENTROPY_PC - 5
current_page = 0
# line_gap_entropy_max = int(line_gap_entropy_percent/100) * font_size

# Line Related
line_slope_entropy_max = int(
    (LINE_SLOPE_ENTROPY_PC/100) * FONT_SIZE/LINE_SLOPE_ENTROPY_FONT_DIV)

# Letter and Word Entropy
letter_entropy_max = int((LETTER_ENTROPY_PC/100) * FONT_SIZE)
word_entropy_max = int((WORD_ENTROPY_PC/100) * FONT_SIZE)

# Check entropy
if line_gap_entropy_max <= 0:
    line_gap_entropy_max = 1
if line_slope_entropy_max <= 0:
    line_slope_entropy_max = 1
if letter_entropy_max <= 0:
    letter_entropy_max = 1
if word_entropy_max <= 0:
    word_entropy_max = 1

# Starting pos
pos_x = MARGIN_LEFT
pos_y = MARGIN_TOP

# Counters
count_page = 0
count_lines = 1

# Random Noise
max_dot_rad = 10
num_of_dots = 100

# Background
background_entropy = 4
path = "images\\random_bg\\"

# File Names
filename = ""
img_list = []


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
    width, height = 0, 0
    for row in range(background_entropy*background_entropy):
        for col in range(4):
            bg_img = Image.open(path + bg_parts[randrange(len(bg_parts))])
            img.paste(bg_img, (pos_x, pos_y))
            width, height = bg_img.size
            pos_x += width
        pos_x = 0
        pos_y += height


# Create Objects and page
font = ImageFont.truetype(font_name, FONT_SIZE)
img = Image.new('RGB', page_res["normal"], color=PAGE_COLOR)
draw = ImageDraw.Draw(img)
create_bg()


def create_page():
    global pos_x
    global pos_y
    global img
    global draw
    global count_page
    img = Image.new('RGB', page_res["normal"], color=PAGE_COLOR)
    draw = ImageDraw.Draw(img)
    create_bg()
    pos_x = MARGIN_LEFT
    pos_y = MARGIN_TOP
    count_page += 1


def start_writing(_filename):
    f = open(_filename, 'r')
    file_lines_list = f.read().split('\n')  # GET LINES
    for line in file_lines_list:
        # print("LINE: ")
        for word in line.split():
            # print("WORD: ")
            write_word(word)
        insert_new_line()
    save_image(filename + str(current_page))

# returns a y point for x input


def get_ypos(_x):
    if LINE_SLANTNNG_STLYE == 0:
        y = 0
    elif LINE_SLANTNNG_STLYE == 1:
        y = LINE_SLOPE*(_x**(1/4) - (sin((_x+60)/15))/4)
    elif LINE_SLANTNNG_STLYE == 2:
        y = LINE_SLOPE*(_x**(1/5)) - (sin(_x/LINE_SIN_PARA_DIV) / LINE_SIN_DIV)
    elif LINE_SLANTNNG_STLYE == 3:
        y = LINE_SLOPE*(_x**LINE_SLOPE_X_POWER - sin(-_x/200)) - sin(_x)
    else:
        y = custom_formula(_x)
    return y


def insert_new_line():
    global pos_x
    global pos_y
    global count_lines
    pos_y += line_gap_min + \
        randrange(-line_gap_entropy_max, line_gap_entropy_max)
    pos_x = MARGIN_LEFT
    count_lines += 1


def print_info():
    print("HANDWRITER")
    print("Page Res: ", page_res)
    print("page_color:", PAGE_COLOR)
    print("text_color:", TEXT_COLOR)
    print("word_space:", WORD_SPACE)
    print("letter_space:", LETTER_SPACE)
    print("letter_entropy_max:", letter_entropy_max)
    print("word_entropy_max:", word_entropy_max)
    print("line_slope:", LINE_SLOPE)
    print("line_var_a:", LINE_VAR_A)
    print("line_sin_para_div", LINE_SIN_DIV)
    print("line_slope_entropy_percent:", LINE_SLOPE_ENTROPY_PC)
    print("line_slope_entropy_font_div:", LINE_SLOPE_ENTROPY_FONT_DIV)
    print("line_slope_entropy_max:", line_slope_entropy_max)
    print("line_slope_x_power", LINE_SLOPE_X_POWER)
    # print("",)


def test1():
    print_info()
    test_str = "A pixel font is a font that looks crisp/aliased on the screen; a pixel is either black (or any other color) or white (or any other color); not shaded in between - maximum contrast. A bitmap font is by definition a pixel font, but an outline font can be a pixel font as well."
    test_str = test_str.split()
    for word in test_str:
        write_word(word)
    save_image(filename + str(current_page))
    # Writeline test


def write_word(_word):
    # print(_word)
    global pos_x
    global pos_y
    global current_page

    # Check if line if full
    width, height = draw.textsize(_word, font=font)
    # Width full go to next line
    if (width + pos_x + MARGIN_RIGHT) >= page_res["normal"][0]:
        insert_new_line()
        # print("LINE FULL")

    # Check if page is full
    if (pos_y + MARGIN_BOTTOM) >= page_res["normal"][1]:
        save_image(filename + str(current_page))
        current_page += 1
        create_page()
        # print("PAGE FULL")

    word_ypos_entropy = randrange(-word_entropy_max,
                                  word_entropy_max) + log(pos_y) + get_ypos(pos_x)
    # Write the word
    for letter in _word:
        letter_height_entropy = randrange(-letter_entropy_max,
                                          letter_entropy_max)
        total_ent = word_ypos_entropy + letter_height_entropy
        width, height = draw.textsize(letter, font=font)
        draw.text((pos_x, pos_y + word_ypos_entropy + total_ent),
                  letter, font=font, fill=TEXT_COLOR)
        pos_x += width + LETTER_SPACE
        # pos_y += height
    # Give space after word
    space = ' '*WORD_SPACE
    draw.text((pos_x, pos_y), space, font=font, fill=TEXT_COLOR)
    width, height = draw.textsize(space, font=font)
    pos_x += width
    # pos_y += height
    return 0


def save_image(_filename):
    img_dir = 'images/'
    img.save(img_dir + _filename + '.png')
    img_list.append(img_dir + filename + str(current_page) + '.png')


def save_pdf(_filename):
    print("Creating PDF")
    image_object_list = []
    print("Adding Image:", img_list[0])
    img = Image.open(img_list[0])  # will hold a single image object
    img_list.pop(0)

    for fname in img_list:
        print("Adding Image:", fname)
        image_object_list.append(Image.open(fname))
    img.save('pdf/' + _filename + '.pdf', save_all=True,
             append_images=image_object_list)


def get_texts_and_write():
    # Get file names
    global filename
    global img_list
    text_files_list = []
    all_files = listdir(curdir)
    print("Text Files Found:")
    for fil in all_files:
        if ".txt" in fil:
            text_files_list.append(fil)
            print(fil)

    # For each file create images
    for textfile in text_files_list:
        img_list.clear()
        filename = textfile.replace(".txt", '') + '_'
        start_writing(textfile)
        save_pdf(filename)


create_page()
get_texts_and_write()
# test1()
print("Created: Pages:{}, Lines:{}".format(str(count_page), str(count_lines)))
