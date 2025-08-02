# Magic 8 ball
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

import sys, time
from machine import SPI, Pin
#import random

from pbk_ili9488 import Display, color565
from sprite_handler import SpriteHandler
#from sys_font import SysFont

IMG_Y = 0
CHAR_HEIGHT = 17
CHAR_SPACING = 2
SPACE_WIDTH = 4
ANSWER_X = 206
ANSWER_Y = 48
## CHARACTERS positions and sizes on sprite sheet
CHARACTERS = {
    "A" : {"img_x" : 0,"img_y" : IMG_Y,"img_w" : 10,"img_h" : CHAR_HEIGHT} ,
    "B" : {"img_x" : 13,"img_y" : IMG_Y,"img_w" : 11,"img_h" : CHAR_HEIGHT} ,
    "C" : {"img_x" : 24,"img_y" : IMG_Y,"img_w" : 11,"img_h" : CHAR_HEIGHT} ,
    "D" : {"img_x" : 37,"img_y" : IMG_Y,"img_w" : 12,"img_h" : CHAR_HEIGHT} ,
    "E" : {"img_x" : 49,"img_y" : IMG_Y,"img_w" : 12,"img_h" : CHAR_HEIGHT} ,
    "F" : {"img_x" : 61,"img_y" : IMG_Y,"img_w" : 11,"img_h" : CHAR_HEIGHT} ,
    "G" : {"img_x" : 72,"img_y" : IMG_Y,"img_w" : 12,"img_h" : CHAR_HEIGHT} ,
    "H" : {"img_x" : 86,"img_y" : IMG_Y,"img_w" : 12,"img_h" : CHAR_HEIGHT} ,
    "I" : {"img_x" : 99 ,"img_y" : IMG_Y,"img_w" : 4,"img_h" : CHAR_HEIGHT} ,
    "J" : {"img_x" : 104,"img_y" : IMG_Y,"img_w" : 11,"img_h" : CHAR_HEIGHT} ,
    "K" : {"img_x" : 116,"img_y" : IMG_Y,"img_w" : 12,"img_h" : CHAR_HEIGHT} ,
    "L" : {"img_x" : 128,"img_y" : IMG_Y,"img_w" : 12,"img_h" : CHAR_HEIGHT} ,
    "M" : {"img_x" : 140,"img_y" : IMG_Y,"img_w" : 15,"img_h" : CHAR_HEIGHT} ,
    "N" : {"img_x" : 157,"img_y" : IMG_Y,"img_w" : 10,"img_h" : CHAR_HEIGHT} ,
    "O" : {"img_x" : 168,"img_y" : IMG_Y,"img_w" : 13,"img_h" : CHAR_HEIGHT} ,
    "P" : {"img_x" : 182,"img_y" : IMG_Y,"img_w" : 11,"img_h" : CHAR_HEIGHT} ,
    "Q" : {"img_x" : 193,"img_y" : IMG_Y,"img_w" : 13,"img_h" : CHAR_HEIGHT} ,
    "R" : {"img_x" : 207,"img_y" : IMG_Y,"img_w" : 12,"img_h" : CHAR_HEIGHT} ,
    "S" : {"img_x" : 219,"img_y" : IMG_Y,"img_w" : 10,"img_h" : CHAR_HEIGHT} ,
    "T" : {"img_x" : 229,"img_y" : IMG_Y,"img_w" : 12,"img_h" : CHAR_HEIGHT} ,
    "U" : {"img_x" : 241,"img_y" : IMG_Y,"img_w" : 12,"img_h" : CHAR_HEIGHT} ,
    "V" : {"img_x" : 253,"img_y" : IMG_Y,"img_w" : 11,"img_h" : CHAR_HEIGHT} ,
    "W" : {"img_x" : 264,"img_y" : IMG_Y,"img_w" : 16,"img_h" : CHAR_HEIGHT} ,
    "X" : {"img_x" : 281,"img_y" : IMG_Y,"img_w" : 10,"img_h" : CHAR_HEIGHT} ,
    "Y" : {"img_x" : 291,"img_y" : IMG_Y,"img_w" : 11,"img_h" : CHAR_HEIGHT} ,
    "Z" : {"img_x" : 303,"img_y" : IMG_Y,"img_w" : 10,"img_h" : CHAR_HEIGHT} ,
    "." : {"img_x" : 313,"img_y" : IMG_Y,"img_w" : 4,"img_h" : CHAR_HEIGHT} ,
    "," : {"img_x" : 316,"img_y" : IMG_Y,"img_w" : 3,"img_h" : CHAR_HEIGHT} ,
    "'" : {"img_x" : 319,"img_y" : IMG_Y,"img_w" : 2,"img_h" : CHAR_HEIGHT} ,
    "-" : {"img_x" : 322,"img_y" : IMG_Y,"img_w" : 4,"img_h" : CHAR_HEIGHT}
    }
