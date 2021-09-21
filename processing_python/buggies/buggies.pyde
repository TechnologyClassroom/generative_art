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
    #noLoop()  # Comment to run draw() infinitely (or until 'count' hits limit)


##########################################################################
# draw()
# function gets run repeatedly (unless noLoop() called in setup())
#
# 0--1--2--3--4
# |           |
# 15          5
# |           |
# 14          6
# |           |
# 13          7
# |           |
# 12-11-10--9-8
#
#
##########################################################################

def draw():
    global timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    global random_seed
    random_seed = int(frameCount*1000000/(second()+1))
    #random_seed = 113
    random_seed = helper.get_seed(random_seed)
    helper.set_seed(random_seed)
    
    palette_idx = int(random(0,len(pal)))
    palette = pal[palette_idx]        
    palette_bg_idx = int(random(0, len(palette)))
    
    if frameCount == 500:
        exit()

    counter = frameCount % 100

    background(g.backgroundColor)

    noFill()
    noStroke()

    r = 200

    translate(width / 2, height / 2)

    # Full bug
    w_bug = random(width*0.2, width*0.5)
    # Calculate based on ratio (w_bug*random_multiplier)
    h_bug = random(height*0.3, height*0.6)
    x_0 = 0 - w_bug / 2
    y_0 = 0 - h_bug / 2

    # Head
    w_head_offset = 0.5
    x_head = x_0+w_bug*(1-w_head_offset)/2
    y_head = y_0
    w_head = w_bug*w_head_offset
    h_head = random(0, h_bug * 0.2)

    # Pronotum
    w_pron_offset = 0.9
    g_pron = random(0, 15)  # gap
    x_pron = x_0+w_bug*(1-w_pron_offset)/2
    y_pron = y_head + h_head + g_pron
    w_pron = w_bug*w_pron_offset
    h_pron = random(0, h_bug * 0.3)

    # Elytron
    g_elyt = random(0, 15)
    x_elyt = x_0
    y_elyt = y_pron + h_pron + g_elyt
    w_elyt = w_bug
    h_elyt = h_bug - h_head - h_pron

    w_eyes = 50
    h_eyes = 50
    

    
    fill(0, 0, 50)
    head = get_16_points(x_head, y_head, w_head, h_head)
    pron = get_16_points(x_pron, y_pron, w_pron, h_pron)
    elyt = get_16_points(x_elyt, y_elyt, w_elyt, h_elyt)
    l_wing = get_16_points(elyt[0][0], elyt[0][1], w_elyt / 2, h_elyt)
    r_wing = get_16_points(elyt[2][0], elyt[2][1], w_elyt / 2, h_elyt)
    l_eye = get_16_points(head[1][0]-w_eyes/2, head[1][1], h_eyes, w_eyes)
    r_eye = get_16_points(head[3][0]-w_eyes/2, head[3][1], h_eyes, w_eyes)


    ##########################################################################
    # Legs
    ##########################################################################
    wing_x_squeeze = 50
    
    elyt[7][0] -= wing_x_squeeze*1.1
    elyt[13][0] += wing_x_squeeze*1.1
    elyt[14][0] += wing_x_squeeze
    
    elyt[0] = [pron[12][0], pron[12][1]-h_pron*0.1]
    elyt[2] = [pron[10][0], pron[10][1]-h_pron*0.1]
    elyt[4] = [pron[8][0], pron[8][1]-h_pron*0.1]
    
    arm_length_a = w_elyt*random(0.01, 0.1)
    arm_length_b = h_elyt*random(0.01, 0.4)
    arm_length_c = h_elyt*random(0.01, 0.4)
    arm_width_a = random(15, 30)
    arm_width_b = random(15, 30)
    arm_width_c = random(15, 30)
    
    up_angle_a = random(200, 260)
    up_angle_b = random(200, 340)
    up_angle_c = random(200, 340)
    dn_angle_a = random(145, 185)
    dn_angle_b = random(60, 160)
    dn_angle_c = random(60, 160)
    
    
    pushStyle()
    c = palette[palette_bg_idx]
    fill(c[0], c[1], random(5, 25))
    draw_leg(pron[14][0], pron[14][1], arm_length_a, up_angle_a, 50, arm_length_b, up_angle_b, 5, arm_length_c, up_angle_c, 5)
    draw_leg(elyt[15][0], elyt[15][1], arm_length_a, dn_angle_a, 50, arm_length_b, dn_angle_b, 5, arm_length_c, dn_angle_c, 5, True)
    draw_leg(elyt[14][0], elyt[14][1], arm_length_a, dn_angle_a, 50, arm_length_b, dn_angle_b, 5, arm_length_c, dn_angle_c, 5, True)
    pushMatrix()
    scale(-1.0, 1.0)  
    draw_leg(pron[14][0], pron[14][1], arm_length_a, up_angle_a, 50, arm_length_b, up_angle_b, 5, arm_length_c, up_angle_c, 5)
    draw_leg(elyt[15][0], elyt[15][1], arm_length_a, dn_angle_a, 50, arm_length_b, dn_angle_b, 5, arm_length_c, dn_angle_c, 5, True)
    draw_leg(elyt[14][0], elyt[14][1], arm_length_a, dn_angle_a, 50, arm_length_b, dn_angle_b, 5, arm_length_c, dn_angle_c, 5, True)
    popMatrix()
    popStyle()
    
    
    ##########################################################################
    # Neck
    ##########################################################################
    curve_tightness = random(0.5, 0.9)
    
    pushStyle()
    
    m = createGraphics(width, height)
    m.beginDraw()
    m.pushMatrix()
    m.translate(width/2, height/2)
    m.beginShape()
    m.curveTightness(curve_tightness)
    m.curveVertex(head[12][0]+w_head*0.05, head[11][1]-g_pron*2)
    m.curveVertex(head[8][0]-w_head*0.05, head[9][1]-g_pron*2)
    m.curveVertex(head[8][0]+w_head*0.2, head[9][1]+g_pron*2)
    m.curveVertex(head[12][0]-w_head*0.2, head[11][1]+g_pron*2)
    m.curveVertex(head[12][0]+w_head*0.05, head[11][1]-g_pron*2)
    m.curveVertex(head[8][0]-w_head*0.05, head[9][1]-g_pron*2)
    m.curveVertex(head[8][0]+w_head*0.2, head[9][1]+g_pron*2)
    m.endShape()
    m.endDraw()
    m.popMatrix()
    
    pattern = get_pattern('bg', 0.7, palette, palette_bg_idx)
    pattern.mask(m)
    image(pattern, -width/2, -height/2)
    
    pushStyle()
    noFill()
    #stroke(0, 0, 20)
    beginShape()
    cvp(head[12][0]+w_head*0.1, head[11][1]-g_pron)
    cvp(head[8][0]-w_head*0.1, head[9][1]-g_pron)
    cvp(head[8][0]+w_head*0.2, head[9][1]+g_pron*2)
    cvp(head[12][0]-w_head*0.2, head[11][1]+g_pron*2)
    cvp(head[12][0]+w_head*0.1, head[11][1]-g_pron)
    cvp(head[8][0]-w_head*0.1, head[9][1]-g_pron)
    cvp(head[8][0]+w_head*0.2, head[9][1]+g_pron*2)
    endShape()
    popStyle()
    
    ##########################################################################
    # Eyes
    ##########################################################################
    # l_eye[8][0] -= 10
    # l_eye[8][1] -= 10
    # r_eye[12][0] += 10
    # r_eye[12][1] -= 10
    
    # pushStyle()
    # fill(0, 0, 90)
    # curveTightness(-0.5)
    # beginShape()
    # cvp(*l_eye[15])
    # cvp(*l_eye[4])
    # cvp(*l_eye[8])
    # cvp(*l_eye[13])
    # cvp(*l_eye[15])
    # cvp(*l_eye[4])
    # cvp(*l_eye[8])
    # endShape()
    
    # beginShape()
    # cvp(*r_eye[0])
    # cvp(*r_eye[5])
    # cvp(*r_eye[7])
    # cvp(*r_eye[12])
    # cvp(*r_eye[0])
    # cvp(*r_eye[5])
    # cvp(*r_eye[7])
    # endShape()
    
    # popStyle()


    ##########################################################################
    # Head
    ##########################################################################
    curve_tightness = random(-2, 1)
    

    angles, radii = get_angles_radii(random(5, 30), w_head*0.1, w_head*0.8)
    
    x_ = head[10][0]
    y_ = head[10][1] - random(-radii[2]*0.2, radii[2]*0.5)
    
    m = createGraphics(width, height)
    m.beginDraw()
    m.curveTightness(curve_tightness)
    m.pushMatrix()
    m.translate(width/2, height/2)
    m.beginShape()
    for a, r in zip(angles, radii):
        x, y = helper.circle_points(x_, y_, r, radians(a))
        m.curveVertex(x, y)
    m.endShape()
    m.endDraw()
    m.popMatrix()
    
    pattern = get_pattern('bg', random(0.5, 0.7), palette, palette_bg_idx)
    pattern.mask(m)
    image(pattern, -width/2, -height/2)
    
    pushStyle()
    beginShape()
    noFill()
    stroke(0, 0, 0)
    strokeWeight(1)
    curveTightness(curve_tightness)
    for a, r in zip(angles, radii):
        x, y = helper.circle_points(x_, y_, r, radians(a))
        curveVertex(x, y)
    endShape()
    popStyle()
    
    
    
    ##########################################################################
    # Elytron
    ##########################################################################
    m = createGraphics(width, height)
    m.beginDraw()
    m.pushMatrix()
    m.translate(width/2, height/2)
    m.beginShape()
    m.curveVertex(*elyt[0])
    m.curveVertex(*elyt[2])
    m.curveVertex(*elyt[4])
    m.curveVertex(*elyt[7])
    m.curveVertex(*elyt[10])
    m.curveVertex(*elyt[13])
    m.curveVertex(*elyt[0])
    m.curveVertex(*elyt[2])
    m.curveVertex(*elyt[4])
    m.endShape()
    m.endDraw()
    m.popMatrix()

    pattern = get_pattern('bg', 0.3, palette, palette_bg_idx)
    pattern.mask(m)
    image(pattern, -width/2, -height/2)
    

    pushStyle()
    noFill()
    #stroke(0, 0, 20)
    beginShape()
    cvp(*elyt[0])
    cvp(*elyt[2])
    cvp(*elyt[4])
    cvp(*elyt[7])
    cvp(*elyt[10])
    cvp(*elyt[13])
    cvp(*elyt[0])
    cvp(*elyt[2])
    cvp(*elyt[4])
    endShape()
    popStyle()

    ##########################################################################
    # Pronotum
    ##########################################################################
    pron[0][0] += w_pron*0.1
    pron[4][0] -= w_pron*0.1
    rw = w_pron*0.1
    rh = h_pron*0.1
    rand_00 = random(-rw, rw)
    rand_01 = random(-rh, rh)
    rand_2 = random(-rh, rh)
    rand_70 = random(-rw, rw)
    rand_71 = random(-rh, rh)
    rand_10 = random(-rh, rh)
    
    pron[0][0] += rand_00
    pron[0][1] += rand_01
    pron[2][1] += rand_2
    pron[4][0] -= rand_00
    pron[4][1] += rand_01
    pron[10][1] += rand_10

        
    m = createGraphics(width, height)
    m.beginDraw()
    m.pushMatrix()
    m.translate(width/2, height/2)
    m.beginShape()
    m.curveVertex(*pron[0])
    m.curveTightness(0.7)
    m.curveVertex(*pron[2])
    m.curveTightness(0)
    m.curveVertex(*pron[4])
    m.curveVertex(*pron[7])
    m.curveTightness(0.7)
    m.curveVertex(*pron[10])
    m.curveTightness(0)
    m.curveVertex(*pron[13])
    m.curveVertex(*pron[0])
    m.curveTightness(0.7)
    m.curveVertex(*pron[2])
    m.curveTightness(0)
    m.curveVertex(*pron[4])
    m.endShape()
    m.endDraw()
    m.popMatrix()

    pattern = get_pattern('bg', random(0.5, 0.7), palette, palette_bg_idx)
    pattern.mask(m)
    image(pattern, -width/2, -height/2)
    
    # Outline
    pushStyle()
    noFill()
    stroke(0, 0, 0)
    strokeWeight(1)
    beginShape()
    cvp(*pron[0])
    curveTightness(0.7)
    cvp(*pron[2])
    curveTightness(0)
    cvp(*pron[4])
    cvp(*pron[7])
    curveTightness(0.7)
    cvp(*pron[10])
    curveTightness(0)
    cvp(*pron[13])
    cvp(*pron[0])
    curveTightness(0.7)
    cvp(*pron[2])
    curveTightness(0)
    cvp(*pron[4])
    endShape()
    popStyle()
    
    ##########################################################################
    # Wing Coverings
    ##########################################################################
    wing_mid_offset = 50
    #elyt[2][1] += 50

    #r_wing[7][0] -= wing_x_squeeze
    l_wing[13][0] += wing_x_squeeze

    for i in [0, 2, 12, 13]:
        l_wing[i][0] = helper.random_centered(l_wing[i][0], w_elyt*0.1)
        l_wing[i][1] = helper.random_centered(l_wing[i][1], w_elyt*0.1)
    
    pattern_style = helper.random_list_value(['dots', 'butterball'])
    pattern = get_pattern(pattern_style, 1, palette, palette_bg_idx)
        
    # Left wing (to be mirrored)
    m = createGraphics(width, height)
    m.beginDraw()
    m.pushMatrix()
    # rotate(PI/40)
    m.translate(width/2, height/2)
    m.beginShape()
    m.curveVertex(*l_wing[0])
    m.curveVertex(*l_wing[2])
    m.curveVertex(l_wing[5][0], l_wing[5][1]-h*0.05)
    m.curveVertex(*l_wing[8])
    m.curveTightness(0.9)
    m.curveVertex(*l_wing[13])
    m.curveTightness(0)
    m.curveVertex(*l_wing[0])
    m.curveVertex(*l_wing[2])
    m.curveVertex(l_wing[5][0], l_wing[5][1]-h*0.05)
    m.endShape()
    m.endDraw()
    m.popMatrix()
    
    # Clip/Mask the pattern to wing size
    pattern.mask(m)
    pushMatrix()
    image(pattern, -width/2, -height/2)
    outline_wing(l_wing)
    # Mirror the wing
    scale(-1.0, 1.0)
    image(pattern, -width/2, -height/2)
    outline_wing(l_wing)
    popMatrix()

    
    ##########################################################################
    # Antennae
    ##########################################################################
    angles, radii = get_angles_radii_antennae(30, width*0.2)
    
    x_ = random(-width*0.3, -width*0.1)
    y_ = random(-height*0.3, height*0.2)
    
    curve_tightness = []
    for a in angles:
        curve_tightness.append(random(-3, 0.6))
        
    p = palette[palette_bg_idx]
    
    break_point = int(random(2, len(angles)))
    pushMatrix()
    noFill()
    strokeWeight(width*0.002)
    stroke(p[0], p[1], 10)
    beginShape()  
    curveTightness(curve_tightness[0])
    x, y = helper.circle_points(x_, y_, angles[-1], radii[-1])
    curveVertex(x, y)
    curveVertex(pron[1][0], pron[1][1])
    # curveVertex(x_head-random(w_head*0.01, w_head*0.8), y_head-random(h_head*0.01, h_head*0.5))
    for i, (a, r, c) in enumerate(zip(angles, radii, curve_tightness)):  
        if i >= break_point:
            break
        curveTightness(c)
        x, y = helper.circle_points(x_, y_, r, radians(a))
        curveVertex(x, y)
    endShape()
    curveTightness(0)
    
    scale(-1, 1)
    noFill()
    strokeWeight(width*0.002)
    stroke(p[0], p[1], 10)
    beginShape()   
    curveTightness(curve_tightness[0])
    x, y = helper.circle_points(x_, y_, angles[-1], radii[-1])
    curveVertex(x, y)
    curveVertex(pron[1][0], pron[1][1])
    # curveVertex(x_head-random(w_head*0.01, w_head*0.8), y_head-random(h_head*0.01, h_head*0.5))
    for i, (a, r, c) in enumerate(zip(angles, radii, curve_tightness)):    
        if i >= break_point:
            break
        curveTightness(c)
        x, y = helper.circle_points(x_, y_, r, radians(a))
        curveVertex(x, y)
    endShape()
    curveTightness(0)
    popMatrix()
    
    

    helper.save_frame_timestamp('buggies_{}'.format(palette_idx), timestamp, random_seed)

    # Save memory by closing image, just look at it in the file system
    # if (w > 1000) or (h > 1000):
    #     exit()


