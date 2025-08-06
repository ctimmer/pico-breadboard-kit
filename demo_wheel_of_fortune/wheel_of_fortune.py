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
# Wheel of Fortune board controller
#

from pbk_ili9488 import color565
from sprite_handler import SpriteHandler

#-----------------------------------------
#
SMALL = False  # True to use half size sprite images
#SMALL = True

DISPLAY_BG = color565 (211,211,211)   # Light grey
BOARD_WIDTH = 460            # WOF board size
BOARD_HEIGHT = 310
BOARD_X_POSITION = 10        # position in display
BOARD_Y_POSITION = 5
BOARD_X_OFFSET = BOARD_X_POSITION + 7   # sprite image position
BOARD_Y_OFFSET = BOARD_Y_POSITION + 36
BOARD_BG = color565 (28,174,252)      # Blueish
CHAR_WIDTH = 30              # sprite image size
CHAR_HEIGHT = 38
X_PADDING = 2                # pixels between sprites
Y_PADDING = 2
BOARD_LINES = [
    { # line 1
    "length" : 12 ,
    "x_board" : 1 ,
    "y_board" : 0 ,
    "text" : "" ,
    "space_sub" : "#"
    } ,
    { # line 2
    "length" : 14 ,
    "x_board" : 0 ,
    "y_board" : 1 ,
    "text" : "" ,
    "space_sub" : "#"
    } ,
    { # line 3
    "length" : 14 ,
    "x_board" : 0 ,
    "y_board" : 2 ,
    "text" : "" ,
    "space_sub" : "#"
    } ,
    { # line 4
    "length" : 12 ,
    "x_board" : 1 ,
    "y_board" : 3 ,
    "text" : "" ,
    "space_sub" : "#"
    } ,
    { # category
    "length" : 14 ,
    "x_board" : 0 ,
    "y_board" : 5 ,
    "text" : "" ,
    "space_sub" : " "
    }
    ]

SPRITE_FILE = "wof-char240x152.raw"
SPRITE_FILE_ROWS = 4
# Translate characters to sprite index
SPRITE_CHARS = {
    "A" : 0, "B" : 1, "C" : 2, "D" : 3, "E" : 4, "F" : 5, "G" : 6, "H" : 7,
    "I" : 8, "J" : 9, "K" : 10, "L" : 11, "M" : 12, "N" : 13, "O" : 14, "P" : 15,
    "Q" : 16, "R" : 17, "S" : 18, "T" : 19, "U" : 20, "V" : 21, "W" : 22, "X" : 23,
    "Y" : 24, "Z" : 25, " " : 26, "#" : 27
    }

if SMALL :
    BOARD_X_POSITION = 0 # 10
    BOARD_Y_POSITION = 0 # 5
    BOARD_X_OFFSET = BOARD_X_POSITION + 1 # 7
    BOARD_Y_OFFSET = BOARD_Y_POSITION + 6 # 36
    # use half size sprite images
    CHAR_WIDTH = 15   # sprite image size
    CHAR_HEIGHT = 19  # test
    BOARD_WIDTH = 240 # 460
    BOARD_HEIGHT = 120 # 310
    for line_idx, line_data in enumerate (BOARD_LINES) :
        line_data ["y_board"] = line_idx    # pack board lines
    X_PADDING = 2
    Y_PADDING = 3
    SPRITE_FILE = "wof-char120x76.raw"   # text

