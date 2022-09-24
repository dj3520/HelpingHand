import tkinter as tk
import tkinter.ttk as ttk

from tkinter import filedialog
import configparser, os, shutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog import events as watchevents

rootwin = tk.Tk()
rootwin.title("HelpingHand - for Phasmophobia * by DJ3520 [V:1.1.0 ~ Obtusely Overdue Overhaul]")

tabs = ttk.Notebook(rootwin)
tabs.pack()
diagnosis = tk.Frame(tabs)
tabs.add(diagnosis, text="Diagnosis")

display_texts = {
  "EMF Level 5": "All lights on the EMP will illuminate. 5th and final light is red.",
  "Spirit Box": "Spirit Box responds to your questions. What is said will show on the display.",
  "Fingerprints": "Or handprints. BUT NOT FOOTPRINTS. Shine the UV flashlight on objects the ghost has touched, such as doors or light switches.",
  "Ghost Orb": "With night vision enabled on a camera, saw what might be mistaken as a spec of dust or a fly. (Tip: Flies are extinct in-game)",
  "Ghost Writing": "The blank book you brought with you now has pretty drawings you don't remember anyone putting there.",
  "Freezing Temperatures": "Below 0C or 32F degrees. Cold enough to see your breath. Chilling!"
}

# Bitmap: EMF5, Box, Prints, Orbs, Writing, Temps

possibilities = {
  "Spirit": ["011010", "Smudge sticks are more effective against these. Patience is also required to identify a spirit."],
  "Shade": ["100110", "Shy, hunt lone players. Sticking together reduces chances of death but also reduces activity."],
  "Poltergeist": ["011100", 'Moves objects, even multiple at once. Considered "noisy", useless in a room with no items.'],
  "Jinn": ["110100", "Territorial, only attack when threatened. High speed travel unless power is cut."],
  "Mare": ["010101", "Powerful in the dark, weak in the light. Will want to turn off lights, or even power."],
  "Phantom": ["100101", "Slow. When viewed directly will take large amount of sanity. Taking its picture will make it disappear."],
  "Wraith": ["011001", "Relentless hunter. Can fly and go through walls. Salt will temporarily lower it's aggression before making it worse afterwords."],
  "Banshee": ["101001", "Focuses on one player at a time. Crucifixes have a larger effective range."],
  "Revenant": ["101010", "Faster while hunting, slower while players are hiding."],
  "Yurei": ["000111", "Strong effect on sanity. Using smudge sticks might trap it in it's current room."],
  "Oni": ["110010", "More active while players are near. Able to throw objects with great speed."],
  "Demon": ["010011", "Highly aggressive. Crucifix is recommended. No penalty to sanity if it cooperates with you using the Ouija board."],
}

signs = tk.LabelFrame(diagnosis, text="Evidence")
signs.grid(row=0)
type_list = tk.LabelFrame(diagnosis, text="Possibilities")
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

b = tk.Button(signs, text="Clear", command=reset_evidence)
b.grid(sticky=tk.W)

configf = configparser.ConfigParser(defaults={"s_directory": "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Phasmophobia", "d_Directory": os.path.expanduser('~') + "\\Pictures", "copy_pictures": "0"})
if os.path.isfile("settings.ini"):
  configf.read("settings.ini")
else:
  with open("settings.ini", "w") as f:
    configf.write(f)
config = {}
for i in configf.items(section="DEFAULT"):
  config[i[0]] = i[1]
  print("Config: {}".format(i))

pictures = tk.Frame(tabs)
tabs.add(pictures, text="Pictures")

def choose_which(which):
  if which == "s":
    ask = "Please select game folder."
    init = "s_directory"
  else:
    ask = "Please select save folder."
    init = "d_directory"
  folder = filedialog.askdirectory(title=ask, initialdir=config[init], mustexist=True)
  if not os.path.isdir(folder):
    print("Not folder: '{}'".format(folder))
  config[init] = folder
  save_config(config)

# Define here instead of lower so invalid folder messages show.
disp_pic = tk.Label(pictures, text="Picture copying wasn't enabled.") # Intentionally not "is" to differentiate with startup text.

# Define here so save_config treats as global
folders_ok = 0

