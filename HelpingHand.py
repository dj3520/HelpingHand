import tkinter as tk
import tkinter.ttk as ttk

rootwin = tk.Tk()
rootwin.title("HelpingHand - for Phasmophobia")

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

signs = tk.LabelFrame(rootwin, text="Evidence")
signs.grid(row=0)
type_list = tk.LabelFrame(rootwin, text="Possibilities")
label_dictionary = {}
for k in possibilities.keys():
  label_dictionary[k] = tk.Label(type_list, text=k)
  label_dictionary[k].grid(row=len(label_dictionary) - 1)
type_list.grid(row=1)


def vartrace(name, indx, op):
  fullist = set(possibilities.keys())
  compstr = ""
  # Make a string representing the checkbox values as 0s and 1s
  for v in chkvars:
    compstr += str(v.get())
  # Go through our checkbox values, and remove anything from the possibilities if we've checked that box but that ghost doesn't want that sign.
  for i in range(len(compstr)):
    if compstr[i] == "0": continue
    complist = fullist.copy()
    for g in complist:
      if not compstr[i] == possibilities[g][i]:
        fullist.remove(g)
  # Now update the display list
  for k, v in label_dictionary.items():
    if k in fullist: v.grid()
    else: v.grid_forget()

chkvars = []
for k, v in display_texts.items():
  newvar = tk.IntVar()
  newvar.trace("w", vartrace)
  chk = tk.Checkbutton(signs, text=k, justify=tk.LEFT, variable=newvar)
  chk.grid(row=len(chkvars), column=0)
  txt = tk.Label(signs, text=v)
  txt.grid(row=len(chkvars), column=1)
  chkvars.append(newvar)

# Changing amounts of possibilities causes window size changes. Not the nicest things.
rootwin.resizable(tk.FALSE, tk.FALSE)
rootwin.update()

rootwin.grid_propagate(False)

rootwin.mainloop()