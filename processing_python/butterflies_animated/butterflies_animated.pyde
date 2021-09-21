##########################################################################
# Aaron Penne
# https://github.com/aaronpenne
##########################################################################

import datetime
import string
import sys
from random import shuffle, seed

import helper
import bug_palette

##########################################################################
# Global variables
##########################################################################

random_seed = 0

# Get time
timestamp = None

# Parameters for draw speed
frame_rate = 30

##########################################################################
# Knobs to turn
##########################################################################

# Canvas size
w = 1000  # width
h = 1000  # height

pal = bug_palette.pal        


upper_angles = [random(x-7, x) for x in range(int(random(0, 20)), int(random(60, 80)), int(random(13, 20)))]
lower_angles = [random(x-7, x) for x in range(int(random(0, 20)), int(random(60, 80)), int(random(13, 20)))]

upper_radii_high = [random(w*0.4, w*0.3) for x in upper_angles]
upper_radii_low = [random(w*0.01, w*0.2) for x in upper_angles]

lower_radii_high = [random(w*0.1, w*0.4) for x in lower_angles]
lower_radii_low = [random(w*0.05, w*0.2) for x in lower_angles]

upper_wing = {}
for i in range(0, 10):
    upper_wing[i] = [[0, 0, 0, 0, 0]]
    for angle in upper_angles:
        x = random(0, w*0.01)
        y = random(0, h*0.01)
        r = random(w*0.25, w*0.4)
        a = radians(random(angle-7, angle))
        phase = random(0, 128) * PI/64
        upper_wing[i].append([x, y, r, a, phase])
    # upper_wing[i].append([x, y, r, radians(random(70, 80)), 0])
for i in range(10, 20):
    upper_wing[i] = [[0, 0, 0, 0, 0]]
    for angle in upper_angles:
        x = random(0, w*0.01)
        y = random(0, h*0.01)
        r = random(w*0.1, w*0.2)
        a = radians(random(angle-7, angle))
        phase = random(0, 128) * PI/64
        upper_wing[i].append([x, y, r, a, phase])
    # upper_wing[i].append([x, y, r, radians(random(70, 80)), 0])
        
lower_wing = {}
for i in range(0, 13):
    lower_wing[i] = [[0, 0, 0, 0, 0]]
    for angle in lower_angles:
        x = random(0, w*0.01)
        y = random(0, h*0.01)
        r = random(w*0.25, w*0.4)
        a = radians(random(angle-7, angle))
        phase = random(0, 128) * PI/64
        lower_wing[i].append([x, y, r, a, phase])
    # lower_wing[i].append([x, y, r, radians(random(70, 80)), 0])
for i in range(13, 26):
    lower_wing[i] = [[0, 0, 0, 0, 0]]
    for angle in lower_angles:
        x = random(0, w*0.01)
        y = random(0, h*0.01)
        r = random(w*0.1, w*0.2)
        a = radians(random(angle-7, angle))
        phase = random(0, 128) * PI/64
        lower_wing[i].append([x, y, r, a, phase]) 
    # lower_wing[i].append([x, y, r, radians(random(70, 80)), 0])
        
palette_idx = int(random(0, len(pal)))
palette = pal[2]
print(palette)

upper_palette = []
for i in upper_wing:
    upper_palette.append(palette[int(random(0, len(palette)))])   
lower_palette = []
for i in lower_wing:
    lower_palette.append(palette[int(random(0, len(palette)))])
      
body = None
angles = None
radii = None
antennae = None
curve_tightness = []

##########################################################################
# setup()
# function gets run once at start of program
##########################################################################

def setup():
    print(frameCount)
    # Sets size of canvas in pixels (must be first line)
    size(w, h)

    # Sets resolution dynamically (affects resolution of saved image)
    pixelDensity(displayDensity())  # 1 for low, 2 for high

    # Sets color space to Hue Saturation Brightness with max values of HSB
    # respectively
    colorMode(HSB, 360, 100, 100, 100)

    # Set the number of frames per second to display
    frameRate(frame_rate)

    background(0, 0, 100)

    rectMode(CORNER)

    global body, angles, radii, antennae, curve_tightness
    
    
    # Antennae
    body = get_16_points(-w*0.015, -h*0.2, w*0.03, h*0.4)
    angles, radii = get_angles_radii_antennae(10, w*0.1)
    
    
    antennae = []
    for i in range(int(random(3, 8))):
        x = body[0][0]
        y = body[0][1]
        r = random(height * 0.1, height * 0.3)
        a = random(45, 80) 
        phase = random(0, 128) * PI/64
        antennae.append([x, y, r, a, phase])

    for a in antennae:
        curve_tightness.append(random(-2, 0.8))

    # Stops draw() from running in an infinite loop (should be last line)
    #noLoop()  # Comment to run draw() infinitely (or until 'count' hits limit)


##########################################################################
# draw()
##########################################################################

