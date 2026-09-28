from psychopy import visual, event, core, gui
import glob
import random


# --- dummy study information and consent ---
consent = gui.Dlg(
    title='Study information',
    labelButtonOK='Agree',
    labelButtonCancel='Decline'
)
consent.addText(
    'Workshop demonstration; not a real research study.\n'
    'Task: see a lion or burrow, then press an arrow key.\n'
    'Responses and times print in the Runner; no file is saved.\n'
    'Taking part is voluntary. Ask your instructor with questions.\n'
    'Choose OK to agree to take part, or Cancel to decline to withdraw participation.')
    
consent.show()

if not consent.OK:
    core.quit()

# --- setup ---
images = glob.glob('stimuli/stimulus*.jpg')
random.shuffle(images)

win = visual.Window(size=(1280, 720), fullscr=False,
                    color='black', checkTiming=False)

stopwatch = core.Clock()

# setup:
rts = []

# --- functions ---
def msg(text):
    message = visual.TextStim(win, text=text, height=0.06)
    message.draw()
    win.flip()
    event.waitKeys()

def show_stim(image):
    stim = visual.ImageStim(win, image=image)
    stim.draw()
    win.flip()

# --- experiment ---
msg('The Fleeing Rabbit\n\n'
    'You are the rabbit, and the lion is on the hunt!\n\n'
    'See a LION? Run the other way: press the OPPOSITE arrow.\n'
    'See a BURROW? Dive in: press the arrow on ITS side.\n\n'
    'Be quick, and be right. Press any key to start.')

for image in images:
    # show the stimulus and start the clock at its onset
    show_stim(image)
    stopwatch.reset()

    # collect the response and read the clock
    keys = event.waitKeys(keyList=['left', 'right'])
    rt = stopwatch.getTime()
    # in the loop, after reading the clock:
    rts.append(rt)
    key = keys[0]

    # derive the correct answer from the filename
    if image.endswith('_L.jpg'):
        correct_key = 'left'
    else:
        correct_key = 'right'

    # feedback for 2 seconds
    if key == correct_key:
        show_stim('stimuli/success.jpg')
    else:
        show_stim('stimuli/failure.jpg')
    core.wait(2)

    # report the trial
    print(f'{image}: {key} pressed, correct was {correct_key}, rt {rt:.2f} s')

msg('That was it. Thank you!')# goodbye:
msg(f'Average reaction time: {sum(rts) / len(rts):.2f} seconds. Thank you!')
win.close()

core.quit()