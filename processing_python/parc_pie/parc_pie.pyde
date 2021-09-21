
import datetime
from random import shuffle, seed


################################################################################
# Global variables
################################################################################

# Get time 
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Set random seed value for both Python 'random' and Processing 'random'
rand_seed = 1138
print(rand_seed)
# Comment out seeds below to get new shape on every run
seed(rand_seed) # This only applys to the Python random functions
randomSeed(rand_seed) # This only applys to the Processing random functions


################################################################################
# Knobs to turn
################################################################################

record = False
animate = True
animate_mode = 'sinusoid'

# Canvas size
w = 1000  # width
h = 1000  # height

steps = 100
num_loops = 4

x_spots = 10
y_spots = 10

frame_rate = 15

c_tan = (41, 13, 97) #f8eed9
c_red = (351, 95, 77) #c40926
c_blue = (245, 90, 59) #1b0f96

w_pad = w*0.12
h_pad = h*0.12

x_min = w_pad
x_max = w - w_pad
x_rad = (x_max - x_min)/9

y_min = h_pad
y_max = h - h_pad
y_rad = (y_max - y_min)/9

def setup():
    # Sets size of canvas in pixels (must be first line)
    size(w, h) # (width, height)
    
    # Sets resolution dynamically (affects resolution of saved image)
    pixelDensity(displayDensity())  # 1 for low, 2 for high
    
    # Sets color space to Hue Saturation Brightness with max values of HSB respectively
    colorMode(HSB, 360, 100, 100, 100)
        
    # Set the number of frames per second to display
    frameRate(frame_rate)

    # Stops draw() from running in an infinite loop (should be last line)
    if not animate:
        noLoop()  # Comment to run draw() infinitely (or until 'count' hits limit) 

    
def draw():
    if frameCount > (steps * num_loops):
        exit()
        
    background(*c_tan)
    noStroke()
    
    up_start = 3*TAU/8
    up_stop = 7*TAU/8
    down_start = 3*TAU/8 - PI
    down_stop = 7*TAU/8 - PI
    
    if animate_mode == 'sinusoid':
        up_start_offset = sin(frameCount*TAU/steps)
        up_stop_offset = sin(frameCount*TAU/(steps/2))
        down_start_offset = cos(frameCount*TAU/(steps/2))
        down_stop_offset = cos(frameCount*TAU/steps)
    else:
        up_start_offset = 0
        up_stop_offset = 0
        down_start_offset = 0
        down_stop_offset = 0
        
    if animate:
        up_start = up_start + up_start_offset
        up_stop = up_stop - up_stop_offset
        down_start = down_start + down_start_offset
        down_stop = down_stop - down_stop_offset
        
        # Sets up top and bottom rows
        top = [x/9.0 for x in range(10)]
        btm = [x/9.0 for x in range(10)]
        btm.reverse() # reverses list in place
    
    # Loops through grid and assign values to each pie
    for i_x in range(10):
        
        # Calculates x location (in pixels) using interpolation (lerp)
        x = lerp(x_min, x_max, i_x/9.0)
        
        for i_y in range(10): 
                
            # Calculates y location (in pixels) using interpolation (lerp)
            y = lerp(y_min, y_max, i_y/9.0)
            
            # Percentage of pie slice to show
            pct = lerp(top[i_x], btm[i_x], i_y/9.0)
        
            draw_pies(x, y, pct, up_start, up_stop, down_start, down_stop)
                
    if record:
        save_frame_timestamp('parc_pie', timestamp)
        
        
def draw_pies(x, y, pct, up_start, up_stop, down_start, down_stop):
    """
    Draws both pie slices, with the top pie as the lead and bottom pie as follower
    There is always a 90 degree (tau/4) gap between top and bottom slices
    """
    
    # d controls the amount of each slice that is shown
    d = pct * TAU/4
    fill(*c_blue)
    arc(x, y, x_rad, y_rad, up_start+d, up_stop-d, PIE)
    
    d = (1-pct) * TAU/4
    fill(*c_red)
    arc(x, y, x_rad, y_rad, down_start+d, down_stop-d, PIE)
        
def save_frame_timestamp(filename, timestamp='', output_dir='output'):
    '''Saves each frame with a structured filename to allow for tracking all output'''
    filename = filename.replace('\\', '')
    filename = filename.replace('/', '')
    output_filename = os.path.join(output_dir, '{}_{}_{}_####.png'.format(timestamp, filename, rand_seed))
    saveFrame(output_filename)
    print(output_filename)