##########################################################################
# Functions
##########################################################################

def draw_leg(x, y, length_a=100, angle_a=165, span_a=50, length_b=200, angle_b=105, span_b=5, length_c=200, angle_c=95, span_c=5, upper_leg=False):
    # Arm A
    angle = angle_a
    span = span_a
    x = x+5
    y = y
    ax1, ay1 = helper.circle_points(x+20, y, -10, radians(angle+span+180))
    ax2, ay2 = helper.circle_points(x+20, y, -10, radians(angle+180))
    ax3, ay3 = helper.circle_points(x+20, y, -10, radians(angle-span+180))
    ax4, ay4 = helper.circle_points(x, y, length_a, radians(angle-span))
    ax5, ay5 = helper.circle_points(x, y, length_a, radians(angle))
    ax6, ay6 = helper.circle_points(x, y, length_a, radians(angle+span))
    
    # Arm B
    angle = angle_b
    span = span_b
    x = ax4
    y = ay4
    bx1, by1 = helper.circle_points(x-span, y, 0, radians(angle+span+180))
    bx2, by2 = helper.circle_points(x, y, 0, radians(angle+180))
    bx3, by3 = helper.circle_points(x+span, y, 0, radians(angle-span+180))
    bx4, by4 = helper.circle_points(x, y, length_b, radians(angle-span))
    bx5, by5 = helper.circle_points(x, y, length_b, radians(angle))
    bx6, by6 = helper.circle_points(x, y, length_b, radians(angle+span))
    
    # Arm C
    angle = angle_c
    span = span_c
    x = bx5
    y = by5
    cx1, cy1 = helper.circle_points(x-span, y, 0, radians(angle+span+180))
    cx2, cy2 = helper.circle_points(x, y, 0, radians(angle+180))
    cx3, cy3 = helper.circle_points(x+span, y, 0, radians(angle-span+180))
    cx4, cy4 = helper.circle_points(x, y, length_c, radians(angle-span))
    cx5, cy5 = helper.circle_points(x, y, length_c, radians(angle))
    cx6, cy6 = helper.circle_points(x, y, length_c, radians(angle+span))
    
    beginShape()
    cvp(cx1, cy1) if upper_leg else  cvp(cx3, cy3)
    cvp(cx2, cy2)
    cvp(cx3, cy3) if upper_leg else  cvp(cx1, cy1)
    cvp(cx4, cy4)
    cvp(cx5, cy5)
    cvp(cx6, cy6)
    cvp(cx1, cy1) if upper_leg else  cvp(cx3, cy3)
    cvp(cx2, cy2)
    cvp(cx3, cy3) if upper_leg else  cvp(cx1, cy1)
    endShape()
    
    beginShape()
    curveTightness(0.8)
    cvp(bx1, by1) if upper_leg else  cvp(bx3, by3)
    cvp(bx2, by2)
    cvp(bx3, by3) if upper_leg else  cvp(bx1, by1)
    cvp(bx4, by4)
    cvp(bx5, by5)
    cvp(bx6, by6)
    cvp(bx1, by1) if upper_leg else  cvp(bx3, by3)
    cvp(bx2, by2)
    cvp(bx3, by3) if upper_leg else  cvp(bx1, by1)
    curveTightness(0)
    endShape()
    
    beginShape()
    cvp(ax1, ay1)
    cvp(ax2, ay2)
    cvp(ax3, ay3)
    cvp(ax4, ay4)
    cvp(ax5, ay5)
    cvp(ax6, ay6)
    cvp(ax1, ay1)
    cvp(ax2, ay2)
    cvp(ax3, ay3)
    endShape()


