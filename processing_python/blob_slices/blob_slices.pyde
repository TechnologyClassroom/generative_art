################################################################################
# code and images by Aaron Penne
# https://github.com/aaronpenne/generative_art
#
# released under the MIT license (https://opensource.org/licenses/MIT)
################################################################################

# Standard Python imports
import datetime
from random import shuffle, seed


################################################################################
# Global variables - knobs to turn
################################################################################

# Logic controls
record = False  # Save every frame?
animate = True  # Loop through draw()? 
seeded = True  # Set random seeds?

# Canvas size
w = 900  # width
h = 1600  # height

# Initializes randomness to make results repeateable (if randomize is set to True)
rand_seed = 1138

min_x = w*0
max_x = w*1
min_y = h*0
max_y = h*1

noise_xy_inc = 0.01
noise_t_inc = 0.02
noise_threshold = 45

toff = 0

################################################################################
# Global variables - color
################################################################################
pal = []

################################################################################
# Global variables - no need to touch
################################################################################

# Gets filename of this script
filename = __file__[:-5]

# Gets current YYMMDD_HHMMSS timestamp (e.g. 20160530_065530)
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


# The setup() function is part of Processing, it gets called one time when this file is run
def setup():
    # Sets size of canvas in pixels (must be first line)
    size(w, h)
    
    # Sets resolution dynamically (affects resolution of saved image)
    pixelDensity(displayDensity())  # 1 for low, 2 for high
    
    # Sets color space to Hue Saturation Brightness with max values of HSB respectively
    colorMode(HSB, 360, 100, 100, 100)
        
    # Set the number of frames per second to display
    frameRate(60)
    
    # Keeps text centered vertically and horizontally at (x,y) coords
    textMode(CENTER)
    textAlign(CENTER, CENTER)
    
    rectMode(CORNERS)
    
    # Stops draw() from running in an infinite loop
    if not animate:
        noLoop()
        
    # Sets random seed value for both Python and Processing 
    if seeded:
        seed(rand_seed)       # Only applies to the random Python module
        randomSeed(rand_seed) # Only applies to the random() Processing function
        noiseSeed(rand_seed)  # Only applies to the noise() Processing function
    
    global pal
    
    # Fisk Mississipi maps
    pal = [color(0,0,100),
           color(0,0,25),
           color(39, 16.9, 92.9), # tan background
           color(48.8, 27, 92.9), # yellowish
           color(152, 15.38, 76.47), # blueish
           color(2.7, 40.3, 86.7), # reddish
           color(60, 18.4, 80.8) # greenish
    ]
    
    # Initializes colors for the first frame
    background(pal[0])
    stroke(pal[1])
    fill(pal[0])
    noStroke()
    
# The draw() function is part of Processing, it gets called in an infinite loop every frame
def draw():
    global pal
    global toff
    
    background(pal[0])
    
    push()
    fill(pal[2])
    noStroke()
    rect(min_x, min_y, max_x, max_y)
    pop()

    # coff = 0
    # draw_blob_slice(noise_xy_inc, noise_threshold, shadow_color(pal[4]), coff-0.1, 7, 7)
    # draw_blob_slice(noise_xy_inc, noise_threshold, shadow_color(pal[4]), coff+0.02, 7, 7)
    # draw_blob_slice(noise_xy_inc, noise_threshold, pal[4], coff, 7, 7)
    
    coff = 1000
    draw_blob_slice(noise_xy_inc, noise_threshold, shadow_color(pal[5]), coff-0.05, 5, 5)
    draw_blob_slice(noise_xy_inc, noise_threshold, pal[5], coff, 5, 5)
    coff = 20
    draw_blob_slice(noise_xy_inc, noise_threshold*1.25, shadow_color(pal[4]), coff-0.05, 5, 5)
    draw_blob_slice(noise_xy_inc, noise_threshold*1.25, pal[4], coff, 5, 5)
    # draw_blob_slice(noise_xy_inc, noise_threshold, pal[6], 0, 20, 20)
    # draw_blob_slice(noise_xy_inc, noise_threshold, pal[4], 20, 20, 20)
    
    toff += noise_t_inc
    
    # Trick to smooth Perlin noise stutter step
    # https://forum.processing.org/two/discussion/21869/confused-about-perlin-animation-result
    if (toff % 1.0 >= 0.975) or (toff % 1.0 < 0.025):
        toff += 0.045
    
    if record:
        save_frame_timestamp(filename, timestamp)
        
def shadow_color(c):
    c_hue = hue(c)
    c_sat = saturation(c)
    c_brite = brightness(c)*0.7
    c_alpha = 100
    return color(c_hue, c_sat, c_brite, c_alpha)

def noise_loop(a, r, min_val, max_val, x_c, y_c):
    # Samples 2D Perlin noise in a circle to make smooth noise loops
    # Adapted from https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_136_Polar_Noise_Loop_2/P5/noiseLoop.js
    xoff = map(cos(a), -1, 1, x_c, x_c + 2*r);
    yoff = map(sin(a), -1, 1, y_c, y_c + 2*r);
    r = noise(xoff, yoff)
    return map(r, 0, 1, this.min, this.max);

def draw_blob_slice(noise_increment=0.02, threshold=50, fill_color=color(0,0,0), offset=0, step=0.5, radius=1):
    xoff = 0
    for x in frange(min_x+radius/2, max_x+radius/2, step):
        yoff = 0
        for y in frange(min_y+radius/2, max_y+radius/2, step):
            noise_value = noise(xoff+offset, yoff+offset, toff)
            alpha_value = map(noise_value, 0, 1, 0, 100)
            if alpha_value>threshold:
                stroke(fill_color, 100)
            else:
                stroke(fill_color, 0)
            strokeWeight(radius)
            point(x, y)
            yoff += noise_increment
        xoff += noise_increment
        
def save_frame_timestamp(filename, timestamp='', output_dir='output'):
    '''Saves each frame with a structured filename to allow for tracking all output'''
    filename = filename.replace('\\', '')
    filename = filename.replace('/', '')
    output_filename = os.path.join(output_dir, '{}_{}_{}_####.png'.format(timestamp, filename, rand_seed))
    saveFrame(output_filename)
    print(output_filename)
    
def mousePressed():
    save_frame_timestamp(filename, timestamp)
    
def frange(start, end=None, inc=None):
    # http://code.activestate.com/recipes/66472/
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
