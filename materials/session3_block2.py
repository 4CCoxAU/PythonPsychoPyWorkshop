from psychopy import gui, core

import random


box = gui.Dlg(title='The Fleeing Rabbit')
box.addField('Native language')
box.addField('Handedness', choices=['Right-handed', 'Left-handed'])
box.show()

participant_id = f'P{random.randint(10000, 99999)}'


if box.OK:
    print(box.data)
else:
    core.quit()