def get_pattern(pattern_style, lightness_offset, palette, palette_bg_idx):
    bg_color = palette[palette_bg_idx]
    
    style = int(random(1, 10))
    
    blend_mode = helper.random_list_value([BLEND, MULTIPLY, SUBTRACT, LIGHTEST])
   
    if pattern_style == 'dots':
        pattern = createGraphics(width, height)
        pattern.beginDraw()
        pattern.pushMatrix()
        pattern.blendMode(blend_mode)
        pattern.background(color(bg_color[0], bg_color[1], bg_color[2]*lightness_offset)) # mauve
        #pattern.translate(width/2, height/2)
        pattern.noStroke()
        for i in range(int(random(20, 40))):
            fg_color = palette[int(random(0, len(palette)))]
            pattern.fill(color(fg_color[0], fg_color[1], fg_color[2]*lightness_offset))
            r = random(5, 200)
            x = random(0, width)
            y = random(0, height)
            pattern.ellipse(x, y, r, r*random(1.2, 3))
        pattern.endDraw()
        pattern.popMatrix
        
    if pattern_style == 'butterball':
        pattern = createGraphics(width, height)
        pattern.beginDraw()
        pattern.pushMatrix()
        pattern.blendMode(blend_mode)
        pattern.background(color(bg_color[0], bg_color[1], bg_color[2]*lightness_offset))
        pattern.translate(width/2-random(0, width*0.05), height/2)
        pattern.noStroke()
        pattern.curveTightness(0)
        for i in range(int(random(3, 11))):
            fg_color = palette[int(random(0, len(palette)))]
            pattern.fill(color(fg_color[0], fg_color[1], fg_color[2]*lightness_offset, 100))
            
            pattern.beginShape()
            for angle in [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 0, 20, 40]:
                r = random(width*0.01, width*0.3)
                a = radians(random(angle-7, angle))
                x_ = random(-width*0.1, width*0.1) if style%2==0 else 0
                y_ = random(-height*0.1, height*0.1) if style%2==0 else 0
                x, y = helper.circle_points(x_, y_, r, a)
                pattern.curveVertex(x, y)
            pattern.endShape()
            
        pattern.endDraw()
        pattern.popMatrix
        
    elif pattern_style == 'bg':
        pattern = createGraphics(width, height)
        pattern.beginDraw()
        pattern.pushMatrix()
        pattern.background(color(bg_color[0], bg_color[1], bg_color[2]*lightness_offset)) # mauve
        pattern.endDraw()
        pattern.popMatrix
        
    elif pattern_style == 'gradient':
        pattern = createGraphics(width, height)
        pattern.beginDraw()
        pattern.pushMatrix()
        pattern.blendMode(blend_mode)
        pattern.background(color(0, 100, 100*lightness_offset)) # mauve
        #pattern.translate(width/2, height/2)
        pattern.noStroke()
        for i in range(40):
            pattern.fill(color(random(0, 360), random(20,30), random(60,90), 50*lightness_offset)) # green
            r = random(200, 1000)
            x = random(0, width)
            y = random(0, height)
            pattern.ellipse(x, y, r, r)
        pattern.endDraw()
        pattern.popMatrix
        
        
    blendMode(BLEND)
    
    return pattern


