# pico-breadboard-kit - nixie tube image demo

Displays nixie sprite sheet file

Displays example numbers represented by nixie images

## Usage

```
run pbk_nixie_display.py
```

## Demonstrates

- Sprite sheet with same size images arranged in 2 rows
- Accessing sprite images via index

## Requires

- Tested on a Raspberry pico 2w
- modules/pbk_ili9488.py
- modules/sprite_handler.py

## Files

- pbk_nixie_display.py
  - demostration application
- nixie360x98.raw
  - nixie sprite sheet image file
- mpremote.sh
  - linux bash script to run demo via mpremote
  - May not run because of additional memory requirements
- README.md
  - This documentation file