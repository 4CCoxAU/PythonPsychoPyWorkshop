from psychopy import visual, event, core
import random

win = visual.Window(size=(1280, 720), fullscr=False,
                    color='black', checkTiming=False)

stopwatch = core.Clock()

# surprise number one: when the rabbit appears
waits = [1, 1.5, 2, 2.5, 3]
random.shuffle(waits)

win.flip()       # black screen: get ready...
core.wait(waits[0])

# surprise number two: where the rabbit appears
positions = [(-0.5, 0), (0.5, 0)]
random.shuffle(positions)

pic = visual.ImageStim(win, image='rabbit.jpg', size=0.5)
pic.pos = positions[0]
pic.draw()
win.flip()       # the rabbit appears: onset
stopwatch.reset()

keys = event.waitKeys(keyList=['left', 'right'])
rt = stopwatch.getTime()
key = keys[0]

# was the press on the rabbit's side?
if pic.pos[0] < 0:                  # rabbit was on the left
    correct_key = 'left'
else:
    correct_key = 'right'

print(f'Choice reaction: {rt:.3f} s, pressed {key}, correct was {correct_key}')

win.close()
core.quit()