from psychopy import visual, event, core, gui
import glob
import random


win = visual.Window(size=(1280, 720), fullscr=False,
                    color='black', checkTiming=False)

def make_button(label, pos):
    button = visual.Rect(
        win=win, width=0.55, height=0.12, pos=pos,
        fillColor='darkgreen', lineColor='white', units='height'
    )
    button_label = visual.TextStim(
        win=win, text=label, color='white', height=0.03,
        pos=pos, units='height'
    )
    return label, button, button_label


def wait_for_choice(question, buttons, body=''):
    heading = visual.TextStim(
        win=win, text=question, color='white', height=0.04,
        pos=(0, 0.40), units='height'
    )
    information = visual.TextStim(
        win=win, text=body, color='white', height=0.027,
        wrapWidth=1.6, pos=(0, 0.03), alignText='left', units='height'
    )
    mouse = event.Mouse(win=win)

    # Wait for any earlier click to be released before showing the screen.
    while any(mouse.getPressed()):
        core.wait(0.01)

    while True:
        heading.draw()
        if body:
            information.draw()
        for label, button, button_label in buttons:
            button.draw()
            button_label.draw()
        win.flip()

        if event.getKeys(keyList=['escape']):
            win.close()
            core.quit()

        if mouse.getPressed()[0]:
            for label, button, button_label in buttons:
                if button.contains(mouse.getPos()):
                    while mouse.getPressed()[0]:
                        core.wait(0.01)
                    return label

        core.wait(0.01)


study_information = (
    'Purpose: [Describe the purpose of the study.]\n'
    'What you will do: [Describe the task and what participants will be asked to do.]\n'
    'Time: [Give the expected duration.]\n'
    'Risks and benefits: [Describe any relevant risks or benefits.]\n'
    'Data: [Explain what is recorded, how it is used, and how it is stored.]\n'
    'Participation: Taking part is voluntary. [Explain how and when participants '
    'can withdraw, including any limits on removing data.]\n'
    'Questions: [Provide the appropriate contact information.]'
)

read_information = make_button('Continue to consent', (0, -0.36))
wait_for_choice(
    'Study information — The Fleeing Rabbit',
    [read_information],
    study_information
)

agree_button = make_button('I agree to take part', (-0.32, -0.36))
decline_button = make_button('I do not agree', (0.32, -0.36))
consent = wait_for_choice(
    'Do you consent to take part?',
    [agree_button, decline_button]
)

if consent != 'I agree to take part':
    win.close()
    core.quit()
