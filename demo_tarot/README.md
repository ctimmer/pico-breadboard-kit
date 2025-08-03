# pico-breadboard-kit - Tarot card image demo

Displays all the terot cards

Displays all the cards inverted

Displays tarot reading(s)

## Usage

```
run pbk_tarot.py
```

Button 1 - Show tarot reading

Button 2 - Quit

## Demonstrates

- Sprite sheet with same size images arranged in 2 rows
- Accessing sprite images via id
- Button 1 Show tarot reading
- Button 2 Quit

## Requires

- Tested on a Raspberry pico 2w
- modules/pbk_ili9488.py
- modules/sprite_handler.py
- modules/sys_font.py

## Files

- pbk_tarot.py
  - demostration application
- tarot240x300.raw
  - Very small tarot card images that will fit on the display
- tarot280x300.raw
  - Smaller tarot card reading images that us less memory  
- tarot342x428.raw
  - Larger tarot card reading images
- mpremote.sh
  - linux bash script to run demo via mpremote
  - May not run because of additional memory requirements
- README.md
  - This documentation file