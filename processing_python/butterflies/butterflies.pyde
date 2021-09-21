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
frame_rate = 1

##########################################################################
# Knobs to turn
##########################################################################

# Canvas size
w = 1000  # width
h = 1000  # height

pal = bug_palette.pal


##########################################################################
# setup()
# function gets run once at start of program
##########################################################################

def setup():

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

    # Stops draw() from running in an infinite loop (should be last line)
    # noLoop()  # Comment to run draw() infinitely (or until 'count' hits
    # limit)


##########################################################################
# draw()
##########################################################################

def draw():
    global timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

    global random_seed
    random_seed = int(frameCount * 1000000 / (second() + 1))
    #random_seed = 75
    random_seed = helper.get_seed(random_seed)
    helper.set_seed(random_seed)

    blend_modes = [BLEND, ADD, SUBTRACT, DARKEST, LIGHTEST,
                   DIFFERENCE, EXCLUSION, MULTIPLY, SCREEN, REPLACE]
    blendMode(blend_modes[0])

    if frameCount == 500:
        exit()

    #palette = pal[int(random(0,len(pal)))]
    #palette_bg_idx = int(random(0, len(palette)))

    background(g.backgroundColor)

    translate(width / 2, height / 2)

    palette_idx = int(random(0, len(pal)))
    palette = pal[palette_idx]

    range_upper_angles = [
        x for x in range(int(random(0, 20)), int(random(50, 80)), int(random(7, 20)))]
    range_lower_angles = [
        x for x in range(int(random(0, 20)), int(random(50, 80)), int(random(7, 20)))]
    range_upper_radii = [width * 0.2, width * 0.45]
    range_lower_radii = [width * 0.2, width * 0.3]

    num_layers = 10

    lines = helper.random_list_value(['none', 'some', 'outer', 'all'])
    print(lines)

    curveTightness(random(-2, 0.6))

    ##########################################################################
    # Upper Wings
    ##########################################################################
    origin = [0, 0]

    upper_wing = {}
    for i in range(num_layers):
        upper_wing[i] = [0, 0]
        for angle in range_upper_angles:
            upper_wing[i].append(helper.circle_points_list(random(0, width * 0.01), random(
                0, height * 0.01), random(width * 0.2, width * 0.4), radians(random(angle - 7, angle))))

    for i in range(7):
        if lines == 'none':
            noStroke()
        elif lines == 'all':
            stroke(0, 0, 0, 60)
        elif lines == 'outer':
            stroke(0, 0, 0, 60)
        elif lines == 'some':
            stroke(0, 0, 0, helper.random_list_value([0, 60]))

        p = palette[int(random(0, len(palette)))]
        if (i == 3) and (i == 6):
            fill(0, 0, 100, 100)
        else:
            fill(p[0], p[1], p[2], 20)
        wing = []
        wing.append(origin)
        for angle in range_upper_angles:
            wing.append(helper.circle_points_list(random(0, width * 0.01), random(0, height * 0.01),
                                                  random(width * 0.2, width * 0.4), radians(random(angle - 7, angle))))

        draw_wings(wing, True)

    for i in range(7):
        if lines == 'none':
            noStroke()
        elif lines == 'all':
            stroke(0, 0, 0, 60)
        elif lines == 'outer':
            noStroke()
        elif lines == 'some':
            stroke(0, 0, 0, helper.random_list_value([0, 60]))

        p = palette[int(random(0, len(palette)))]
        if (i == 3) and (i == 6):
            fill(0, 0, 100, 100)
        else:
            fill(p[0], p[1], p[2], 20)
        wing = []
        wing.append(origin)
        for angle in range_upper_angles:
            wing.append(helper.circle_points_list(random(0, width * 0.01), random(0, height * 0.01),
                                                  random(width * 0.1, width * 0.2), radians(random(angle - 7, angle))))

        draw_wings(wing, True)

    ##########################################################################
    # Lower Wings
    ##########################################################################
    origin = [0, 0]

    for i in range(11):
        if lines == 'none':
            noStroke()
        elif lines == 'all':
            stroke(0, 0, 0, 60)
        elif lines == 'outer':
            stroke(0, 0, 0, 60)
        elif lines == 'some':
            stroke(0, 0, 0, helper.random_list_value([0, 60]))

        p = palette[int(random(0, len(palette)))]
        if (i == 3) and (i == 6):
            fill(0, 0, 100, 100)
        else:
            fill(p[0], p[1], p[2], 20)
        wing = []
        wing.append(origin)
        for angle in range_lower_angles:
            wing.append(helper.circle_points_list(random(0, width * 0.01), random(0, height * 0.01),
                                                  random(width * 0.15, width * 0.3), radians(random(angle - 7, angle))))
        wing.append(helper.circle_points_list(random(0, width * 0.01), random(0,
                                                                              height * 0.01), random(width * 0.15, width * 0.3), radians(random(73, 87))))

        draw_wings(wing)

    for i in range(11):
        if lines == 'none':
            noStroke()
        elif lines == 'all':
            stroke(0, 0, 0, 60)
        elif lines == 'outer':
            noStroke()
        elif lines == 'some':
            stroke(0, 0, 0, helper.random_list_value([0, 60]))

        p = palette[int(random(0, len(palette)))]
        if (i == 3) and (i == 6):
            fill(0, 0, 100, 100)
        else:
            fill(p[0], p[1], p[2], 20)
        wing = []
        wing.append(origin)
        for angle in range_lower_angles:
            wing.append(helper.circle_points_list(random(0, width * 0.01), random(0, height * 0.01),
                                                  random(width * 0.05, width * 0.2), radians(random(angle - 7, angle))))
        wing.append(helper.circle_points_list(random(0, width * 0.01), random(0,
                                                                              height * 0.01), random(width * 0.05, width * 0.2), radians(random(73, 87))))

        draw_wings(wing)

    ##########################################################################
    # Antennae and body
    ##########################################################################
    body = get_16_points(-width * 0.015, -height * 0.15,
                         width * 0.03, height * 0.5)
    curveTightness(0)

    # Body
    fill(0, 0, 100)
    noStroke()
    draw_16_points(body)

    antennae = []
    for i in range(int(random(3, 8))):

        x = body[0][0]
        y = body[0][1]
        r = random(height * 0.1, height * 0.3)
        a = random(range_upper_angles[-1] * 1.2, 80)
        antennae.append(helper.circle_points(x, y, r, radians(a)))

    curve_tightness = []
    for a in antennae:
        curve_tightness.append(random(-2, 0.8))

    pushStyle()
    pushMatrix()

    translate(0, -random(height * 0.24, height * 0.26))
    noFill()
    strokeWeight(width * 0.001)
    stroke(p[0], p[1], 25)

    scale(1, -1)

    beginShape()
    curveVertex(*body[2])
    curveVertex(*body[2])
    for i, (x, y) in enumerate(antennae):
        curveTightness(curve_tightness[i])
        curveVertex(x, y)
    endShape()

    scale(-1, 1)

    beginShape()
    curveVertex(*body[2])
    curveVertex(*body[2])
    for i, (x, y) in enumerate(antennae):
        curveTightness(curve_tightness[i])
        curveVertex(x, y)
    endShape()
    popStyle()
    popMatrix()

    helper.save_frame_timestamp('butterflies_{}_{}'.format(palette_idx, lines), timestamp, random_seed)

    # Save memory by closing image, just look at it in the file system
    # if (w > 1000) or (h > 1000):
    #     exit()


##########################################################################
# Functions
##########################################################################

def draw_wings(wing, upper_wing=False):
    style = helper.random_list_value([BLEND, MULTIPLY, SUBTRACT, DARKEST])
    pushMatrix()
    if upper_wing:
        scale(1, -1)
    blendMode(style)
    draw_curve_filled(wing)
    blendMode(BLEND)
    scale(-1, 1)
    blendMode(style)
    draw_curve_filled(wing)
    blendMode(BLEND)
    popMatrix()


def get_16_points(x, y, w, h):
    squeeze = random(-w * 0.2, w * 0.2)
    points = [0] * 16
    points[0] = [x, y]
    points[1] = [x + w * 0.25, y]
    points[2] = [x + w * 0.5, y - h * 0.05]
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
    for t in data + data[:3]:
        cvp(*t)
    endShape()

def mousePressed():
    helper.save_frame_timestamp('butterflies', timestamp, random_seed)
