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
  "Spirit": 0b011010,
  "Shade": 0b100110,
  "Poltergeist": 0b011100,
  "Jinn": 0b110100,
  "Mare": 0b010101,
  "Phantom": 0b100101,
  "Wraith": 0b011001,
  "Banshee": 0b101001,
  "Revenant": 0b101010,
  "Yurei": 0b000111,
  "Oni": 0b110010,
  "Demon": 0b010011,
}

signs = tk.LabelFrame(rootwin, text="Evidence")
chkvars = []
for k, v in display_texts.items():
  newvar = tk.IntVar()
  chk = tk.Checkbutton(signs, text=k, variable=newvar)
  chk.grid(row=len(chkvars), column=0)
  txt = tk.Label(signs, text=v)
  txt.grid(row=len(chkvars), column=1)
  chkvars.append(newvar)

