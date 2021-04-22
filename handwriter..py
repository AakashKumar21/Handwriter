from PIL import ImageFont, Image, ImageDraw
from random import randrange
from math import log, sin

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
line_gap_entropy_max = 20
current_page = 0
margin_x = 10
margin_y = 10
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
letter_entropy_percent = 6
word_entropy_percent = 4
letter_entropy_max = int((letter_entropy_percent/100) * font_size)
word_entropy_max = int((word_entropy_percent/100) * font_size)

# Starting pos
pos_x = margin_x
pos_y = margin_y

# Create Objects and page
font = ImageFont.truetype('myfont.ttf', font_size)
img = Image.new('RGB', page_res["normal"], color = page_color)
draw = ImageDraw.Draw(img)

def create_page():
    global pos_x
    global pos_y
    global img
    global draw
    img = Image.new('RGB', page_res["normal"], color = page_color)
    draw = ImageDraw.Draw(img)
    pos_x = margin_x
    pos_y = margin_y


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
    y = line_slope*(_x**(1/4)) - ( sin(_x/line_sin_para_div) / line_sin_div)
    # y = line_slope*(_x**(line_slope_x_power) - sin(-_x/200) ) - sin(_x)
    return y 

def insert_new_line():
    global pos_x
    global pos_y
    pos_y += line_gap_min + randrange(-line_gap_entropy_max, line_gap_entropy_max)
    pos_x = margin_x

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
        print("LINE FULL")
    
    if pos_y >= page_res["normal"][1]:
        save_image("test" + str(current_page))
        current_page += 1
        create_page()
        print("PAGE FULL")

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