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
record = True  # Save every frame?
animate = True  # Loop through draw()? 
seeded = True  # Set random seeds?

# Canvas size
w = 800  # width
h = 800  # height

# Initializes randomness to make results repeateable (if randomize is set to True)
rand_seed = 1138

# Controls resolution of noise()
noise_increment = 0.03
offset_frame = 0
offset_blob = 0

################################################################################
# Global variables - color
################################################################################
color_background = (60, 7, 86)
color_foreground = (0, 0, 25)
color_stroke = (0, 0, 25)

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
    
    # Stops draw() from running in an infinite loop
    if not animate:
        noLoop()
        
    # Sets random seed value for both Python and Processing 
    if seeded:
        seed(rand_seed)       # Only applies to the random Python module
        randomSeed(rand_seed) # Only applies to the random() Processing function
        noiseSeed(rand_seed)  # Only applies to the noise() Processing function
    
    # Initializes colors for the first frame
    background(*color_background)
    stroke(*color_foreground)
    fill(*color_foreground)

    
# The draw() function is part of Processing, it gets called in an infinite loop every frame
def draw():
    background(*color_background)
    fill(*color_background)
    
    # Allows for modifying global variables. This is done to allow variables to persist through draw() loops
    global offset_frame
    global offset_blob
    global num_blobs
    
    offset_frame += noise_increment
    
    r = 60
    r_delta = 80
    num_points = 200

    for i in range(0, 410, 2):
        offset_blob += 0.02
        beginShape()
        for x, y in circle_noise_locations(w/2+i-200, h/2, r, r_delta, num_points, offset_frame):
            vertex(x, y)
        endShape()
        
    if record:
        save_frame_timestamp(filename, timestamp)

        
def save_frame_timestamp(filename, timestamp='', output_dir='output'):
    '''Saves each frame with a structured filename to allow for tracking all output'''
    filename = filename.replace('\\', '')
    filename = filename.replace('/', '')
    output_filename = os.path.join(output_dir, '{}_{}_{}_####.png'.format(timestamp, filename, rand_seed))
    saveFrame(output_filename)
    print(output_filename)
    
def circle_noise_locations(cx, cy, r, r_delta, n_points, noise_offset):
    offset_angle = 0
    x0, y0 = 0, 0
    for i in range(n_points):
        offset_angle = noise_increment 
        a = i*TAU/n_points
        r_noise = r + map(noise(1*cos(a)+1, cx*0.01, noise_offset), 0, 1, r-r_delta, r+r_delta)
        x = r_noise * cos(a) + cx
        y = 1.6 * r_noise * sin(a) + cy
        # Connects the first point to the last
        if i == 0:
            x0 = x
            y0 = y
        yield x, y
    yield x0, y0
    
def mousePressed():
    save_frame_timestamp(filename, timestamp)
