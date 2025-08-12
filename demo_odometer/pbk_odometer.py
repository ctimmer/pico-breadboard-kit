# -*-coding:utf-8 -*-
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


import sys
from machine import SPI, Pin
import time

from pbk_ili9488 import Display, color565
from sprite_handler import SpriteHandler
from sys_font import SysFont

SPI_ID = 0
BAUDRATE = 100_000_000
SCK_PIN = 2

CS_PIN = 5
DC_PIN = 6
RST_PIN = 7
MOSI_PIN = 3
PHASE = 0
POLARITY = 0

DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320
WHITE = color565 (255,255,255)
BLACK = color565 (0,0,0)
RED = color565 (255,0,0)
GREEN = color565 (0,255,0)
BLUE = color565 (0,0,255)
BROWN = color565 (165,42,42)
YELLOW_ORANGE = color565 (255,179,67)

ODOMETER_DIGITS = 6
ODOMETER_MOD = int (10 ** ODOMETER_DIGITS)
ODOMETER_MAX = ODOMETER_MOD - 1
ODOMETER_FORMAT = "{:0" + str (ODOMETER_DIGITS) + "d}"
ODOMETER_X = 10
ODOMETER_Y = 10
ODOMETER_DIGIT_OFFSET = 24
OD_DIGIT_FILE = "odomdigits.raw"
OD_SHEET_WIDTH = 170
OD_SHEET_HEIGHT = 20
OD_IMAGE_WIDTH = 17
OD_IMAGE_HEIGHT = 20
OD_PADDING = 2
OD_WIDTH = OD_IMAGE_WIDTH + (OD_PADDING * 2)
OD_HEIGHT = OD_IMAGE_HEIGHT + (OD_PADDING * 2)
OD_BACKGROUND = BLACK

spi = SPI(SPI_ID,
            baudrate = BAUDRATE,
            sck = Pin (SCK_PIN),
            mosi = Pin (MOSI_PIN),
            phase = PHASE,
            polarity = POLARITY)

display = Display (spi = spi ,
                    cs = Pin (CS_PIN) ,
                    dc = Pin (DC_PIN) ,
                    rst = Pin (RST_PIN) ,
                    width = DISPLAY_WIDTH ,
                    height = DISPLAY_HEIGHT)

sysfont = SysFont (display)

odom_images = SpriteHandler ()


ODOMETER = []
digit_data = {}

SCROLL_HEIGHT = 5
SCROLL_SEPARATION = 2

def scroll_digit_up (digit, scroll, odometer_digit) :
    #print ("gpi:", image_data)
    if scroll not in [1, 2, 3] :
        print (f"Invalid scroll value: {scroll}")
        return None
    next_key = "next"
    image_data = digit_data [digit]
    x_display = odometer_digit ["x_image"]
    y_display = odometer_digit ["y_image"]
    x_sprite = image_data ["x"]
    y_sprite = image_data ["y"] + ((SCROLL_HEIGHT * scroll) + SCROLL_SEPARATION)
    w_image = image_data ["w"]
    h_image = image_data ["h"] - ((SCROLL_HEIGHT * scroll) + SCROLL_SEPARATION)

    display.draw_sprite (odom_images.get_sprite (x_sprite,
                                                 y_sprite,
                                                 w_image,
                                                 h_image) ,
                            x = x_display,                # screen position
                            y = y_display,
                            w = w_image,               # image dimensions
                            h = h_image)
    #
    y_display += h_image
    #print (f"sep: y={y_display}, h={SCROLL_SEPARATION}")
    display.fill_rectangle (x=x_display, y=y_display, w=w_image, h=SCROLL_SEPARATION, color=OD_BACKGROUND)
    y_display += SCROLL_SEPARATION
    image_data = digit_data [image_data[next_key]]
    x_sprite = image_data ["x"]
    y_sprite = image_data ["y"]
    w_image = image_data ["w"]
    h_image = (SCROLL_HEIGHT * scroll) - SCROLL_SEPARATION
    #print (f"new: y={y_display}, h={h}")
    display.draw_sprite (odom_images.get_sprite (x_sprite, y_sprite, w_image, h_image) ,
                            x = x_display,                # screen position
                            y = y_display,
                            w = w_image,               # image dimensions
                            h = h_image)

