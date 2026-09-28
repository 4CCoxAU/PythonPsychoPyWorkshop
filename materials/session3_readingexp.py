from psychopy import visual, core, gui
from psychopy.hardware import keyboard
import os, csv, random
from datetime import datetime

# Dialog
info = {"Participant ID": ""}
if not gui.DlgFromDict(info, title="Self-Paced Reading").OK:
    core.quit()

pid = "P000"
if info["Participant ID"]:
    pid = info["Participant ID"]

# Window and Textbox
win = visual.Window(size=[1000, 700], units="pix", color="black", fullscr=False)
txt = visual.TextBox2(win, text="+", font="Arial", letterHeight=48, color="white", size=(900, 200), alignment="center")
kb = keyboard.Keyboard()


def show(t):
    txt.text = t
    txt.draw()
    win.flip()

def wait_space_rt():
    kb.clearEvents()
    kb.clock.reset()
    while True:
        for k in kb.getKeys(keyList=["space", "escape"], waitRelease=False):
            if k.name == "escape":
                win.close()
                core.quit()
            if k.name == "space":
                return round(k.rt * 1000, 3)
        core.wait(0.001)

# Content
story = "On a clear Saturday morning, Maya set out for a slow jog along the riverside path. The air smelled faintly of wet grass, and bicycles drifted past like quiet birds. She counted her breaths, matching them to the soft rhythm of her footsteps. At the old footbridge she paused, watching sunlight scatter across the water. A family unpacked breakfast nearby; a thermos hissed, and someone laughed. Maya stretched, then started again along the path that curved through willows. Past the square she slowed, noticing the scent of roasted coffee drifting from a tiny kiosk. Children were chalking bright shapes on the paving stones, and a busker tuned a battered guitar. Maya stopped to tie a loose shoelace and glanced at the notes for the concert pinned to a lamp post. She thought about her own violin, stored away in a dusty case under her bed. The sun was climbing higher, glinting off the windows of nearby apartments. She began jogging again, feeling the steady beat of her pulse and the easy warmth of the morning settle into her muscles."

ctrl = story.split()
target = "grass,"
repl = "toothpaste"
exp_tokens = ctrl.copy()


idx = 3
# We loop through the exp_tokens which is a list of words
# the variable idx is equal to the index of the target word in the story.
if target in exp_tokens:
    idx = exp_tokens.index(target)
    
exp_tokens[idx] = repl
conds = [("control", ctrl), ("experimental", exp_tokens)]
random.shuffle(conds)

# Run
rows = []
for cname, tokens in conds:
    show("+") 
    core.wait(0.6)
    for i, tok in enumerate(tokens):
        show(tok)
        rt = wait_space_rt()
        rows.append({
            "participant": pid,
            "condition": cname,
            "word_index": i,
            "word": tok,
            "is_surprising": int(cname == "experimental" and i == idx),
            "rt_ms": rt
        })

# Save and exit
ts = datetime.now().strftime("%Y%m%d-%H%M%S")
os.makedirs("data", exist_ok=True)
out = f"data/SPR_min_{pid}_{ts}.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["participant","condition","word_index","word","is_surprising","rt_ms"])
    w.writeheader(); w.writerows(rows)

show(f"Done.\nSaved: {out}\nPress any key to exit.")
kb.waitKeys()
win.close()
core.quit()