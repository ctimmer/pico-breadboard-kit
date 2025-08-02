# Modules used by demostration applications

## Descriptions

- pbk_ili9488.py
  - Driver for display
  - The documentation indicates the display is a ST7796SU1 but the modified ili driver seemed to worked best for me.
  - There was no micropython driver supplied
- sprite_handler.py
  - Loads the sprite sheet image file
  - Provides various interfaces to access the individual sprite images.
- sys_font.py
  - Provides a simple pixel oriented font.