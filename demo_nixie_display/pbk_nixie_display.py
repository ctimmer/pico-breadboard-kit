# Pico Breadboard Kit - display nixie sprites
#
import time
from machine import SPI, Pin

from pbk_ili9488 import Display, color565
from sprite_handler import SpriteHandler

NIXIE_SPRITE_SHEET ="nixie360x98.raw"
NIXIE_WIDTH = 30
NIXIE_HEIGHT = 49

#-----------------------------------------
## Sprite index of decimal digits, with and without decimal point
nixie_img_idx = {
    "digit" : {      # without decimal point
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

spi = SPI(0, baudrate=100_000_000, sck=Pin(2), mosi=Pin(3), phase=0, polarity=0)

display = Display (spi = spi ,
                 cs = Pin (5) ,
                 dc = Pin (6) ,
                 rst = Pin (7) ,
                 width = 480 ,
                 height = 320)

# display nixie sprite sheet
display.clear (color565(r=255, g=255, b=255))
display.draw_image(path=NIXIE_SPRITE_SHEET, x=20, y=20, w=360, h=98)
time.sleep (3.0)

nixie_sprites = SpriteHandler ()
nixie_sprites.load_raw_file (NIXIE_SPRITE_SHEET ,
                        image_width = NIXIE_WIDTH ,
                        image_height = NIXIE_HEIGHT ,
                        image_rows = 2)

# display nixie number values
display.clear (color565(r=255, g=255, b=255))
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
for _, number in enumerate (nixie_values) :
    if type (number) is str :
        formatted = number
    else :
        formatted = f"{number:.2f}"
    nixie_images.append (display_nixie (formatted, nixie_length))
#print (nixie_images)
col_start = 14
row_start = 12
for row_idx, nixie_image in enumerate (nixie_images) :
    row_offset = (row_idx * 49) + row_start
    for col_idx, digit_index in enumerate (nixie_image) :
        col_offset = (col_idx * 30) + col_start
        display.draw_sprite (nixie_sprites [digit_index],
                            x=col_offset,
                            y=row_offset,
                            w=30,
                            h=49)
    #break
