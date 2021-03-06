# General Settings
font_name = 'Aakash.ttf'

# Quality of output image
QUALITY = "normal"
# Font size in px
FONT_SIZE = 34
# Space between letters
LETTER_SPACE = 0
# Page color in RGB
PAGE_COLOR = (255, 255, 255)
# Text color in RGB
TEXT_COLOR = (0, 0, 0)
# Space between words
WORD_SPACE = 3
# Vertical line gap
LINE_GAP = 10
# Percentage of Randomnes in Vertical line gap
LINE_GAP_ENTROPY_PC = 15
# MARGINS
MARGIN_LEFT = 20
MARGIN_RIGHT = 20
MARGIN_TOP = 20
MARGIN_BOTTOM = 40
MARGIN_BOTTOM_MULTIPLIER_ON_PAGE_NO = 2
MARGIN_BOTTOM_PAGE_NO = 50
# Percentage of Randomnes in Letter gap
LETTER_ENTROPY_PC = 3
# Percentage of Randomnes in Word gap
WORD_ENTROPY_PC = 3


BG_TRANS_ENABLE = True
BG_TRANS_VALUE = 0.2

# Line Slope Settings
LINE_SLOPE = 2
LINE_VAR_A = 0
LINE_SIN_PARA_DIV = 10
LINE_SIN_DIV = 2
LINE_SLOPE_X_POWER = 1/3
LINE_SLOPE_ENTROPY_PC = 5
LINE_SLOPE_ENTROPY_FONT_DIV = 3.5


# Line Slanting Style
# 0: Straight line no slant
# 1: Slight slant, Best one
# 2: Style 2
# 3: Hard steep changing, not that good
# 4: Custom formula
# for example
# def custom_formula(x):
#     y = m*(x+c)
#     return y
LINE_SLANTNNG_STLYE = 1
