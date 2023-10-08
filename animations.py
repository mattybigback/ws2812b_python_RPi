from collections import deque
import random
import colorsys

class RotatingRing:
    ring_buffer = []
    rotate_direction = "clockwise"
    rotate_amount = 1
    frame_counter = 0

    def __init__(self, num_pixels):
        for pixel in range(num_pixels):
            pixel = {   "red":0,
                "green":0,
                "blue":0
            }
            self.ring_buffer.append(pixel)
    
    def get_buffer(self):
        return self.ring_buffer
    
    def rotate_buffer(self):
        self.ring_buffer = deque(self.ring_buffer)
        if self.rotate_direction == "clockwise":
            self.ring_buffer.rotate(self.rotate_amount)
        if self.rotate_direction == "anticlockwise":
            self.ring_buffer.rotate(-abs(self.rotate_amount))
        self.ring_buffer = list(self.ring_buffer)
        if self.frame_counter == len(self.ring_buffer)-1:
            self.frame_counter = 0
        else:
            self.frame_counter += 1

    def set_position(self, position, pixel_color):
        self.ring_buffer[position]["red"] = pixel_color[0]
        self.ring_buffer[position]["green"] = pixel_color[1]
        self.ring_buffer[position]["blue"] = pixel_color[2]

def random_color_simple():
    "Generates a random color from a limited palette (3 bit RGB)"
    color_int = random.randint(1,7)
    red = get_bit_at_position(color_int, 1) * 255
    green = get_bit_at_position(color_int, 2) * 255
    blue = get_bit_at_position(color_int, 3) * 255
    return(red,green,blue)
    
def get_bit_at_position(input_value, bit_position):
    """Returns the value of a bit at a given position"""
    return (input_value & (1 << (bit_position - 1))) >> (bit_position - 1)

def hsv_to_rgb24(h, s, v):
   rgb = colorsys.hsv_to_rgb(h, s, v)
   rgb = tuple(round(255*x) for x in rgb)
   return rgb