def outline_wing(l_wing):
    pushStyle()
    noFill()
    stroke(0, 0, 0)
    strokeWeight(1)
    
    pushMatrix()
    # rotate(PI/40)
    beginShape()
    cvp(*l_wing[0])
    cvp(*l_wing[2])
    cvp(l_wing[5][0], l_wing[5][1]-h*0.05)
    cvp(*l_wing[8])
    curveTightness(0.9)
    cvp(*l_wing[13])
    curveTightness(0)
    cvp(*l_wing[0])
    cvp(*l_wing[2])
    cvp(l_wing[5][0], l_wing[5][1]-h*0.05)
    endShape()
    popMatrix()
    popStyle()
    

def cvp(x, y):
    curveVertex(x, y)
    #ellipse(x, y, 5, 5)


def get_16_points(x, y, w, h):
    points = [0] * 16
    points[0] = [x, y]
    points[1] = [x + w * 0.25, y]
    points[2] = [x + w * 0.5, y]
    points[3] = [x + w * 0.75, y]
    points[4] = [x + w, y]
    points[5] = [x + w, y + h * 0.25]
    points[6] = [x + w, y + h * 0.5]
    points[7] = [x + w, y + h * 0.75]
    points[8] = [x + w, y + h]
    points[9] = [x + w * 0.75, y + h]
    points[10] = [x + w * 0.5, y + h]
    points[11] = [x + w * 0.25, y + h]
    points[12] = [x, y + h]
    points[13] = [x, y + h * 0.75]
    points[14] = [x, y + h * 0.5]
    points[15] = [x, y + h * 0.25]
    return points