# endscroll_digit_up #

def scroll_digit_down (digit, scroll, odometer_digit) :
    #print ("gpi:", odometer_digit)
    if scroll not in [1, 2, 3] :
        print (f"Invalid scroll value: {scroll}")
        return None
    '''
    display.fill_rectangle (x=odometer_digit ["x_image"],
                            y=odometer_digit ["y_image"],
                            w=OD_IMAGE_WIDTH,
                            h=OD_IMAGE_HEIGHT,
                            color=OD_BACKGROUND)
    '''
    next_key = "prev"
    image_data = digit_data [digit]
    x_display = odometer_digit ["x_image"]
    y_display = odometer_digit ["y_image"] + ((SCROLL_HEIGHT * scroll) + SCROLL_SEPARATION)
    x_sprite = image_data ["x"]
    y_sprite = image_data ["y"] # + ((SCROLL_HEIGHT * scroll) + SCROLL_SEPARATION)
    w_image = image_data ["w"]
    h_image = image_data ["h"] - ((SCROLL_HEIGHT * scroll) + SCROLL_SEPARATION)
    
    display.draw_sprite (odom_images.get_sprite (x_sprite,
                                                 y_sprite,
                                                 w_image,
                                                 h_image) ,
                            x = x_display,                # screen position
                            y = y_display,
                            w = w_image,               # image dimensions
                            h = h_image)
    
    #
    #return
    y_display -= SCROLL_SEPARATION
    #print (f"sep: y={y_display}, h={SCROLL_SEPARATION}")
    display.fill_rectangle (x=x_display, y=y_display, w=w_image, h=SCROLL_SEPARATION, color=OD_BACKGROUND)
    #return
    y_display = odometer_digit ["y_image"]
    image_data = digit_data [image_data[next_key]]
    x_sprite = image_data ["x"]
    y_sprite = image_data ["y"] + (SCROLL_HEIGHT * (4 - scroll))
    w_image = image_data ["w"]
    h_image = image_data ["h"] - (SCROLL_HEIGHT * (4 - scroll))
    #print (f"new: spr: x={x_sprite} y={y_sprite} img: w={w_image} h={h_image}")
    display.draw_sprite (odom_images.get_sprite (x_sprite, y_sprite, w_image, h_image) ,
                            x = x_display,                # screen position
                            y = y_display,
                            w = w_image,               # image dimensions
                            h = h_image)

# end scroll_digit_down #

def scroll_digit (digit, scroll_level, scroll_up, odometer_digit) :
    #print ("### scroll_digit:", digit, scroll)
    if scroll_level not in [1, 2, 3, 4] :
        print (f"Invalid scroll value: {scroll_level}")
        return None

    #image_data = digit_data [digit]
    if scroll_level >= 4 :
        ## Done  scrolling, display current digit
        next_key = "next"
        if not scroll_up :
            next_key = "prev"
        image_data = digit_data [digit]
        image_data = digit_data [image_data[next_key]]
        display.draw_sprite (odom_images.get_sprite (image_data["x"],
                                                     image_data["y"],
                                                     OD_IMAGE_WIDTH,
                                                     OD_IMAGE_HEIGHT) ,
                            x = odometer_digit ["x_image"],                # screen position
                            y = odometer_digit ["y_image"],
                            w = OD_IMAGE_WIDTH,               # image dimensions
                            h = OD_IMAGE_HEIGHT)
        return
    #
    if scroll_up :
        scroll_digit_up (digit, scroll_level, odometer_digit)
    else :
        scroll_digit_down (digit, scroll_level, odometer_digit)

