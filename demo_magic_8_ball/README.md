# pico-breadboard-kit - magic 8 ball image demo

Displays random answers

## Usage

```
run pbk_magic_8_ball.py
```

Button 1 - Display answer (shake 8 ball)

Button 2 - Quit

## Demonstrates

- Sprite sheet with variable sized images
- Using sprite sheet for character font

## Requires

- Tested on a Raspberry pico 2w
- modules/pbk_ili9488.py
- modules/sprite_handler.py

## Files

- pbk_magic_8_ball.py
  - demostration application
- magic8ans227x200.raw
  - Answer background image
- magic8char327x17.raw
 - Character images for answer
- mpremote.sh
  - linux bash script to run demo via mpremote
  - May not run because of additional memory requirements
- README.md
  - This documentation file