def draw_curve_filled(data):
    beginShape()
    for t in data+data[:3]:
        cvp(*t)
    endShape()
    
    
def draw_16_points(points):
    beginShape()
    for p in points + points[0:3]:
        cvp(*p)
    endShape()


def draw_12_points(points):
    #points = [points[i] for i in [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15]]
    curveTightness(0.3)
    beginShape()
    for p in points + points[0:3]:
        cvp(*p)
    endShape()

def get_angles_radii(angle_offset, r_min, r_max):
    angles = [0]*11
    angles[0] = helper.random_centered(0, angle_offset)
    angles[1] = helper.random_centered(45, angle_offset)
    angles[2] = helper.random_centered(90, angle_offset)
    angles[3] = 180 - angles[1]
    angles[4] = 180 - angles[0]
    angles[5] = helper.random_centered(225, angle_offset)
    angles[6] = 270
    angles[7] = 180 - angles[5]
    angles[8] = angles[0]
    angles[9] = angles[1]
    angles[10] = angles[2]

    radii = [0]*11
    radii[0] = random(r_min, r_max)
    radii[1] = random(r_min, r_max)
    radii[2] = random(r_min, r_max)
    radii[3] = radii[1]
    radii[4] = radii[0]
    radii[5] = random(r_min, r_max)
    radii[6] = random(r_min, r_max)
    radii[7] = radii[5]
    radii[8] = radii[0]
    radii[9] = radii[1]
    radii[10] = radii[2]

    return angles, radii


def get_angles_radii_antennae(angle_offset, r):                    
    angles = [0]*6
    angles[0] = helper.random_centered(315, angle_offset)
    angles[1] = helper.random_centered(270, angle_offset)
    angles[2] = helper.random_centered(180, angle_offset)
    angles[3] = helper.random_centered(90, angle_offset)
    angles[4] = helper.random_centered(30, angle_offset)
    angles[5] = helper.random_centered(300, angle_offset)
    
    radii = [0]*6
    radii[0] = random(r*0.85, r)
    radii[1] = random(r*0.7, r*0.9)
    radii[2] = random(r*0.45, r*0.75)
    radii[3] = random(r*0.25, r*0.5)
    radii[4] = random(r*0.15, r*0.3)
    radii[5] = random(r*0.1, r*0.15)

    return angles, radii

def mousePressed():
    helper.save_frame_timestamp('buggies', timestamp, random_seed)
