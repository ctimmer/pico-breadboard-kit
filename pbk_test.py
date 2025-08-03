#

'''
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
from machine import SPI, Pin, Timer, ADC
import time

from modules.pbk_ili9488 import Display, color565

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
BROWN = color565(165,42,42)
YELLOW_ORANGE = color565 (255,179,67)

LED_1_PIN = 16
LED_2_PIN = 17

BUTTON_1_PIN = 15
BUTTON_2_PIN = 14

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
    print ("End display test")

############################## BUTTON TEST ####################################
button_1 = Pin (BUTTON_1_PIN, Pin.IN)
button_2 = Pin (BUTTON_2_PIN, Pin.IN)

def button_test () :
    print ("", "Starting BUTTON test (press button 2 to quit)")
    while button_2 () == 1 :
        if button_1 () == 0 :
            print ("button 1 pressed")
            time.sleep (0.5)
    print ("button 2 pressed, end button test")

############################## LED TEST ####################################
led_1 = Pin (LED_1_PIN, Pin.OUT, value=1)
led_2 = Pin (LED_2_PIN, Pin.OUT, value=0)

def led_test () :
    print ("", "Starting LED test")
    for count in range (0, 10) :
        print (led_1.value(), led_2.value())
        led_1.toggle ()
        led_2.toggle ()
        time.sleep (0.2)

    #led.value (0)
    led_1.value (0)
    led_2.value (0)
    print ("End LED test")

############################## JOYSTICK TEST ####################################
x_axis = ADC (0)
y_axis = ADC (1)

def joystick_test () :
    print ("", "Starting JOYSTICK test (press button 2 to quit)")
    while button_2 () == 1 :
        x = x_axis.read_u16 () # 0-65535
        y = y_axis.read_u16 ()
        print (f"x={x} y={y}")
        time.sleep (1.0)

############### main #################

display_test ()

button_test ()

led_test ()

joystick_test ()

