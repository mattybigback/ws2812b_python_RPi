##!/usr/bin/env python3
# NeoPixel library ring spin example
# Author: Matt Harrison
# Repo: 
# Adapted from strandtest.py by Tony DiCola (tony@tonydicola.com)
# https://github.com/rpi-ws281x/rpi-ws281x-python/blob/master/examples/strandtest.py

import random
import time
import colorsys
from rpi_ws281x import PixelStrip, Color
import argparse
from collections import deque

# LED strip configuration:
LED_COUNT = 12          # Number of LED pixels.
# LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM, requires root)
LED_PIN = 10            # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0, does not require root)
LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10            # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False      # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0         # set to '1' for GPIOs 13, 19, 41, 45 or 53


def get_bit_at_position(input_value, bit_position):
    """Returns the value of a bit at a given position"""
    return (input_value & (1 << (bit_position - 1))) >> (bit_position - 1)

def random_color_simple():
    "Generates a random color from a limited palette (3 bit RGB)"
    color_int = random.randint(1,7)
    red = get_bit_at_position(color_int, 1) * 255
    green = get_bit_at_position(color_int, 2) * 255
    blue = get_bit_at_position(color_int, 3) * 255
    return(red,green,blue)

def single_pixel_wipe(strip, pixel_color=(255,255,255), wait_ms=100):
    """Turn on a single pixel and move it around the ring"""
    leds = []
    for i in range(strip.numPixels()):
        pixel = {   "red":0,
            "green":0,
            "blue":0
        }
        leds.append(pixel)

    leds[0]["red"] = pixel_color[0]
    leds[0]["green"] = pixel_color[1]
    leds[0]["blue"] = pixel_color[2]

    for pixel in leds:
        for idx_pixel, pixel in enumerate(leds):
            red = leds[idx_pixel]["red"]
            green = leds[idx_pixel]["green"]
            blue = leds[idx_pixel]["blue"]
            strip.setPixelColor(idx_pixel, Color(red,green,blue))
        strip.show()
        leds = deque(leds)
        leds.rotate(1)
        leds = list(leds)
        time.sleep(wait_ms / 1000.0)

def hsv_to_rgb24(h, s, v):
   rgb = colorsys.hsv_to_rgb(h, s, v)
   rgb = tuple(round(255*x) for x in rgb)
   return rgb

def all_off(strip):
    """Turn off all LEDs"""
    for j in range (strip.numPixels()):
        strip.setPixelColor(j, Color(0,0,0))
        strip.show()

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            print("Single pixel wipe")
            single_pixel_wipe(strip, pixel_color=random_color_simple())

    except KeyboardInterrupt:
        if args.clear:
            all_off(strip)
