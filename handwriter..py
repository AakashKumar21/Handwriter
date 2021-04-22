from PIL import ImageFont, Image, ImageDraw
from random import randrange
from math import log

font_size = 34
page_res = {"normal":(800,1128), "high":(1200,1692)}
page_color = (255,255,255)
text_color = (0,0,0)
word_space = 3
letter_space = 4
letter_entropy_percent = 10
word_entropy_percent = 10
letter_entropy_max = int((letter_entropy_percent/100) * font_size)
word_entropy_max = int((letter_entropy_percent/100) * font_size)
pos_x = 10
pos_y = 10
font = ImageFont.truetype('myfont.ttf', font_size)
img = Image.new('RGB', page_res["normal"], color = page_color)
draw = ImageDraw.Draw(img)

def print_info():
    print("HANDWRITER")
    print("Page Res: ", page_res)
    print("page_color:",page_color)
    print("text_color:", text_color)
    print("word_space:", word_space)
    print("letter_space:",letter_space )
    print("letter_entropy_max:",letter_entropy_max)
    print("word_entropy_max:",word_entropy_max)
    # print("",)
    # print("",)

def test1():
    print_info()
    test_str = "Hi there i am testing full line writing test dadada aakash"
    test_str = test_str.split()
    for word in test_str:
        write_word(word)
    save_image("test")

def write_word(_word):
    global pos_x
    global pos_y
    word_height_entropy = randrange(start=-word_entropy_max,stop=word_entropy_max) + log(pos_y)
    # Write the word
    for letter in _word:
        letter_height_entropy = randrange(-letter_entropy_max,letter_entropy_max)
        total_ent = word_height_entropy + letter_height_entropy
        draw.text((pos_x, pos_y + word_height_entropy + total_ent), letter, font=font, fill=text_color)
        width, height = draw.textsize(letter)
        pos_x += width + letter_space
        # pos_y += height
    # Give space after word
    space = ' '*word_space
    draw.text((pos_x, pos_y), space, font=font, fill=text_color)
    width, height = draw.textsize(space)
    pos_x += width
    # pos_y += height


def save_image(_filename):
    img.save('images/'+_filename+'.png')

test1()