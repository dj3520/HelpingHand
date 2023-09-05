import tkinter as tk
import tkinter.ttk as ttk

from tkinter import filedialog
import configparser, os, shutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog import events as watchevents

rootwin = tk.Tk()
rootwin.title("HelpingHand - for Phasmophobia * by DJ3520 & Chaosangel767 [V:1.1.0 ~ Obtusely Overdue Overhaul]")

tabs = ttk.Notebook(rootwin)
tabs.pack()
diagnosis = tk.Frame(tabs)
tabs.add(diagnosis, text="Diagnosis")

display_texts = {
  "EMF Level 5":            "Ghost maxes out the EMF device reading.",
  "Ultraviolet":            "Includes fingerprints and footprints. Does not last long. Shine UV light on objects the ghost has touched, such as doors, windows, light switches, etc.",
  "Ghost Writing":          "The blank book you brought with you now has pretty drawings you don't remember anyone putting there. Ghost can throw the book if not evidence.",
  "Freezing Temperatures":  "Below 0C or 32F degrees. Cold breath is not reliable as it starts before the freezing temps begin. Weather plays an effect on resting temperature of map.",
  "DOTS":                   "A laser grid that may reveal a manifesting human shape. Can be seen on-camera.",
  "Ghost Orb":              "With night vision enabled on a camera, saw what might be mistaken as a spec of dust or a fly. (Tip: Flies are extinct in-game, and snow only goes down)",
  "Spirit Box":             "Spirit Box responds to your questions. Activity tends to increase while using the spirit box (most ghosts don't like your voice)."
}

# Bitmap: EMF5, Ultraviolet, Writing, Temps, DOTS, Orbs, Spirit Box
# 1 = required TRUE, 0 = required FALSE

possibilities = {
  "Spirit":      ["1010001", "If smudge stick used while not hunting, cannot hunt until 180 seconds pass (3 minutes)"],
  "Poltergeist": ["0110001", "Can throw more than one object at a time. Will throw anything not nailed down in a hunt (causes a mini tornado)."],
  "Mare":        ["0010011", "Never turns lights on. Hunts at 60% sanity with lights off and 40% sanity if lights in the ghost room are on. Can roam into a dark room to start hunt."],
  "Demon":       ["0111000", "Hunts early and more often. Can hunt even at 100% sanity. Crucifix range increased."],
  "Yokai":       ["0000111", "Can hunt with more sanity when players speak nearby. Has a smaller range to sense players during a hunt than other ghosts."],
  "Myling":      ["1110000", "Can only hear footsteps within range of tools bugging out. Usually footsteps can be heard from farther away."],
  "Raiju":       ["1000110", "During hunting, active electronics boost speed (including when held.)"],
  "Moroi":       ["0011001", "Can curse you through spirit box which will constantly drain sanity when inside house."],
  #
  "Wraith":      ["1000101", "Never steps in salt, even during a hunt."],
  "Banshee":     ["0100110", "More likely to sing or hum during ghost events. Will arely wail through microphone. Picks one player as a target. Can roam to player and do events."],
  "Revenant":    ["0011010", "During a hunt, slowly wanders unless chasing. Fast when chasing."],
  "Yueri":       ["0001110", "Cannot leave room for 90 seconds after successfully using smudge sticks. Only ghost that can move the entrance door when not hunting."],
  "Hantu":       ["0101010", "During hunt, becomes faster in colder rooms and slower in warmer rooms. Really wants the breaker to be off."],
  "Onryo":       ["0001011", "A lit candle acts as a crucifix. Chance to hunt after blowing out a candle. Will roam to a room without a candle to hunt."],
  "Obake":       ["1100010", "Can change ghost's appearence briefly during a hunt. Fingerprints are more rare, last a shorter time, but can be unique (Count the fingers.)"],
  "Deogen":      ["0010101", "Always knows your location (hiding won't save you) but slow enough to outrun when near you. Don't stay still during a hunt!"],
  #
  "Phantom":     ["0100101", "Disappears if photo taken during ghost event (event still continues.) Sanity takes a hit if picture is not taken."],
  "Jinn":        ["1101000", "Ability is based on breaker being on. Never turns off power. Will speed up in a hunt until in range of the player."],
  "Shade":       ["1011000", "Only able to do a small set of things when a player is in the same room. Makes events more rare. Hunts occur below 30% sanity (except cursed hunts)."],
  "Oni":         ["1001100", "Throws items with more force (not faster just stronger.) Never manifests as ball of smoke."],
  "Goryo":       ["1100100", "Will not do DOTS if a player is in the same room. Best to set up a camera."],
  "Twins":       ["1001001", "Can summon a decoy to another room. Can begin hunt from either location. Hunts at two different speeds depending on whether real ghost or decoy."],
  "Mimic":       ["0101011", "Spawns orbs (where it is, may not be the ghost room) but doesn't count as evidence! Imitates other ghosts (but can switch to others, including itself!)"],
  "Thaye":       ["0010110", "Starts strong and fast, but gets weaker and slower the longer players are in the same room."],
}

signs = tk.LabelFrame(diagnosis, text="Evidence")
signs.grid(row=0)
type_list = tk.LabelFrame(diagnosis, text="Possibilities")
label_dictionary = {}

# Logic and things starts at this point.

# Make GUI elements based on possibilities.
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

# Make GUI elements based on evidences
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

# Pictures tab section

# Load settings
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

tk.Label(pictures, text="Pictures taken by the in-game photo camera can be saved to a folder of your choice.\nThis program must be open for this to occur.").pack()
pic_checkbox = tk.IntVar()
pic_checkbox.set(int(config["copy_pictures"]))
tk.Checkbutton(pictures, text="Enable this!", command=set_pictures_active, variable=pic_checkbox).pack()
tk.Button(pictures, text="Select game folder.", command=choose_s).pack()
tk.Button(pictures, text="Select destination folder.", command=choose_d).pack()
disp_pic.pack()

# Changing amounts of possibilities causes window size changes. Not the nicest things.
# So after we've done all the setup for the GUI, lock down the size.
rootwin.resizable(tk.FALSE, tk.FALSE)
# Ok we're all done with setup. Make it appear.
rootwin.update()

# Don't resize things based on their content. Leave them the same size.
type_list.grid_propagate(False)
rootwin.grid_propagate(False)

# Actual work with pictures happens here.
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
    outfile = config["d_directory"] + "/" + dispname
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
  save_config(config) # Sets folders_ok
  if folders_ok == 1:
    filewatch = FileEventHandler(config["s_directory"])
    print("Watching for new PNGs enabled in startup. Folder: {}".format(config["s_directory"]))
    disp_pic.config(text="Watching the game folder for new pictures...")

# Let the GUI take control.
rootwin.mainloop()
