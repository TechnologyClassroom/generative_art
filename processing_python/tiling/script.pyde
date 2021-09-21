##########################################################################
# Code and images by Aaron Penne
# https://github.com/aaronpenne/generative_art
#
# Released under the MIT license (https://opensource.org/licenses/MIT)
##########################################################################

import datetime
from random import shuffle, seed, choice, randint
import os

w = 800
h = 800

record = False
animate = False
seeded = False

rand_seed = 1138

##########################################################################
# Global variables - no need to touch
##########################################################################

# Allows for global colors
c = [color(0) for x in range(22)]
c_wed = [color(0) for x in range(12)]
c_terr = [color(0) for x in range(10)]

# Gets filename of this script
filename = __file__[:-5]

# Gets current YYMMDD_HHMMSS timestamp (e.g. 20160530_065530)
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


##########################################################################
# Setup
##########################################################################
def setup():
    # Sets size of canvas in pixels (must be first line)
    size(w, h)

    # Sets resolution dynamically (affects resolution of saved image)
    pixelDensity(2)  # 1 for low, 2 for high

    # Stops draw() from running in an infinite loop
    if not animate:
        noLoop()

    # Sets random seed value for both Python and Processing
    global rand_seed
    if seeded:
        seed(rand_seed)       # Only applies to the random Python module
        # Only applies to the random() Processing function
        randomSeed(rand_seed)
        noiseSeed(rand_seed)  # Only applies to the noise() Processing function
    else:
        rand_seed = randint(0, 2000000)
        seed(rand_seed)
        randomSeed(rand_seed)
        noiseSeed(rand_seed)

    # Set the number of frames per second to display
    frameRate(20)

    # Keeps text centered vertically and horizontally at (x,y) coords
    textMode(CENTER)
    textAlign(CENTER, CENTER)

    rectMode(CENTER)

    # Sets color space and max values
    colorMode(HSB, 360, 100, 100, 100)
    # blendMode(SUBTRACT)

    global c
    # Fisk Mississipi maps
    c[0] = color(39, 16.9, 92.9)  # tan background
    c[1] = color(48.8, 27, 92.9)  # yellowish
    c[2] = color(152, 15.38, 76.47)  # blueish
    c[3] = color(2.7, 40.3, 86.7)  # reddish
    c[4] = color(60, 18.4, 80.8)  # greenish
    # Klint
    c[5] = color(300, 33, 1)  # blackish
    c[6] = color(206, 61, 50)  # bluegray
    c[7] = color(60, 18.4, 80.8)  # greenish
    c[8] = color(2.7, 40.3, 86.7)  # reddish
    c[9] = color(216, 41, 46)  # blueish
    c[10] = color(37, 18, 80)  # grayish
    c[11] = color(51, 3, 93)  # whiteish
    # Synopsis
    c[12] = color(206, 61, 50)  # blue
    c[13] = color(270, 27, 49)  # purple
    c[14] = color(206, 61, 50)  # bluegray
    c[15] = color(354, 53, 95)  # pink
    c[16] = color(18, 41, 98)  # peach
    # Starbucks gift card
    c[17] = color(291, 60, 52)  # purple
    c[18] = color(291, 60, 22)  # dark purple
    c[19] = color(162, 30, 34)  # green
    c[20] = color(162, 82, 19)  # dark green
    c[21] = color(15.7, 65.7, 37.5)  # dark brown

    global c_wed
    c_wed[0] = color(23.9, 55.9, 86.3)  # orange
    c_wed[1] = color(355.3, 47.4, 74.5) # dusty red
    c_wed[2] = color(39.9, 58.4, 100)   # yellow
    c_wed[3] = color(18, 72.4, 66.7)    # dark orange
    c_wed[4] = color(215.5, 29.1, 95.7) # light blue
    c_wed[5] = color(355.3, 47.4, 74.5) # dusty red
    c_wed[6] = color(354.8, 35.6, 88.2) # pink
    c_wed[7] = color(18, 72.4, 66.7)    # dark orange
    c_wed[8] = color(15.7, 65.7, 27.5)  # dark brown
    c_wed[9] = color(27.3, 78.6, 5.5)   # black
    c_wed[10] = color(13.6, 10.2, 84.3)  # cream
    c_wed[11] = color(0, 0, 95)  # white
    
    global c_terr
    c_terr[0] = color(15.7, 65.7, 37.5)  # dark brown
    c_terr[1] = '#C57B62'  # terra cotta
    c_terr[2] = '#BA967F'  # brown
    c_terr[3] = '#B6A8A7'  # gray
    c_terr[4] = '#D7966E'  # orangey
    c_terr[5] = '#70675E'  # gray brown
    c_terr[6] = color(355.3, 47.4, 74.5) # dusty red
    c_terr[7] = '#B3A59E'
    c_terr[8] = '#C57B62'  # terra cotta
    c_terr[9] = color(15.7, 65.7, 37.5)  # dark brown

    # Sets the color for the first run
    c_bg = color(0, 0, 100)  # bg
    c_fill = c[8]  # fill
    c_stroke = c[5]  # stroke
    
    background(0,0,100)
    
    fill(c_fill)
    stroke(c_stroke)