ANSWER_COUNT = 20   # Need to adjust if the number of answer changes
GREETING_IDX = ANSWER_COUNT
GOODBYE_IDX = ANSWER_COUNT + 1
BUTTONS_IDX = ANSWER_COUNT + 2
## answers
# x_off/y_off are relative to ANSWER_X/ANSWER_Y
ANSWER_LINES = [
    {
    "lines" : [
        {"x_off" : 90,"y_off" : 90,"text" : "IT IS"} ,
        {"x_off" : 70,"y_off" : 120,"text" : "CERTAIN."}]
    } ,
    {
    "lines" : [
        {"x_off" : 90,"y_off" : 90,"text" : "IT IS"} ,
        {"x_off" : 40,"y_off" : 120,"text" : "DECIDEDLY SO."}]
    } ,
    {
    "lines" : [
        {"x_off" : 68,"y_off" : 90,"text" : "WITHOUT"} ,
        {"x_off" : 70,"y_off" : 120,"text" : "A DOUBT."}]
    } ,
    {
    "lines" : [
        {"x_off" : 94,"y_off" : 90,"text" : "YES"} ,
        {"x_off" : 56,"y_off" : 120,"text" : "DEFINITELY."}]
    } ,
    {
    "lines" : [
        {"x_off" : 70,"y_off" : 90,"text" : "YOU MAY"} ,
        {"x_off" : 58,"y_off" : 120,"text" : "RELY ON IT."}]
    } ,
    {
    "lines" : [
        {"x_off" : 94,"y_off" : 90,"text" : "AS I"} ,
        {"x_off" : 54,"y_off" : 120,"text" : "SEE IT, YES."}]
    } ,
    {
    "lines" : [
        {"x_off" : 44,"y_off" : 120,"text" : "MOST LIKELY."}]
    } ,
    {
    "lines" : [
        {"x_off" : 64,"y_off" : 90,"text" : "OUTLOOK"} ,
        {"x_off" : 82,"y_off" : 120,"text" : "GOOD."}]
    } ,
    {
    "lines" : [
        {"x_off" : 96,"y_off" : 96,"text" : "YES."}]
    } ,
    {
    "lines" : [
        {"x_off" : 54,"y_off" : 100,"text" : "SIGNS POINT"} ,
        {"x_off" : 74,"y_off" : 130,"text" : "TO YES."}]
    } ,
    {
    "lines" : [
        {"x_off" : 86,"y_off" : 90,"text" : "DON'T"} ,
        {"x_off" : 50,"y_off" : 120,"text" : "COUNT ON IT"}]
    },
    {
    "lines" : [
        {"x_off" : 62,"y_off" : 100,"text" : "MY REPLY"} ,
        {"x_off" : 86,"y_off" : 130,"text" : "IS NO"}]
    } ,
    {
    "lines" : [
        {"x_off" : 50,"y_off" : 106,"text" : "MY SOURCES"} ,
        {"x_off" : 80,"y_off" : 136,"text" : "SAY NO"}]
    } ,
    {
    "lines" : [
        {"x_off" : 66,"y_off" : 90,"text" : "OUTLOOK"} ,
        {"x_off" : 46,"y_off" : 120,"text" : "NOT SO GOOD"}]
    } ,
    {
    "lines" : [
        {"x_off" : 90,"y_off" : 90,"text" : "VERY"} ,
        {"x_off" : 60,"y_off" : 120,"text" : "DOUBTFUL"}]
    } ,
    {
    "lines" : [
        {"x_off" : 62,"y_off" : 90,"text" : "ASK AGAIN"} ,
        {"x_off" : 76,"y_off" : 120,"text" : "LATER."}]
    } ,
    {
    "lines" : [
        {"x_off" : 50,"y_off" : 102,"text" : "BETTER NOT"} ,
        {"x_off" : 36,"y_off" : 132,"text" : "TELL YOU NOW."}]
    } ,
    {
    "lines" : [
        {"x_off" : 76,"y_off" : 90,"text" : "CANNOT"} ,
        {"x_off" : 43,"y_off" : 120,"text" : "PREDICT NOW."}]
    } ,
    {
    "lines" : [
        {"x_off" : 40,"y_off" : 114,"text" : "CONCENTRATE"} ,
        {"x_off" : 38,"y_off" : 144,"text" : "AND ASK AGAIN."}]
    } ,
    {
    "lines" : [
        {"x_off" : 50,"y_off" : 104,"text" : "REPLY HAZY,"} ,
        {"x_off" : 60,"y_off" : 136,"text" : "TRY AGAIN."}]
    } ,
    ## These are not magic 8 ball answers
    {
    "lines" : [
        {"x_off" : 40,"y_off" : 114,"text" : "CONCENTRATE"} ,
        {"x_off" : 62,"y_off" : 144,"text" : "THEN ASK"}]
    } ,
    {
    "lines" : [
        {"x_off" : 66,"y_off" : 114,"text" : "GOODBYE,"} ,
        {"x_off" : 18,"y_off" : 144,"text" : "HOPE THIS HELPED"}]
    } ,
    {
    "lines" : [
        {"x_off" : -200,"y_off" : 250,"text" : "BUTTONS  SHAKE, QUIT"}]
    }
    ]

