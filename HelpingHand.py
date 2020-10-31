import tkinter as tk
import tkinter.ttk as ttk

rootwin = tk.Tk()

display_texts = {
  "EMF Level 5": "All lights on the EMP will illuminate.",
  "Spirit Box": "Spirit Box responds to your questions.",
  "Fingerprints": "Find on objects the ghost has touched using the UV light. Handprints and footprints also count.",
  "Ghost Orb": "With night vision enabled on a camera, saw what might be mistaken as a fly. (Flies are extinct in-game)",
  "Ghost Writing": "The blank book you brought in now has pretty doodles.",
  "Freezing Temperatures": "Below 0 degrees Celsius or 32 degrees Fahrenheit. Cold enough to see your breath."
}

# Bitmap: EMF5, Box, Prints, Orbs, Writing, Temps

possibilities = {
  "Spirit": "011010",
  "Shade": "100110",
  "Poltergeist": "011100",
  "Jinn": "110100",
  "Mare": "010101",
  "Phantom": "100101",
  "Wraith": "011001",
  "Banshee": "101001",
  "Revenant": "101010",
  "Yurei": "000111",
  "Oni": "110010",
  "Demon": "010011",
}

def vartrace(name, indx, op):
  fullist = set(possibilities.keys())
  compstr = ""
  # Make a string representing the checkbox values as 0s and 1s
  for v in chkvars:
    compstr + = str(v.get())
  # Go through our checkbox values, and remove anything from the possibilities if we've checked that box but that ghost doesn't want that sign.
  for i in range(len(compstr)):
    if compstr[i] == "0": continue
    complist = fullist
    for g in complist:
      if not compstr[i] == possibilities[g][i]:
        fullist.remove(g)
  # Now update the display list


signs = tk.LabelFrame(rootwin, text="Evidence")
chkvars = []
for k, v in display_texts.items():
  newvar = tk.IntVar()
  newvar.trace("w", vartrace)
  chk = tk.Checkbutton(signs, text=k, variable=newvar)
  chk.grid(row=len(chkvars), column=0)
  txt = tk.Label(signs, text=v)
  txt.grid(row=len(chkvars), column=1)
  chkvars.append(newvar)

