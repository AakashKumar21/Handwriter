from PIL import ImageFont, Image, ImageDraw
from random import randrange
from math import log, sin
from os import listdir, curdir, remove
from config import *
import sys
from progress.bar import Bar,IncrementalBar,ChargingBar

PAGE_RES = {"normal": (800, 1128), "high": (1200, 1692)}


# Check entropy and assing 1 if less or equal to 0
def _sanitize_entropy_var():  
    global LINE_GAP_ENTROPY_MAX
    global LINE_SLOPE_ENTROPY_MAX
    global LETTER_ENTROPY_MAX
    global WORD_ENTROPY_MAX 
    if LINE_GAP_ENTROPY_MAX <= 0:
        LINE_GAP_ENTROPY_MAX = 1
    if LINE_SLOPE_ENTROPY_MAX <= 0:
        LINE_SLOPE_ENTROPY_MAX = 1
    if LETTER_ENTROPY_MAX <= 0:
        LETTER_ENTROPY_MAX = 1
    if WORD_ENTROPY_MAX <= 0:
        WORD_ENTROPY_MAX = 1


# Line Related
def set_max_entropy_values():
    global LINE_SLOPE_ENTROPY_MAX
    global LETTER_ENTROPY_MAX
    global WORD_ENTROPY_MAX
    global LINE_GAP_ENTROPY_MAX
    global LINE_GAP_MIN
    # Line entropy
    LINE_GAP_ENTROPY_MAX = LINE_GAP_ENTROPY_PC - 5
    LINE_SLOPE_ENTROPY_MAX = int(
        (LINE_SLOPE_ENTROPY_PC/100) * FONT_SIZE/LINE_SLOPE_ENTROPY_FONT_DIV)
    # Letter and Word Entropy
    LETTER_ENTROPY_MAX = int((LETTER_ENTROPY_PC/100) * FONT_SIZE)
    WORD_ENTROPY_MAX = int((WORD_ENTROPY_PC/100) * FONT_SIZE)
    LINE_GAP_MIN = FONT_SIZE + LINE_GAP
    # Sanitise values
    _sanitize_entropy_var()


def reset_xy_pos():
    global pos_x, pos_y
    # Starting pos
    pos_x = MARGIN_LEFT
    pos_y = MARGIN_TOP


def set_initial_values():
    global count_lines, count_page
    global background_entropy
    global current_filename, current_img_lst, current_page
    global BG_PATH, FONT, FONT_SIZE
    global current_progress
    # Counters
    count_page = 0
    count_lines = 1
    current_page = 0
    current_progress = 0
    # Background
    background_entropy = 4
    BG_PATH = "images\\random_bg\\"
    FONT = ImageFont.truetype(font_name, FONT_SIZE)
    # File Names
    current_filename = ""
    current_img_lst = []
    reset_xy_pos()


def _create_bg():
    global img
    # Get file names
    bg_parts = []
    if background_entropy == 4:
        all_parts = listdir(BG_PATH)
        for part in all_parts:
            if "cross_4" in part:
                bg_parts.append(part)

    pos_x = 0
    pos_y = 0
    width, height = 0, 0
    for row in range(background_entropy*background_entropy):
        for col in range(4):
            bg_img = Image.open(BG_PATH + bg_parts[randrange(len(bg_parts))])
            img.paste(bg_img, (pos_x, pos_y))
            width, height = bg_img.size
            pos_x += width
        pos_x = 0
        pos_y += height


def create_page():
    global pos_x
    global pos_y
    global img
    global draw
    global count_page
    count_page += 1
    # print("Page: ", count_page)
    img = Image.new('RGB', PAGE_RES["normal"], color=PAGE_COLOR)
    draw = ImageDraw.Draw(img)
    _create_bg()
    pos_x = MARGIN_LEFT
    pos_y = MARGIN_TOP

    
def letter_replacer(letter):
    if letter in ['\“','\”',"\""]:
        return '\"'
    elif letter in ['\’','\‘', '\'']:
        return '\''
    elif letter == '—':
        return '-'
    elif letter == '❟':
        return ','
    else: 
        return letter

def sanitize_text(file):
    text = file.read()
    new_text = ""
    for t in text:
        if not t.isalnum():
            new_text += letter_replacer(t)
        elif not t.isprintable():
            new_text += ' '
        elif t.isspace():
            new_text += ' '
        elif t == '…':
            return '...'
        else:
            new_text += t
    return new_text


def start_writing(_filename):
    global current_filename
    global current_progress
    global bar
    current_line = 0
    f = open(_filename, 'r', errors="ignore", encoding='utf-8')
    file_text_sanitised = sanitize_text(f)
    file_lines_list = file_text_sanitised.split('\n')  # GET LINES
    bar = ChargingBar('Processing', max=len(file_lines_list))
    for line in file_lines_list:            # For each lines
        bar.next()
        for word in line.split():           # For each words
            write_word(word)
        insert_new_line()
        current_line += 1
    bar.finish()
    save_image(current_filename + str(current_page))


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
    count_lines += 1
    # print("Line: ", count_lines)
    pos_y += LINE_GAP_MIN + \
        randrange(-LINE_GAP_ENTROPY_MAX, LINE_GAP_ENTROPY_MAX)
    pos_x = MARGIN_LEFT


