# Mechanical odometer demo 

Displays odometer, increments up and down

## Usage

```
run pbk_odometer.py
```

## Demonstrates

- Images
  - Display image from file
  - Sprite sheet with same size images arranged in 1 row
  - Accessing sprite images via index
  - Accessing partial sprite images

## Requires

- Tested on a Raspberry pico 2w
- modules/pbk_ili9488.py
- modules/sprite_handler.py

## Files

- pbk_odometer.py
  - demonstration application
- odomdigits.raw
  - odometer digit sprite sheet image file
- mpremote.sh
  - linux bash script to run demo via mpremote
  - May not run because of additional memory requirements
- README.md
  - This documentation file