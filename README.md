# Micropython access to Pico Breadboard Kit

[Board Description](https://wiki.52pi.com/index.php?title=EP-0172)

[Software (c++)](https://github.com/geeekpi/pico_breadboard_kit/tree/pico2) Uses LVGL interface

## Connected Components
- pbk_test.py
  - Tests each component
- Display
  - ST7796SU1
  - Controller (modified): modules/pbk_ili9488.py
  - [Source](https://github.com/QiaoTuCodes/MicroPython-_ILI9488/tree/main), search "my stuff" for changes
  - The controller was also used to develop the sprite_handler module
- Display Touch
  - Haven't figured this out yet :frowning:
- Buzzer
  - GP13
  - On/Off and very loud :smile:
- LEDs
  - D1 GP16
  - D2 GP17
- Joystick
  - X-axis: ADC0
  - Y-axis: ADC1
- RGB LED
  - GP12
  - Haven't figured this out yet :frowning:
- Buttons
  - BTN1: GP15
  - BTN2: GP14

## Directories

- demo_magic_8_ball
  - Implementation of the magic 8 ball toy
  - If you haven't heard of this toy, you are not old enough
- demo_nixie_display
  - Simulates nixie tube numeric display
- demo_tarot
  - Implementation of Tarot card readings (fortune telling)
- demo_wheel_of_fortune
  - Implementation of Wheel of Fortune game board
  - Could be used for a full WOF application
- images
  - glad.raw - displayed by pbk_test.py
- modules
  - pbk_ili9488.py modified display controller
  - sprite_handler.py - Loads sprite sheet and extracts images
  - sys_font.py - simple pixel oriented character font

## Files

- pbk_test.py - Simple component test demo
- README.md - This documentation file
