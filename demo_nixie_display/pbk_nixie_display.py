#
################################################################################
# The MIT License (MIT)
#
# Copyright (c) 2025 Curt Timmerman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################
#
# Pico Breadboard Kit - display nixie sprites
#
import time
from machine import SPI, Pin

from pbk_ili9488 import Display, color565
from sprite_handler import SpriteHandler

SPI_ID = 0
BAUDRATE = 100_000_000
SCK_PIN = 2

CS_PIN = 5
DC_PIN = 6
RST_PIN = 7
MOSI_PIN = 3
PHASE = 0
POLARITY = 0

WHITE = color565 (255, 255, 255)

DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320

NIXIE_SPRITE_SHEET_FILE ="nixie360x98.raw"
NIXIE_SPRITE_SHEET_WIDTH = 360
NIXIE_SPRITE_SHEET_HEIGHT = 98
NIXIE_SPRITE_SHEET_ROWS = 2

NIXIE_WIDTH = 30
NIXIE_HEIGHT = 49

#-----------------------------------------
## Sprite index of decimal digits, with and without decimal point
nixie_img_idx = {
    "digit" : {      # no decimal point
        "0" : 0 ,
        "1" : 1 ,
        "2" : 2 , 
        "3" : 3 ,
        "4" : 4 ,
        "5" : 5 ,
        "6" : 6 ,
        "7" : 7 ,
        "8" : 8 ,
        "9" : 9 ,
        " " : 10 ,
        "-" : 11 ,
        "+" : 10      # No "+", blank it out
        } ,
    "digitdp" : {     # with decimal point
        "0" : 12 ,
        "1" : 13 ,
        "2" : 14 , 
        "3" : 15 ,
        "4" : 16 ,
        "5" : 17 ,
        "6" : 18 ,
        "7" : 19 ,
        "8" : 20 ,
        "9" : 21 ,
        " " : 22 ,
        "-" : 23 ,
        "+" : 22
        }
    }

## display_nixie  - returns an array of nixie image indexes representing nbr_str
def display_nixie (num_str, nixie_len = None) :
    #print (f"num_str:'{num_str}'")
    formatted = num_str
    if nixie_len is not None:
        formatted = adjust_nixie_str (formatted, nixie_len)
    nixie_idx_list = []
    flen = len (formatted)
    #print (f"flen:{flen}")
    digit_idx = 0
    while digit_idx < flen : #in range (0,flen - 0) :
        #print (f"digit_idx:{digit_idx}")
        if formatted [digit_idx] == "." :
            digit_idx += 1                      # skip decimal point
        image_group = nixie_img_idx["digit"]        # default No DP
        if digit_idx < (flen - 1) :
            if formatted [digit_idx + 1] == "." :
                image_group = nixie_img_idx["digitdp"] # digit + DP
        nixie_idx_list.append (image_group [str(formatted[digit_idx])])
        digit_idx += 1
    #print (nixie_idx_list)
    return nixie_idx_list
## end display_nixie #

def adjust_nixie_str (number_str, nixie_len) :
    formatted = number_str
    #print (f"number_str: '{formatted}'")
    formatted_len = len (formatted)
    #print (formatted_len, nixie_len)
    if formatted_len < nixie_len :
        formatted = " " * (nixie_len - formatted_len) + formatted
        if '.' in formatted :
            formatted = " " + formatted
        #print (f"<len:{formatted}")
    else :
        if '.' in formatted :
            formatted = " " + formatted
            #formatted_len -= 1
        if formatted_len > nixie_len :
            #print (formatted)
            formatted = formatted [(formatted_len - nixie_len):]
            #print (f">len:{formatted}")
    return formatted
## end adjust_nixie_str #

#######################################################################

spi = SPI (SPI_ID,
            baudrate = BAUDRATE,
            sck = Pin(SCK_PIN),
            mosi = Pin(MOSI_PIN),
            phase = PHASE,
            polarity = POLARITY)

display = Display (spi = spi ,
                    cs = Pin (CS_PIN) ,
                    dc = Pin (DC_PIN) ,
                    rst = Pin (RST_PIN) ,
                    width = DISPLAY_WIDTH ,
                    height = DISPLAY_HEIGHT)

# display nixie sprite sheet
print ("Display nixie sprite sheet")
display.clear (WHITE)
x_display = 60
y_display = 100
display.draw_image(path = NIXIE_SPRITE_SHEET_FILE,
                    x = x_display, y = y_display,
                    w = NIXIE_SPRITE_SHEET_WIDTH, h = NIXIE_SPRITE_SHEET_HEIGHT)
time.sleep (2.0)

nixie_sprites = SpriteHandler ()
nixie_sprites.load_raw_file (NIXIE_SPRITE_SHEET_FILE ,
                            image_width = NIXIE_WIDTH ,
                            image_height = NIXIE_HEIGHT ,
                            image_rows = NIXIE_SPRITE_SHEET_ROWS)

# display nixie number values
print ("Display nixie number examples")
display.clear (WHITE)
nixie_values = [
    100.00 ,
    "0" , 
    1495.0 ,
    -500.25 ,
    "991234567890.1234" ,
    -25.7654
    ]
nixie_images = []
nixie_length = 15
## create an array of nixie image indexes for each example number
for _, number in enumerate (nixie_values) :
    if type (number) is str :
        formatted = number
    else :
        formatted = f"{number:.2f}"
    nixie_images.append (display_nixie (formatted, nixie_length))
#
col_start = 14
row_start = 8
for row_idx, nixie_image in enumerate (nixie_images) :
    row_offset = row_start + (row_idx * NIXIE_HEIGHT) + row_idx
    for col_idx, digit_index in enumerate (nixie_image) :
        col_offset = (col_idx * NIXIE_WIDTH) + col_start
        display.draw_sprite (nixie_sprites [digit_index],  # access sprite by index 
                            x = col_offset,                # screen position
                            y = row_offset,
                            w = NIXIE_WIDTH,               # nixie image dimensions
                            h = NIXIE_HEIGHT)