def print_info():
    print("HANDWRITER")
    print("Page Res: ", PAGE_RES)
    print("page_color:", PAGE_COLOR)
    print("text_color:", TEXT_COLOR)
    print("word_space:", WORD_SPACE)
    print("letter_space:", LETTER_SPACE)
    print("letter_entropy_max:", LETTER_ENTROPY_MAX)
    print("word_entropy_max:", WORD_ENTROPY_MAX)
    print("line_slope:", LINE_SLOPE)
    print("line_var_a:", LINE_VAR_A)
    print("line_sin_para_div", LINE_SIN_DIV)
    print("line_slope_entropy_percent:", LINE_SLOPE_ENTROPY_PC)
    print("line_slope_entropy_font_div:", LINE_SLOPE_ENTROPY_FONT_DIV)
    print("line_slope_entropy_max:", LINE_SLOPE_ENTROPY_MAX)
    print("line_slope_x_power", LINE_SLOPE_X_POWER)
    # print("",)


def write_word(_word):
    # print(_word)
    global pos_x
    global pos_y
    global current_page
    global WORD_ENTROPY_MAX
    global draw

    # Check if line if full
    width, height = draw.textsize(_word, font=FONT)
    # Width full go to next line
    if (width + pos_x + MARGIN_RIGHT) >= PAGE_RES["normal"][0]:
        insert_new_line()
        # print("LINE FULL")

    # Check if page is full
    if (pos_y + MARGIN_BOTTOM + MARGIN_TOP) >= PAGE_RES["normal"][1]:
        save_image(current_filename + str(current_page))
        current_page += 1
        create_page()
        # print("PAGE FULL")

    word_ypos_entropy = randrange(-WORD_ENTROPY_MAX,
                                  WORD_ENTROPY_MAX) + log(pos_y) + get_ypos(pos_x)
    # Write the word
    for letter in _word:
        letter_height_entropy = randrange(-LETTER_ENTROPY_MAX,
                                          LETTER_ENTROPY_MAX)
        total_ent = word_ypos_entropy + letter_height_entropy
        width, height = draw.textsize(letter, font=FONT)
        draw.text((pos_x, pos_y + word_ypos_entropy + total_ent),
                  letter, font=FONT, fill=TEXT_COLOR)
        pos_x += width + LETTER_SPACE
        # pos_y += height
    # Give space after word
    space = ' '*WORD_SPACE
    draw.text((pos_x, pos_y), space, font=FONT, fill=TEXT_COLOR)
    width, height = draw.textsize(space, font=FONT)
    pos_x += width
    # pos_y += height
    return 0

def insert_page_no():
    insert_new_line()
    draw.text( (PAGE_RES['normal'][0]/2, pos_y), str(current_page+1), font=FONT, fill=TEXT_COLOR)

def save_image(_filename):
    global current_img_lst
    global count_page
    global add_page_no
    if add_page_no:
        insert_page_no()

    img_dir = 'images/'
    img.save(img_dir + _filename + '.png')
    current_img_lst.append(img_dir + current_filename + str(current_page) + '.png')


def save_pdf(_filename):
    global current_img_lst
    global count_page, count_lines, current_progress
    current_progress = 0
    print("Creating PDF: ", _filename)
    print("Pages: ", count_page)
    print("Lines: ", count_lines)
    print()
    image_object_list = []
    # print("Adding Image:", current_img_lst[0])
    img = Image.open(current_img_lst[0])  # will hold a single image object

    for fname in current_img_lst[1:]:
        # print("Adding Image:", fname)
        image_object_list.append(Image.open(fname))
    img.save('pdf/' + _filename + '.pdf', save_all=True,
             append_images=image_object_list)
    for files in current_img_lst:
        remove(files)


def get_texts_and_write(_filename):
    # Get file names
    global filename
    global current_img_lst

    current_img_lst.clear()
    current_filename = _filename.replace(".txt", '') + '_'
    start_writing(_filename)
    save_pdf(current_filename)
    set_initial_values()


if __name__ == "__main__":
    global textfile
    global count_page, count_lines
    global add_page_no
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    textfiles = [f for f in args if f.endswith('.txt')]
    fontfiles = [f for f in args if f.endswith('.ttf')]
    if 'page_no' in args:
        print("Options: Add page number")
        MARGIN_BOTTOM += MARGIN_BOTTOM*MARGIN_BOTTOM_MULTIPLIER_ON_PAGE_NO
        add_page_no = True
    if len(fontfiles) > 0:
        font_name = fontfiles[0]
    else:
        raise SystemExit("NO FONT FILE PROVIDED")
    if len(textfiles) == 0:
        raise SystemExit("NO TEXT FILE PROVIDED")
    for files in textfiles:
        set_initial_values()
        set_max_entropy_values()
        create_page()
        get_texts_and_write(files)