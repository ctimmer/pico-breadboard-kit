from machine import Pin
import neopixel
import time

# Define the pin connected to the data line of the WS2812B/WS2818 strip
# Replace '14' with the actual GPIO pin number used on your board (e.g., ESP32, ESP8266, Pico)
data_pin = Pin(12, Pin.OUT) 

# Define the number of LEDs in your strip
num_pixels = 8

# Create a NeoPixel object
# The first argument is the Pin object, the second is the number of pixels
pixels = neopixel.NeoPixel(data_pin, num_pixels)

# Example 1: Set a single LED to a specific color (e.g., red)
# pixels[index] = (red_value, green_value, blue_value)
pixels[0] = (255, 0, 0) # Set the first pixel (index 0) to red
pixels.write() # Update the LED strip to display the changes
time.sleep(1) # Wait for 1 second

# Example 2: Cycle through colors on all LEDs
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)] # Red, Green, Blue
for _ in range(3): # Repeat the cycle a few times
    for color in colors:
        for i in range(num_pixels):
            pixels[i] = color
        pixels.write()
        time.sleep(0.5)

# Example 3: Turn all LEDs off
for i in range(num_pixels):
    pixels[i] = (0, 0, 0) # Set all pixels to black (off)
pixels.write()

data_pin.value (0)
print ("done")