##########################################################################
# Draw
##########################################################################
def draw():
    
    x_step = 10
    y_step = 10
    
    pad_scale = 0.8
    
    x_span = int(width*pad_scale)
    y_span = int(height*pad_scale)
    
    xc_start = width/2 - x_span/2
    xc_stop = width/2 + x_span/2
    
    yc_start = height/2 - y_span/2
    yc_stop = height/2 + y_span/2
    
    x_d = int((xc_stop-xc_start)/(x_step-1))
    y_d = int((yc_stop-yc_start)/(y_step-1))
    
    x_r = x_d/2
    y_r = y_d/2
    
    r_pad = 1
    
    noFill()
    cnt = 0
    i_x = 0
    for x in range(xc_start, xc_stop+1, x_d):
        i_y = 0
        for y in range(yc_start, yc_stop+1, y_d):
            cnt += 1
            if cnt in [3, 7, 15, 18, 25, 30, 60, 63, 78]:
                continue
            
            push()
            translate(x, y)
            strokeWeight(2)
            rect(0, 0, x_d, y_d)
            strokeWeight(2)
            

        
            curveTightness(0)
            beginShape()
            vertex(-x_r, 0)
            curveVertex(random(-x_r,x_r),random(-y_r,y_r))
            curveVertex(random(-x_r,x_r),random(-y_r,y_r))
            curveVertex(random(-x_r,x_r),random(-y_r,y_r))
            curveVertex(random(-x_r,x_r),random(-y_r,y_r))
            vertex(x_r, 0)
            endShape()
        

            
            pop()
            i_y += 1
        i_x += 1
        
    
    if record:
        save_frame_timestamp(filename, timestamp)
    if not animate:
        save_frame_timestamp(filename, timestamp)

        
    if height > 1000 or width > 1000:
        import sys
        exit()
        sys.exit()

##########################################################################
# Sketch functions
##########################################################################




##########################################################################
# Helper and utility functions (used across multiple sketches)
##########################################################################
def mousePressed():
    save_frame_timestamp(filename, timestamp)

def save_frame_timestamp(filename, timestamp='', output_dir='output'):
    '''
    Saves each frame with a structured filename to allow for tracking all output
    '''
    filename = filename.replace('\\', '')
    filename = filename.replace('/', '')
    output_filename = os.path.join(
        output_dir, '{}_{}_{}_####.png'.format(timestamp, filename, rand_seed))
    saveFrame(output_filename)
    print(output_filename)

def circle_point(cx, cy, rx, ry, a):
    '''
    Translates polar coords to cartesian
    '''
    x = cx + rx * cos(a) / 2
    y = cy + ry * sin(a) / 2
    return x, y

def noise_loop(a, r, min_val, max_val, x_c, y_c):
    '''
    Samples 2D Perlin noise in a circle to make smooth noise loops
    Adapted from https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_136_Polar_Noise_Loop_2/P5/noiseLoop.js
    '''
    xoff = map(cos(a), -1, 1, x_c, x_c + 2 * r)
    yoff = map(sin(a), -1, 1, y_c, y_c + 2 * r)
    r = noise(xoff, yoff)
    return map(r, 0, 1, this.min, this.max)

def frange(start, end=None, inc=None):
    '''
    http://code.activestate.com/recipes/66472/
    '''
    if end == None:
        end = start + 0.0
        start = 0.0
    if inc == None:
        inc = 1.0
    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
    return L