################################################################################

display = None
get_answer_button = None
quit_button = None
answer_chars = None

#---------------------------------------------------------

def display_answer_char (char : str ,  # length = 1
                         x_pos : int ,
                         y_pos : int) :
    if char == " " :
        return SPACE_WIDTH
    if char not in CHARACTERS :
        return 0
    char_data = CHARACTERS [char]
    char_image = answer_chars.get_sprite (
                    char_data ["img_x"] ,
                    char_data ["img_y"] ,
                    char_data ["img_w"] ,
                    char_data ["img_h"])
    display.draw_sprite (char_image, x_pos, y_pos,
                                     char_data ["img_w"], char_data ["img_h"])
    return char_data ["img_w"]   # returns character pixel width
def display_answer_string (ans_str : str ,
                           x_pos : int,
                           y_pos:  int) :
    x = x_pos
    y = y_pos
    for char in ans_str :
        x += display_answer_char (char, x, y) + CHAR_SPACING
def display_answer (answer_index : int) :
    clear_answer ()
    time.sleep (0.2)
    answer = ANSWER_LINES [answer_index]
    for line in answer["lines"] :
        display_answer_string (line["text"],
                               ANSWER_X + line["x_off"] ,
                               ANSWER_Y + line["y_off"])
def get_answer () :
    display_answer (time.ticks_ms () % ANSWER_COUNT)
    #display_answer (random.randint (0, (len (ANSWER_LINES) - 1)))
def clear_answer  () :
    display.draw_image("magic8ans227x200.raw", x=ANSWER_X, y=ANSWER_Y, w=227, h=200)

def initialize_display () :
    global display
    global get_answer_button
    global quit_button
    global answer_chars
    spi = SPI(0,
              baudrate=100_000_000, sck=Pin(2),
              mosi=Pin(3),
              phase=0,
              polarity=0)
    display = Display (spi = spi ,
                         cs = Pin (5) ,
                         dc = Pin (6) ,
                         rst = Pin (7) ,
                         width = 480 ,
                         height = 320)

    #BTN1: GP15, BTN2: GP14
    get_answer_button = Pin(15, Pin.IN)
    quit_button = Pin(14, Pin.IN)

    answer_chars = SpriteHandler ()
    answer_chars.load_raw_file ("magic8char327x17.raw" ,
                            variable_size = True  ,
                            buffer_width = 327)

    display.clear (color565 (0,127,0))
    display.fill_circle(x0=320, y0=160, r=158, color=color565 (0,0,0))
    display_answer (BUTTONS_IDX)
    display_answer (GREETING_IDX)

#---------------------------------------------------------

initialize_display ()

while quit_button.value() != 0 :
    if get_answer_button.value() == 0 :
        get_answer ()       # display random answer
        time.sleep (1.3)    # debounce button input
    else :
        time.sleep (0.1)    # concentration time

display_answer (GOODBYE_IDX)
