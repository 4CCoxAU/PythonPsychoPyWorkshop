from psychopy import visual, event, core, gui
import os
import random
import pandas as pd

# --- dummy study information and consent ---
consent = gui.Dlg(
    title='Study information',
    labelButtonOK='Agree',
    labelButtonCancel='Decline'
)
consent.addText('Workshop demonstration; not a real research study.')
consent.addText('You will read one version of a short story, one word at a time, and press Space.')
consent.addText('Your reading times are saved in a CSV file in the data folder.')
consent.addText('Taking part is voluntary. Choose Agree to continue, or Decline to quit.')
consent.show()

if not consent.OK:
    core.quit()

# --- random participant ID ---
data_folder = 'data'
os.makedirs(data_folder, exist_ok=True)

# Randomly generate participant ID. 
participant_id = f'P{random.randint(10000, 99999)}'

#---collect basic demographic info---
box = gui.Dlg(title='Self-paced reading experiment')
box.addField('Native language')
box.addField('Age')
box.show()

if box.OK:
    language = box.data['Native language']
    age = box.data['Age']
else:
    core.quit()

# --- window and text ---
win = visual.Window(
    size=(1000, 700), units='pix', color='black', fullscr=False
)
text = visual.TextStim(win, text='+', color='white', height=48, units='pix')
clock = core.Clock()

def show(message):
    text.text = message
    text.draw()
    win.flip()


# --- story and conditions ---
story = """On a clear Saturday morning, Maya set out for a slow jog along the riverside path.
The air smelled faintly of wet grass, and bicycles drifted past like quiet birds.
She counted her breaths, matching them to the soft rhythm of her footsteps.
At the old footbridge she paused, watching sunlight scatter across the water.
A family unpacked breakfast nearby; a thermos hissed, and someone laughed.
Maya stretched, then started again along the path that curved through willows.
Past the square she slowed, noticing the scent of roasted coffee drifting from a tiny kiosk.
Children were chalking bright shapes on the paving stones, and a busker tuned a battered guitar.
Maya stopped to tie a loose shoelace and glanced at the notes for the concert pinned to a lamp post.
She thought about her own violin, stored away in a dusty case under her bed.
The sun was climbing higher, glinting off the windows of nearby apartments.
She began jogging again, feeling the steady beat of her pulse and the easy warmth of the morning settle into her muscles."""

# Make two word lists. Change one word in the experimental version.
control_words = story.split()
experimental_words = control_words.copy()
target_word = 'grass,'
replacement_word = 'toothpaste,'

target_index = control_words.index(target_word)
experimental_words[target_index] = replacement_word

# --- run the reading task ---
show('You will read one story, one word at a time.\n'
    'Press Space for the next word.\n'
    'Press Escape to stop.\n\n'
    'Press any key to begin.')
event.waitKeys()

results = []

# Randomly assign this participant to one of the two conditions.
conditions = ['control', 'experimental']
random.shuffle(conditions)
condition = conditions[0]

if condition == 'control':
    words = control_words
else:
    words = experimental_words

show('+')
core.wait(0.6)

for word_index in range(len(words)):
    word = words[word_index]
    event.clearEvents()
    text.text = word
    text.draw()
    win.callOnFlip(clock.reset)
    win.flip()
    keys = event.waitKeys(
        keyList=['space', 'escape'],
        timeStamped=clock
    )

    key, reaction_time = keys[0]
    if key == 'escape':
        win.close()
        core.quit()

    results.append({
        'participant': participant_id,
        'condition': condition,
        'word_index': word_index,
        'word': word,
        'is_surprising': int(
            condition == 'experimental' and word_index == target_index
        ),
        'rt_ms': reaction_time * 1000
    })

# --- save one row per word to a CSV file ---
output_file = f'{data_folder}/{participant_id}.csv'

data = pd.DataFrame(results)
data.to_csv(output_file, index=False)

show(f'Done!\nYour data were saved to:\n{output_file}\n\nPress any key to close.')
event.waitKeys()
win.close()
core.quit()