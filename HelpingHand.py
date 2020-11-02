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
  "Spirit": ["011010", "Can be delayed with smudge sticks."],
  "Shade": ["100110", "Shy, hunt lone players. Sticking together prevents death but also activity."],
  "Poltergeist": ["011100", 'Moves objects, considered "noisy", useless in a room with no items.'],
  "Jinn": ["110100", "Territorial, only attack when threatened. High speed travel unless power is cut."],
  "Mare": ["010101", "Powerful in the dark. Will want to turn off lights, or even power."],
  "Phantom": ["100101", "Slow. When viewed directly will take large amount of sanity. Taking its picture will make it disappear."],
  "Wraith": ["011001", "Relentless hunter. Can fly and go through walls. Salt is toxic and will prevent attacks."],
  "Banshee": ["101001", "Focuses on one player at a time. Crucifixes have a larger effective range."],
  "Revenant": ["101010", "Faster while hunting, slower while players are hiding."],
  "Yurei": ["000111", "Strong effect on sanity. Weak to smudge sticks."],
  "Oni": ["110010", "Moves quicker while players are near. Means more activity but also more dangerous."],
  "Demon": ["010011", "Highly aggressive. Crucifix is recommended. No penalty to sanity when using Ouiji board and it cooperates."],
}

signs = tk.LabelFrame(rootwin, text="Evidence")
signs.grid(row=0)
type_list = tk.LabelFrame(rootwin, text="Possibilities")
label_dictionary = {}
for k, v in possibilities.items():
  label_dictionary[k] = [None, None]
  label_dictionary[k][0] = tk.Label(type_list, text=k)
  label_dictionary[k][0].grid(row=len(label_dictionary) - 1, column=0, sticky=tk.W)
  label_dictionary[k][1] = tk.Label(type_list, text=v[1])
  label_dictionary[k][1].grid(row=len(label_dictionary) - 1, column=1, sticky=tk.W, padx=20)
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
      if not compstr[i] == possibilities[g][0][i]: # compares place I of string with matching key in possibilities, first element of list, place I in string.
        fullist.remove(g)
  # Now update the display list
  row = 0
  for k, v in label_dictionary.items():
    if k in fullist:
      # Text needs pad, so can't do for loop like lower down.
      v[0].grid(row=row, column=0, sticky=tk.W)
      v[1].grid(row=row, column=1, sticky=tk.W, padx=20)
    else:
      for i in v:
        i.grid_forget()
    row += 1

chkvars = []
for k, v in display_texts.items():
  newvar = tk.IntVar()
  newvar.trace("w", vartrace)
  chk = tk.Checkbutton(signs, text=k, justify=tk.LEFT, variable=newvar)
  chk.grid(row=len(chkvars), column=0, sticky=tk.W)
  txt = tk.Label(signs, text=v)
  txt.grid(row=len(chkvars), column=1, sticky=tk.E)
  chkvars.append(newvar)

def reset_evidence():
  for i in chkvars:
    i.set(0)

b = tk.Button(signs, text="Reset", command=reset_evidence)
b.grid(sticky=tk.W)

# Changing amounts of possibilities causes window size changes. Not the nicest things.
rootwin.resizable(tk.FALSE, tk.FALSE)
rootwin.update()

type_list.grid_propagate(False)
rootwin.grid_propagate(False)

rootwin.mainloop()