def draw():
    global timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    global random_seed
    random_seed = int(frameCount*100000/(second()+1))
    random_seed = 1143
    random_seed = helper.get_seed(random_seed)
    helper.set_seed(random_seed)
    
    global body, angles, radii, antennae, curve_tightness
    
    steps = 32
    
    if frameCount >= 2*steps:
        exit()
    
    #palette = pal[int(random(0,len(pal)))]        
    #palette_bg_idx = int(random(0, len(palette)))
    
    background(g.backgroundColor)

    translate(width/2, height/2)
    
    curveTightness(curve_tightness[-1])

            
    ##########################################################################
    # Upper Wings
    ##########################################################################
    
    #stroke(0, 0, 0, 60)
    noStroke()
    
    for i in upper_wing:
        layer = []
        p = upper_palette[i]     
        if (i==3) and (i==6):
            fill(0, 0, 100, 20)
        else:
            fill(p[0], p[1], p[2], 20)
            
        for x, y, r, a, phase in upper_wing[i]:
            r = r + sin(frameCount*PI/steps+phase) * 15
            layer.append(helper.circle_points_list(x, y, r, a))

        draw_wings(layer, True)
    
    

    ##########################################################################
    # Lower Wings
    ##########################################################################
   
    for i in lower_wing:
        layer = []
        p = lower_palette[i]     
        if (i==3) and (i==6):
            fill(0, 0, 100, 20)
        else:
            fill(p[0], p[1], p[2], 20)
            
        for x, y, r, a, phase in lower_wing[i]:
            r = r + sin(frameCount*PI/steps+phase) * 11
            layer.append(helper.circle_points_list(x, y, r, a))

        draw_wings(layer)
    

    
    ##########################################################################
    # Antennae and body
    ##########################################################################
    
    
    
    antennae_points = []
    for x, y, r, a, phase in antennae:
        r = r + sin(frameCount*PI/steps+phase) * 5
        a = a + sin(frameCount*PI/steps+phase) * 7
        antennae_points.append(helper.circle_points_list(x, y, r, radians(a)))
    
    # Body
    fill(0, 0, 100)
    noStroke()
    draw_16_points(body)
        
    pushStyle()
    pushMatrix()

    translate(0, -random(height * 0.32, height * 0.35))
    noFill()
    strokeWeight(width * 0.001)
    stroke(p[0], p[1], 25)

    scale(1, -1)

    beginShape()
    curveVertex(*body[2])
    curveVertex(*body[2])
    for i, (x, y) in enumerate(antennae_points):
        curveTightness(curve_tightness[i])
        curveVertex(x, y)
    endShape()

    scale(-1, 1)

    beginShape()
    curveVertex(*body[2])
    curveVertex(*body[2])
    for i, (x, y) in enumerate(antennae_points):
        curveTightness(curve_tightness[i])
        curveVertex(x, y)
    endShape()
    popStyle()
    popMatrix()

    helper.save_frame_timestamp('butterflies', timestamp, random_seed)

    # Save memory by closing image, just look at it in the file system
    # if (w > 1000) or (h > 1000):
    #     exit()


##########################################################################
# Functions
##########################################################################

def draw_wings(wing, upper_wing=False):
    pushMatrix()
    if upper_wing:
        scale(1,-1)
    draw_curve_filled(wing)
    scale(-1,1)
    draw_curve_filled(wing)
    popMatrix()


def get_16_points(x, y, w, h):
    squeeze = random(w*0.2, w*0.3)
    points = [0] * 16
    points[0] = [x, y]
    points[1] = [x + w * 0.25, y]
    points[2] = [x + w * 0.5, y-h*0.05]
    points[3] = [x + w * 0.75, y]
    points[4] = [x + w, y]
    points[5] = [x + w, y + h * 0.25]
    points[6] = [x + w + squeeze, y + h * 0.5]
    points[7] = [x + w, y + h * 0.75]
    points[8] = [x + w, y + h]
    points[9] = [x + w * 0.75, y + h]
    points[10] = [x + w * 0.5, y + h]
    points[11] = [x + w * 0.25, y + h]
    points[12] = [x, y + h]
    points[13] = [x, y + h * 0.75]
    points[14] = [x - squeeze, y + h * 0.5]
    points[15] = [x, y + h * 0.25]
    
    points.pop(12)
    points.pop(8)
    points.pop(4)
    points.pop(0)
    
    return points

def cvp(x, y):
    curveVertex(x, y)
    #ellipse(x, y, 5, 5)
    
def draw_16_points(points):
    beginShape()
    for p in points + points[0:3]:
        cvp(*p)
    endShape()


def draw_curve_filled(data):
    beginShape()
    for t in data+data[:3]:
        cvp(*t)
    endShape()

def get_angles_radii_antennae(angle_offset, r):                    
    angles = [0]*4
    angles[0] = helper.random_centered(180, angle_offset)
    angles[1] = helper.random_centered(90, angle_offset)
    angles[2] = helper.random_centered(30, angle_offset)
    angles[3] = helper.random_centered(300, angle_offset)
    
    radii = [0]*4
    radii[0] = random(r*0.45, r*0.75)
    radii[1] = random(r*0.25, r*0.5)
    radii[2] = random(r*0.15, r*0.3)
    radii[3] = random(r*0.1, r*0.15)

    return angles, radii

def mousePressed():
    helper.save_frame_timestamp('butterflies', timestamp, random_seed)
