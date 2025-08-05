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
# Pico Breadboard Kit - wheel of fortune demo
#
import time
import random

from machine import SPI, Pin

from pbk_ili9488 import Display
from wheel_of_fortune import WheelOfFortune

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

def solve_it (wof) :
    delay_time = 0.2

    choices_left = []
    for char in "BCDFGHJKLMNPQRSTVWXYZ" :
        choices_left.append (char)
    while len (choices_left) > 0 :
        char = random.choice (choices_left)
        choices_left.remove (char)
        guess_result = "Good"
        guess = wof.guess_character (char)
        if not guess :
            guess_result = "Bad"
        print ("Guessing:", char, guess_result)
        if guess :
            time.sleep (delay_time)

    choices_left = []
    for char in "AEIOU" :
        choices_left.append (char)
    while len (choices_left) > 0 :
        char = random.choice (choices_left)
        choices_left.remove (char)
        guess_result = "Good"
        guess = wof.guess_vowel (char)
        if not guess :
            guess_result = "Bad"
        print ("Guessing (vowels):", char, guess_result)
        if guess :
            time.sleep (delay_time)

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
#
wof = WheelOfFortune (display)
time.sleep (2.0)
#wof.initialize_board ()
wof.initialize_game (bonus_round=False ,
                    category="movie" ,
                    lines=["" ,
                           "butch cassidy" ,
                           "and the" ,
                           "sundance kid"])
time.sleep (2.0)
solve_it (wof)
print (wof.complete_phrase)
time.sleep (2.0)

wof.initialize_game (bonus_round=False ,
                    category="phrase" ,
                    lines=["now is the" ,
                           "time to come" ,
                           "to the aid of" ,
                           "your country"])
time.sleep (2.0)
solve_it (wof)
print (wof.complete_phrase)

