# Pico Breadboard Kit - display nixie sprites
#
import time, sys, gc
import random

from machine import SPI, Pin

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
YELLOW = color565 (255,255,0)

BUTTON_1_PIN = 15
BUTTON_2_PIN = 14

tarot_image = None

TAROT_IDS = {
    "fool" : 0 ,
    "magician" : 1 ,
    "high priestess" : 2 ,
    "empress" : 3 ,
    "emperor" : 4 ,
    "pope" : 5 ,
    "lovers" : 6 ,
    "chariot" : 7 ,
    "justice" : 8 ,
    "hermit" : 9 ,
    "wheel of fortune" : 10 ,
    "strength" : 11 ,
    "hanged man" : 12 ,
    "death" : 13  ,
    "temperance" : 14 ,
    "devil" : 15 ,
    "tower" : 16 ,
    "star" : 17 ,
    "moon" : 18 ,
    "sun" : 19 ,
    "judgment" : 20 ,
    "world" : 21
    }

#######################################################################

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

#BTN1: GP15, BTN2: GP14
button_1 = Pin (BUTTON_1_PIN, Pin.IN) # next reading
button_2 = Pin (BUTTON_2_PIN, Pin.IN) # Quit

def display_tarot_deck () :
    global tarot_image
    width = 40
    height = 75
    image_rows = 4
    tarot_image = SpriteHandler ()
    tarot_image.load_raw_file ("tarot240x300.raw" ,
                                image_width = width ,
                                image_height = height ,
                                image_rows = image_rows)

    for img_idx in range (0,11) :
        display.draw_sprite (tarot_image [img_idx],
                                x = 5 + (img_idx * 42),
                                y = 0,
                                w = width,
                                h = height)
    for img_idx in range (0,11) :
        display.draw_sprite (tarot_image [img_idx + 11],
                                x = 5 + (img_idx * 42),
                                y = 76,
                                w = width,
                                h = height)

    ## show tarot card reversed (inverted)
    for img_idx in range (0,11) :
        display.draw_sprite (tarot_image.get_index_sprite (img_idx, inverted=True),
                                x = 5 + (img_idx * 42),
                                y = 168,
                                w = width,
                                h = height)
    for img_idx in range (0,11) :
        display.draw_sprite (tarot_image.get_index_sprite (img_idx + 11, inverted=True),
                                x = 5 + (img_idx * 42),
                                y = 244,
                                w = width,
                                h = height)
    tarot_image = None

# Tarot reading
def tarot_reading (small = False) :
    global tarot_image
    tarot_image = SpriteHandler ()
    if small :
        sprite_width = 40
        sprite_height = 75
        tarot_image.load_raw_file ("tarot280x300.raw" ,
                                    image_width = sprite_width ,
                                    image_height = sprite_height ,
                                    image_rows = 4)
    else :
        sprite_width = 57
        sprite_height = 107
        tarot_image.load_raw_file ("tarot342x428.raw" ,
                                    image_width = sprite_width ,
                                    image_height = sprite_height ,
                                    image_rows = 4)
    #
    tarot_ids = []
    for _, (card_id, card_idx) in enumerate (TAROT_IDS.items ()) :
        #print (card_id)
        tarot_image.load_index_id (card_id, card_idx)
        tarot_ids.append (card_id)
    display.clear (0)
    sysfont.text_sysfont (10 ,
                            75 ,
                            "Button 1: Take a reading" ,
                            scale = 3 ,
                            text_color = WHITE)
    sysfont.text_sysfont (10 ,
                            150 ,
                            "Button 2: Exit" ,
                            scale = 3 ,
                            text_color = WHITE)
    while button_2.value() != 0 :
        if button_1.value() == 0 :
            do_tarot_reading (tarot_ids ,
                                sprite_width ,
                                sprite_height)
        time.sleep (0.1)
    display.fill_rectangle (0, 290, 480, 30, BLACK)
    sysfont.text_sysfont (20 ,
                            290 ,
                            "Use your readings wisely" ,
                            scale = 3 ,
                            text_color = GREEN)

def do_tarot_reading (tarot_ids ,
                        sprite_width ,
                        sprite_height) :
    display.clear (0)
    tarot_reading_ids = tarot_ids.copy()
    tarot_reading = []
    for count in range (0, 3) :
        tarot_id = tarot_reading_ids [random.randint (0, len (tarot_reading_ids) - 1)]
        tarot_reading.append (tarot_id)
        tarot_reading_ids.remove (tarot_id)
    tarot_spread = ["Past", "Present", "Future"]
    x_pos = 50
    y_pos = 124
    reading_width_max = 12
    sysfont.text_sysfont (x_pos - 30 ,
                            y_pos - 75 ,
                            "Your Tarot Reading" ,
                            scale = 4 ,
                            text_color = WHITE)
    for idx, reading_id in enumerate (tarot_reading) :
        
        sysfont.text_sysfont (x_pos - 10,
                              y_pos - 24,
                              tarot_spread[idx],
                              text_color=WHITE)
        #print ("reading_id:",reading_id)
        card_reversed = random.choice([True, False])
        reading_sprite = tarot_image.get_index_id_sprite (reading_id, inverted=card_reversed)
        display.draw_sprite (reading_sprite, x=x_pos, y=y_pos, w=sprite_width, h=sprite_height)
        reading_id = (reading_id [0]).upper () + reading_id [1:]
        if len (reading_id) > reading_width_max :
            reading_id = reading_id [0:reading_width_max]
        else :
            reading_id = reading_id.center (reading_width_max)
        reading_color = WHITE
        if card_reversed :
            reading_color = YELLOW
        sysfont.text_sysfont (x_pos - 46 ,
                              y_pos + sprite_height + 10 ,
                              reading_id ,
                              text_color=reading_color)
        time.sleep (1.0)
        x_pos += 150
    ## Next/Quit button labels
    sysfont.text_sysfont (146 ,
                            300 ,
                            "Next" ,
                            text_color = GREEN)
    sysfont.text_sysfont (228 ,
                            300 ,
                            "Quit" ,
                            text_color = RED)

#######################################################################

if True :
    print ("Display tarot deck, normal and reversed")
    display_tarot_deck ()
    tarot_image = None
    time.sleep (5.0)

gc.collect ()
print ("Take tarot reading(s)")
tarot_reading (small = True)
