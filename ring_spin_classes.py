##!/usr/bin/env python3
# NeoPixel library ring spin example
# Author: Matt Harrison
# Repo: https://github.com/mattybigback/ws2812b_python_RPi

import time
from animations import *
from rpi_ws281x import PixelStrip, Color
import argparse


# LED strip configuration:
LED_COUNT = 12          # Number of LED pixels.
# LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM, requires root)
LED_PIN = 10            # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0, does not require root)
LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10            # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False      # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0         # set to '1' for GPIOs 13, 19, 41, 45 or 53



def all_off(strip):
    """Turn off all LEDs"""
    for j in range (strip.numPixels()):
        strip.setPixelColor(j, Color(0,0,0))
        strip.show()

def send_buffer_to_leds(strip, buffer):
    for idx_pixel, pixel in enumerate(buffer):
        red = buffer[idx_pixel]["red"]
        green = buffer[idx_pixel]["green"]
        blue = buffer[idx_pixel]["blue"]
        strip.setPixelColor(idx_pixel, Color(red,green,blue))


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
    ring1 = RotatingRing(strip.numPixels())
    send_buffer_to_leds(strip, ring1.ring_buffer)
    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            if ring1.frame_counter == 0:
                ring1.set_position(LED_COUNT-1, random_color_simple())
            ring1.rotate_buffer()
            send_buffer_to_leds(strip, ring1.ring_buffer)
            strip.show()
            delay = 50
            time.sleep(delay / 1000.0)

    except KeyboardInterrupt:
        if args.clear:
            all_off(strip)
