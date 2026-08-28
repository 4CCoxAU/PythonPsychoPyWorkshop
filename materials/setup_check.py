# Setup check for the PsychoPy workshop.
# Open this file in the PsychoPy Coder and press Run.
# If a window appears saying "Your setup works!", you are ready.

from psychopy import visual, core

win = visual.Window(size=(700, 350), color='black')

message = visual.TextStim(
    win,
    text='Your setup works!\n\nThis window closes itself in 4 seconds.',
    color='white',
    height=0.09)

message.draw()
win.flip()
core.wait(4)

win.close()
core.quit()
