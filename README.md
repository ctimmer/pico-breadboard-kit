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
