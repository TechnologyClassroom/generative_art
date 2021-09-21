################################################################################
# Driver (handles globals/setup/draw)
# 
# Code and images by Aaron Penne
# https://github.com/aaronpenne/generative_art
#
# Released under the MIT license (https://opensource.org/licenses/MIT)
################################################################################

import datetime
from random import shuffle, seed
import os

w = 800
h = 800

record = False
animate = False
seeded = True

rand_seed = 1138

################################################################################
# Global variables - no need to touch
################################################################################

# Allows for global colors
c = [color(0) for x in range(16+1)]

# Gets filename of this script
filename = __file__[:-5]

# Gets current YYMMDD_HHMMSS timestamp (e.g. 20160530_065530)
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


################################################################################
# Setup
################################################################################
def setup():
    # Sets size of canvas in pixels (must be first line)
    size(w, h)
    
    # Sets resolution dynamically (affects resolution of saved image)
    pixelDensity(displayDensity())  # 1 for low, 2 for high
        
    # Stops draw() from running in an infinite loop
    if not animate:
        noLoop()
        
    # Sets random seed value for both Python and Processing 
    if seeded:
        seed(rand_seed)       # Only applies to the random Python module
        randomSeed(rand_seed) # Only applies to the random() Processing function
        noiseSeed(rand_seed)  # Only applies to the noise() Processing function
        
    # Set the number of frames per second to display
    frameRate(20)
    
    # Keeps text centered vertically and horizontally at (x,y) coords
    textMode(CENTER)
    textAlign(CENTER, CENTER)

    rectMode(CORNERS)
    
    # Sets color space and max values
    colorMode(HSB, 360, 100, 100, 100)
        
    global c
    # Fisk Mississipi maps
    c[0] = color(39, 16.9, 92.9) # tan background
    c[1] = color(48.8, 27, 92.9) # yellowish
    c[2] = color(152, 15.38, 76.47) # blueish
    c[3] = color(2.7, 40.3, 86.7) # reddish
    c[4] = color(60, 18.4, 80.8) # greenish
    # Klint
    c[5] = color(300, 33, 1) # blackish
    c[6] = color(206, 61, 50) # bluegray
    c[7] = color(60, 18.4, 80.8) # greenish
    c[8] = color(2.7, 40.3, 86.7) # reddish
    c[9] = color(216, 41, 46) # blueish
    c[10] = color(37, 18, 80) # grayish
    c[11] = color(51, 3, 93) # whiteish    
    # Synopsis
    c[12] = color(206, 61, 50)  # blue
    c[13] = color(270, 27, 49)  # purple
    c[14] = color(206, 61, 50)  # bluegray
    c[15] = color(354, 53, 95),  # pink
    c[16] = color(18, 41, 98),  # peach
    
    # Sets the color for the first run
    c_bg = c[0]  # bg
    c_fill = c[8]  # fill
    c_stroke = c[5]  # stroke
    background(c_bg)
    fill(c_fill)
    stroke(c_stroke)
    

################################################################################
# Sketch functions
################################################################################
def draw():
    noFill()
    
    m1 = draw_mask(200)
    m2 = draw_mask(400)
    g = draw_blob(width/2, height/2, 200, frameCount)
    p = draw_pattern()
    g.mask(m2)
    p.mask(m1)
    image(g, 0, 0)
    image(p, 0, 0)
    
    if record:
        save_frame_timestamp(filename, timestamp)
    if not animate:
        save_frame_timestamp(filename, timestamp)
    



################################################################################
# Sketch functions
################################################################################
def draw_mask(r):    
    m = createGraphics(width, height)
    m.beginDraw()
    m.stroke(c[0])
    m.fill(c[0])
    m.ellipse(w/2, h/2, r, r)
    m.endDraw()
    return m
    
def draw_blob(x, y, r, step):  
    g = createGraphics(width, height)
    g.beginDraw()
    g.beginShape()
    g.stroke(c[0])
    g.fill(c[0])
    
    a_vals = [a for a in range(0, 361, int(step))]
    shuffle(a_vals)
    for a in a_vals:
        x0, y0 = circle_point(x, y, r, r, radians(a))
        g.curveVertex(x0, y0)
    for a in a_vals:
        x0, y0 = circle_point(x, y, r, r, radians(a))
        g.curveVertex(x0, y0)
    
    g.endShape()
    g.endDraw()
    return g
    
def draw_pattern():
    p = createGraphics(width, height)
    p.beginDraw()
    p.background(c[12])
    step = 10
    for i,x in enumerate(range(0,width+step,step)):
        if i%2==0:
            p.fill(c[12])
        else:
            p.fill(c[8])
        p.rect(0, x, h, x+step)
    p.endDraw()
    
    return p
    
    
################################################################################
# Helper and utility functions (used across multiple sketches)
################################################################################
def mousePressed():
    save_frame_timestamp(filename, timestamp)
    
def save_frame_timestamp(filename, timestamp='', output_dir='output'):
    '''
    Saves each frame with a structured filename to allow for tracking all output
    '''
    filename = filename.replace('\\', '')
    filename = filename.replace('/', '')
    output_filename = os.path.join(output_dir, '{}_{}_{}_####.png'.format(timestamp, filename, rand_seed))
    saveFrame(output_filename)
    print(output_filename)
    
def circle_point(cx, cy, rx, ry, a):
    '''
    Translates polar coords to cartesian
    '''
    x = cx + rx * cos(a)
    y = cy + ry * sin(a)
    return x, y
    
def noise_loop(a, r, min_val, max_val, x_c, y_c):
    '''
    Samples 2D Perlin noise in a circle to make smooth noise loops
    Adapted from https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_136_Polar_Noise_Loop_2/P5/noiseLoop.js
    '''
    xoff = map(cos(a), -1, 1, x_c, x_c + 2*r);
    yoff = map(sin(a), -1, 1, y_c, y_c + 2*r);
    r = noise(xoff, yoff)
    return map(r, 0, 1, this.min, this.max);
