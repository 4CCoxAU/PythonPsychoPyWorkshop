from psychopy import gui


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
    'Choose OK if you provide informed consent to participant, or Cancel to decline participation in the study.')
    
consent.show()