def save_config(config):
  global folders_ok
  configf.update({"DEFAULT": config})
  with open("settings.ini", "w") as f:
    configf.write(f)
  for i in configf.items(section="DEFAULT"):
    print("New config: {}".format(i))

  test = 3
  if os.path.isdir(config["s_directory"]): test -= 2
  if os.path.isdir(config["d_directory"]): test -= 1
  if config["d_directory"] == config["s_directory"]: test = 4
  print("Value save test result: {}".format(test))

  if test == 4:
    disp_pic.config(text="Game and destination folders are the same. This could cause a pretty nasty crash.")
    folders_ok = 0
  elif test == 3:
    disp_pic.config(text="Game and destination folders invalid.")
    folders_ok = 0
  elif test == 2:
    disp_pic.config(text="Game folder invalid.")
    folders_ok = 0
  elif test == 1:
    disp_pic.config(text="Destination folder invalid.")
    folders_ok = 0
  else:
    folders_ok = 1
    disp_pic.config(text="New configuration saved.")

def choose_s():
  choose_which("s")

def choose_d():
  choose_which("d")

filewatch = None

def set_pictures_active():
  global filewatch
  config["copy_pictures"] = pic_checkbox.get()
  save_config(config)

  if str(config["copy_pictures"]) == "1" and folders_ok:
    if filewatch is None:
      filewatch = FileEventHandler(config["s_directory"])
    print("Watching for new PNGs now enabled. Folder: {}".format(config["s_directory"]))
    disp_pic.config(text="Watching the game folder for pictures...") # Intentionally not "new" pictures to differentiate with startup text.
  elif folders_ok:
    disp_pic.config(text="Picture copying disabled.")
    if not filewatch is None:
      filewatch.stop()

tk.Label(pictures, text="Pictures taken by the in-game photo camera can be copied to a folder of your choice.\nThis program must be open for this to occur.").pack()
pic_checkbox = tk.IntVar()
pic_checkbox.set(int(config["copy_pictures"]))
tk.Checkbutton(pictures, text="Enable this!", command=set_pictures_active, variable=pic_checkbox).pack()
tk.Button(pictures, text="Select game folder.", command=choose_s).pack()
tk.Button(pictures, text="Select destination folder.", command=choose_d).pack()
disp_pic.pack()

# Changing amounts of possibilities causes window size changes. Not the nicest things.
rootwin.resizable(tk.FALSE, tk.FALSE)
rootwin.update()

type_list.grid_propagate(False)
rootwin.grid_propagate(False)

class FileEventHandler():
  def __init__(self, path):
    self.path = path
    self.documents = dict()

    self.event_handler = watchevents.PatternMatchingEventHandler(patterns=["*.png"], ignore_directories=True)
    self.observer = Observer()
    self.event_handler.on_modified = self.on_modified
    self.last_file = ""

    self.observer.schedule(self.event_handler, self.path, recursive=False)
    self.observer.start()

  def on_modified(self, event):
    # Seems to get fired twice. Luckily the game always changes filename for us. So make sure that happens.
    if event.src_path == self.last_file: return
    self.last_file = event.src_path
    if not folders_ok:
      print("Missed opportunity for file copy. Check folders are valid.")
      return
    dispname = datetime.now().isoformat("_","milliseconds").replace(":","-") + ".png"
    outfile = config["d_directory"] + "\\" + dispname
    print("New picture detected: {} -> {}".format(event.src_path, outfile))
    try:
      shutil.copy2(event.src_path, outfile)
    except Exception as e:
      disp_pic.config(text="Error: {}".format(e))
      print("Picture copy error: {}".format(e))
      return
    disp_pic.config(text="Copied last picture to {}".format(dispname))

  def stop(self):
    self.observer.stop()
    self.observer.join()

filewatch = None
if str(config["copy_pictures"]) == "1":
  save_config(config)
  if folders_ok == 1:
    filewatch = FileEventHandler(config["s_directory"])
    print("Watching for new PNGs enabled in startup. Folder: {}".format(config["s_directory"]))
    disp_pic.config(text="Watching the game folder for new pictures...")
rootwin.mainloop()