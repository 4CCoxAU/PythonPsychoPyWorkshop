stopwatch = core.Clock()     # create, once, in the setup
stopwatch.reset()            # zero it: timing starts NOW
rt = stopwatch.getTime()     # read it: seconds since the reset

from psychopy import visual, event, core
import glob
import random

images = glob.glob('stimuli/stimulus*.jpg')
random.shuffle(images)
print(images)

win = visual.Window(size=(1280, 720), fullscr=False,
                    color='black', checkTiming=False)

stopwatch = core.Clock()

# the rabbit must surprise you: shuffled waiting times, first one wins
waits = [1, 1.5, 2, 2.5, 3]
random.shuffle(waits)

                    
welcome = visual.TextStim(win, color='white', height=0.06,
    text='The Fleeing Rabbit\n\n'
         'You are the rabbit, and the lion is on the hunt!\n\n'
         'See a LION? Run the other way: press the OPPOSITE arrow.\n'
         'See a BURROW? Dive in: press the arrow on ITS side.\n\n'
         'Be quick and be right. Press any key to start.')
         
welcome.draw()
win.flip()
event.waitKeys()
                    
def show_stim(image):
    stim = visual.ImageStim(win, image=image)
    stim.draw()
    win.flip()

for image in images:
    
    show_stim(image)
    event.waitKeys()
    
    keys = event.waitKeys(keyList=['left', 'right'])
    key = keys[0]
    
    if image.endswith('_L.jpg'):
        correct_key = 'left'
    else:
        correct_key = 'right'
                    
    if key == correct_key:
        show_stim('stimuli/success.jpg')
    else:show_stim('stimuli/failure.jpg')
    
    core.wait(2)

# after the loop:
msg('That was it. Thank you! Press any key to close.')

win.close()
core.quit()