## Documentation for a class.
#
#  More details.
class WheelOfFortune :
    ## The constructor.
    #  @param self The object pointer.
    #  @param display Display controller.
    ## @var display
    #  a member variable.
    def __init__ (self ,
                  display) :
        ## Updates display
        self.display = display
        ## Interface to sprite sheets
        self.images = SpriteHandler ()
        self.images.load_raw_file (SPRITE_FILE ,
                        image_width = CHAR_WIDTH ,
                        image_height = CHAR_HEIGHT ,
                        image_rows = SPRITE_FILE_ROWS)
        self.images.buffer_images ()  # may not have enough mem for this
        ## For restricting guesses
        self.vowels = "AEIOU"
        ## Automatic guesses for bonus round
        self.bonus_guesses = "RSTLNE"
        ## 
        self.board_characters = {}
        ## Board layout
        self.board_lines = BOARD_LINES
        ## Category line
        self.category_idx = 4
        self.initialize_board ()
        ## Text of game board
        self.complete_phrase = ""
        ## Initial game board display
        self.set_lines ([
            "" ,
            "wheel of" ,
            "fortune"
            ])
        ## Initial game board category
        self.set_category ("game show")
        self.initialize_game ()
        self.show_board ()

    ## Initialize the game board.
    #  @param self The object pointer.
    def initialize_board (self) :
        self.display.clear (DISPLAY_BG)
        self.display.fill_rectangle(x=BOARD_X_POSITION,
                                    y=BOARD_Y_POSITION,
                                    w=BOARD_WIDTH,
                                    h=BOARD_HEIGHT,
                                    color = BOARD_BG)
        for line_idx, line_data in enumerate (self.board_lines) :
            line_data ["text"] = ""
        self.clear_board ()

    ## Test if letter is part of the game board.
    #  @param char Character to be tested.
    #  @param allow_vowels Set to True if test character is vowel.
    def guess_character (self, char, allow_vowels = False) :
        if not char in self.board_characters :
            return False
        if char in self.vowels \
        and not allow_vowels :
            return False
        if not self.board_characters[char]["hide"] :
            return False
        self.board_characters[char]["hide"] = False
        for _, xy_board in enumerate (self.board_characters[char]["positions"]) :
            self.board_sprite (char, xy_board[0], xy_board[1])
        return True

    ## Buy a vowel
    def guess_vowel (self, char) :
        if char not in self.vowels :
            return False
        return self.guess_character (char, allow_vowels=True)

    def clear_board (self) :
        for line_idx, line_data in enumerate (self.board_lines) :
            x_board = line_data ["x_board"]
            y_board = line_data ["y_board"]
            space_sub = line_data ["space_sub"]
            for idx in range (0,line_data ["length"]) :
                self.board_sprite (space_sub, x_board, y_board)
                x_board += 1
    ## Show all game board letters
    def show_board (self) :
        for _, (char, char_entry) in enumerate (self.board_characters.items()) :
            if not char_entry ["hide"] :
                continue
            self.guess_character (char, True)
    def set_lines (self, lines) :
        for line_idx in range (0,4) :
            self.board_lines [line_idx]["text"] = ""
        phrase = ""
        for line_idx in range (0,4) :
            if line_idx >= len (lines) :
                break
            line_data = self.board_lines [line_idx]
            text = lines [line_idx].strip ()
            if len (text) > line_data["length"] :
                text = text[0:line_data["length"]]
            text = text.upper().center (line_data["length"])
            line_data ["text"] = text
            phrase += text + " "
        phrase = " ".join(phrase.split())
        self.complete_phrase = phrase
    def set_category (self, category) :
        line_data = self.board_lines [self.category_idx]
        text = category.center (line_data["length"])
        if len (text) > line_data["length"] :
            text = text[0:line_data["length"]]
        line_data ["text"] = text.upper ()
    def initialize_game (self, bonus_round=False, category=None, lines=None) :
        self.board_characters = {}
        self.clear_board ()
        if category is not None :
            self.set_category (category)
        if lines is not None :
            self.set_lines (lines)
        for line_idx, line_data in enumerate (self.board_lines) :
            x_board = line_data ["x_board"]
            y_board = line_data ["y_board"]
            text = line_data ["text"].replace (" ", line_data["space_sub"])
            for char_idx, char in enumerate (text) :
                if line_idx < 4 :
                    if char not in [" ", "#"] :
                        #self.initialize_character (char, x_board, y_board)
                        if char not in self.board_characters :
                            self.board_characters [char] = {
                                "hide" : True ,
                                "positions" : []
                                }
                        self.board_characters [char]["positions"].append ([x_board, y_board])
                        char = " "
                self.board_sprite (char, x_board, y_board)
                x_board += 1
        if bonus_round :
            for _, char in enumerate (self.bonus_guesses) :
                self.guess_character (char, allow_vowels = True)

    def board_sprite (self, sprite_char, x_board, y_board) :
        x_pos = BOARD_X_OFFSET + (x_board * (CHAR_WIDTH + X_PADDING))
        y_pos = BOARD_Y_OFFSET + (y_board * (CHAR_HEIGHT + Y_PADDING))
        self.display.draw_sprite (self.images[SPRITE_CHARS[sprite_char]],
                                    x=x_pos,
                                    y=y_pos,
                                    w=CHAR_WIDTH,
                                    h=CHAR_HEIGHT)

    def display_sprite (self, sprite_char, x_pos, y_pos) :
        self.display.draw_sprite (self.images[SPRITE_CHARS[sprite_char]],
                                    x=x_pos,
                                    y=y_pos,
                                    w=CHAR_WIDTH,
                                    h=CHAR_HEIGHT)

if __name__ == "__main__" :
    import time
    from machine import SPI, Pin
    from pbk_ili9488 import Display
    #
    SPI_ID = 0
    BAUDRATE = 100_000_000
    SCK_PIN = 2
    MOSI_PIN = 3
    CS_PIN = 5
    DC_PIN = 6
    RST_PIN = 7
    DISPLAY_WIDTH = 480
    DISPLAY_HEIGHT = 320
    #
    spi = SPI(SPI_ID, baudrate=BAUDRATE, sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN))
    display = Display (spi = spi ,
                        cs = Pin (CS_PIN) ,
                        dc = Pin (DC_PIN) ,
                        rst = Pin (RST_PIN) ,
                        width = DISPLAY_WIDTH ,
                        height = DISPLAY_HEIGHT)
    #
    wof = WheelOfFortune (display)
    time.sleep (2.0)
    wof.initialize_game (bonus_round=False ,
                        category="phrase" ,
                        lines=["give","yourself","a round of","applause"])

    time.sleep (5.0)
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" :
        guess = wof.guess_character (char)
        print ("Guessing:", char, guess)
        if guess :
            time.sleep (0.5)

    for char in "AEIOU" :
        guess = wof.guess_vowel (char)
        print ("Guessing (vowels):", char, guess)
        if guess :
            time.sleep (0.5)