# end scroll_digit #

odometer_int = 0    # current odometer reading
odometer_str = ""   # string value of odometer_int

def adjust_odometer (increment = 0) :
    global odometer_int
    odometer_int += increment
    if odometer_int > ODOMETER_MAX :
        odometer_int = 0
    elif odometer_int < 0 :
        odometer_int = ODOMETER_MAX

def odometer_init (start=0) :
    global ODOMETER
    global odometer_int
    global odometer_str
    odometer_int = start
    adjust_odometer ()
    odometer_str = ODOMETER_FORMAT.format (odometer_int) # f"{odometer_int:04d}"
    odometer_x = ODOMETER_X
    odometer_y = ODOMETER_Y
    for digit_idx in range (0, ODOMETER_DIGITS) :
        digit_pos = {
            "x_field" : odometer_x ,
            "y_field" : ODOMETER_Y ,
            "w_field" : OD_IMAGE_WIDTH + (2 * OD_PADDING) ,
            "h_field" : OD_IMAGE_HEIGHT + (2 * OD_PADDING) ,
            "x_image" : odometer_x + OD_PADDING ,
            "y_image" : ODOMETER_Y + OD_PADDING
            }
        ODOMETER.append (digit_pos)
        display.fill_rectangle (x=digit_pos["x_field"] ,
                                y=digit_pos["y_field"] ,
                                w=digit_pos ["w_field"] ,
                                h=digit_pos ["h_field"] ,
                                color=OD_BACKGROUND)
        #print (digit_pos)
        display.draw_sprite (odom_images [int (odometer_str [digit_idx])],
                                x = digit_pos["x_image"] ,
                                y = digit_pos["y_image"] ,
                                w = OD_IMAGE_WIDTH ,
                                h = OD_IMAGE_HEIGHT)
        odometer_x += ODOMETER_DIGIT_OFFSET
    ## Initialize digit data
    for img_idx in range (0,10) :
        #print (odom_images.get_index_sprite_data (img_idx))
        digit_key = str (img_idx)
        digit_data [digit_key] = odom_images.get_index_sprite_data (img_idx)
        digit_data [digit_key]["next"] = str ((img_idx + 1) % 10)
        down_digit = img_idx - 1
        if down_digit < 0 :
            down_digit = 9
        digit_data [digit_key]["prev"] = str (down_digit)

def odometer_increment (increment = 1) :
    global odometer_int
    global odometer_str
    inc_count = increment
    inc_value = 1
    inc_positive = increment >= 0
    if not inc_positive :
        inc_value = -1
        inc_count = abs (increment)
    while inc_count > 0 :
        adjust_odometer (inc_value)
        new_str = ODOMETER_FORMAT.format (odometer_int)
        ## Make a list of all digit indexes that have changed
        change_list = []
        for digit_idx, digit in enumerate (odometer_str) :
            if digit != new_str [digit_idx] :
                change_list.append (digit_idx)  # digit changed
        ## Scroll changed digits
        for scroll_level in range (1,5) :
            for digit_idx in change_list :
                scroll_digit (odometer_str [digit_idx] ,
                                scroll_level ,
                                inc_positive ,
                                ODOMETER [digit_idx])
            time.sleep (0.02)
        odometer_str = new_str
        inc_count -= 1
    
################################################################################

odom_images.load_raw_file (OD_DIGIT_FILE ,
                            image_width = OD_IMAGE_WIDTH ,
                            image_height = OD_IMAGE_HEIGHT)

display.clear (WHITE)
#display.draw_image(path=OD_DIGIT_FILE, x=10, y=10, w=OD_SHEET_WIDTH, h=OD_SHEET_HEIGHT)

odometer_init (999995)
for _ in range (20) :
    odometer_increment (5)
time.sleep (2.0)
for _ in range (30) :
    odometer_increment (-5)



