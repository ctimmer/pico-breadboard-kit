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
#

'''
From the documentation:

Display:
GP2 CLK
GP3 DIN
GP5 CS
GP6 DC
GP7 RST

Pins:
Buzzer      GP13
LEDs        D1: GP16, D2: GP17, D3: 3V3, D4: 5V
RGB LED     GP12
Joystick    X-axis: ADC0, Y-axis: ADC1
Button      BTN1: GP15, BTN2: GP14
'''

import sys
from machine import SPI, Pin, Timer, ADC, PWM
import time

from modules.pbk_ili9488 import Display, color565
from modules.sys_font import SysFont

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

LED_1_PIN = 16
LED_2_PIN = 17

RGB_LEN_PIN = 12

BUTTON_1_PIN = 15
BUTTON_2_PIN = 14

BUZZER_PIN = 13

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

#-------------------------------------------------------------------------------
def display_heading (text, color = WHITE) :
    display_text = text.center (23)
    sysfont.text_sysfont (10 ,
                            10 ,
                            display_text ,
                            scale = 3 ,
                            text_color = color)

def display_status (text, color = WHITE) :
    display.fill_rectangle (x=10, y=290, w=400, h=30, color=BLACK)
    sysfont.text_sysfont (10 ,
                            290 ,
                            text ,
                            scale = 3 ,
                            text_color = color)

############################## DISPLAY TEST ####################################
def display_test () :
    display.clear (WHITE)
    # Rectangles
    display.fill_rectangle(x=10, y=10, w=100, h=100, color=RED)
    display.fill_rectangle(x=120, y=10, w=100, h=100, color=GREEN)
    display.fill_rectangle(x=230, y=10, w=100, h=100, color=BLUE)
    display.fill_rectangle(x=380, y=220, w=100, h=100, color=YELLOW_ORANGE)
    # Text (very small)
    display.draw_text8x8(x=20, y=120,
                        text="Hello World",
                        color=WHITE,
                        background=BLACK,
                        rotate=0)
    # Circle
    display.fill_circle(x0=240, y0=160, r=20, color=BROWN)
    # Image
    display.draw_image(path="images/glad.raw", x=20, y=190, w=160, h=120)
    time.sleep (2.0)
    #print ("End display test")

############################## BUTTON TEST ####################################
button_1 = Pin (BUTTON_1_PIN, Pin.IN)
button_2 = Pin (BUTTON_2_PIN, Pin.IN)

def button_test () :
    #print ("", "Starting BUTTON test (press button 2 to quit)")
    display.clear (BLACK)
    display_heading ("Button Test")
    display_status ("Button 2: Quit")
    while button_2 () == 1 :
        if button_1 () == 0 :
            display_status ("Button 1 pressed")
            time.sleep (0.5)
    display_status ("End of Button Test")
    time.sleep (2.0)
    #print ("button 2 pressed, end button test")

############################## LED TEST ####################################
led_1 = Pin (LED_1_PIN, Pin.OUT, value=0)
led_2 = Pin (LED_2_PIN, Pin.OUT, value=0)

def led_test () :
    #print ("", "Starting LED test")
    display.clear (BLACK)
    display_heading ("LED Test")
    display_status ("Button 2: Quit")
    led_1.value (1)
    while button_2 () == 1 :
        #print (led_1.value(), led_2.value())
        led_1.toggle ()
        led_2.toggle ()
        time.sleep (0.2)
    led_1.value (0)
    led_2.value (0)
    display_status ("End of LED Test")
    time.sleep (2.0)

############################## BUZZER TEST ####################################
buzzer = Pin (BUZZER_PIN, Pin.OUT)

def play_tone(frequency, duration_ms):
    """Plays a tone on the buzzer with the given frequency and duration."""
    buzzer.freq(frequency)  # Set the frequency (pitch)
    buzzer.duty_u16(30000)  # Set the duty cycle (volume, 0-65535)
    time.sleep (duration_ms / 1000)   # Wait for the tone duration (convert ms to seconds)
    buzzer.duty_u16(0)      # Turn off the sound

def buzzer_test () :
    display.clear (BLACK)
    display_heading ("Buzzer Test")
    display_status ("Button 2: Quit")
    while button_2 () == 1 :
        if button_1 () == 0 :
            buzzer.value(1)  # Turn the buzzer on
            time.sleep(0.5)       # Wait for 0.5 seconds
            buzzer.value(0)  # Turn the buzzer off
    #play_tone(440, 500)  # Play A4 for 500ms

############################## JOYSTICK TEST ####################################

JS_CHANGE_MIN = 20  # pixels
JS_MAX = 65535
DISP_MAX = 320
DISP_X_OFFSET = 80

x_axis = ADC (0)    # ACD0
y_axis = ADC (1)    # ADC1

def joystick_read_to_xy () :
    x = x_axis.read_u16 () # 0-65535
    y = y_axis.read_u16 ()
    #print (f"x={x} y={y}")
    if x < 0  \
    or x > JS_MAX :
        return None    # bad read?
    if y < 0  \
    or y > JS_MAX :
        return None    # bad read
    ## convert to pixel xy position
    x_disp = int ((x / JS_MAX) * DISP_MAX)
    y_disp = DISP_MAX - int ((y / JS_MAX) * DISP_MAX)
    #print (f"x_disp:{x_disp} y_disp:{y_disp}")
    return (x_disp, y_disp)
    
def joystick_test () :
    display.clear (BLACK)
    display_heading ("Joystick Test")
    display_status ("Button 2: Quit")
    while True :
        xy_pos = joystick_read_to_xy ()
        if xy_pos is not None :
            curr_x_pos = xy_pos[0]
            curr_y_pos = xy_pos[1]
            break
    display.fill_circle(curr_x_pos + DISP_X_OFFSET, curr_y_pos, 4, WHITE)
    while button_2 () == 1 :
        xy_pos = joystick_read_to_xy ()
        if xy_pos is not None :
            #print (f"xy_pos: {xy_pos}")
            if abs (xy_pos[0] - curr_x_pos) >= JS_CHANGE_MIN \
            or abs (xy_pos[1] - curr_y_pos) >= JS_CHANGE_MIN :
                display.draw_line (curr_x_pos + DISP_X_OFFSET,
                                    curr_y_pos,
                                    xy_pos[0] + DISP_X_OFFSET,
                                    xy_pos[1],
                                    WHITE)
                curr_x_pos = xy_pos[0]
                curr_y_pos = xy_pos[1]
                #print (f"x_pos={curr_x_pos} y={curr_y_pos}")
                time.sleep (0.5)
    display_status ("End of Joystick Test")
    time.sleep (2.0)

############### main #################

display_test ()

button_test ()

led_test ()

buzzer_test ()

joystick_test ()

