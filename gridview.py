import sys
import numpy as np
from PIL import Image, ImageDraw
from collections import namedtuple
from math import * 

pi = np.pi

'''
Process CLI input

GRID PARAMETERS:
    line_density : float
    axis_colors : np.array[3,3]
    overlay : bool

VP DETECTION PARAMETERS: 
    focal_len : float
    line_threshold : float
    principal_point : np.array[2]
    seed : int
'''
# Line = namedtuple('Line', [m, b])
# VP = namedtuple('VP', [x, y])

line_count = 20 # 20 lines per vp
plane_colors = [(255,0,0), (0,255,0), (0,0,255)]
overlay = True # overlay over input img

def draw_grid(img: Image.Image , vps): # euclidean vps
    w, h = img.size[0], img.size[1]
    line_len = 5000
    theta_step = 2*pi/line_count
    draw = ImageDraw.Draw(img)

    for vp in vps:
        color_index = 0
        t0 = np.arctan2(vp[0], vp[1])
        vp_shift = (vp[0] + w//2, -vp[1] + h//2)
        tmp = [t0]
        for i in range(line_count):
            theta = (2*pi/line_count) * i
            endpoint = (
                int(vp_shift[0] + line_len * cos(theta)),
                int(vp_shift[1] + line_len * sin(theta)),
            )
            draw.line([vp_shift, endpoint], fill=(plane_colors[color_index]), width=2)
        color_index += 1
    

    return 1

# Create a blank image canvas
canvas_width = 400  # Adjust these dimensions as needed
canvas_height = 400  # Adjust these dimensions as needed
background_color = "white"

image = Image.new("RGB", (canvas_width, canvas_height), background_color)
vps = [(0,0), (0, 400), (0, -200)]
# vps_test = np.array()

draw_grid(image, vps)
image.show()

print(sys.argv)