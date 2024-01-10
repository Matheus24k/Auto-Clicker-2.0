# Import modules
import tkinter as tk
import tkinter.ttk as ttk
import math
from pynput import keyboard
from pynput.mouse import Button, Controller
from threading import Thread
import time


# Defining functions
def detect_key(key):
    try:
        if key == keyboard.Key.f8:
            button_command()
    finally:
        pass


def filter_int(string):
    return "".join(s for s in string if s.isdigit())


def start_clicking(rate, mb):
    mouse = Controller()

    def click():
        while button.cget("text") == "Stop":
            time.sleep(rate / 1000)
            if mb == "left":
                mouse.click(Button.left)
            if mb == "right":
                mouse.click(Button.right)

    click()


# Create and configure window
root = tk.Tk()
root.title("Auto Clicker")
icon = tk.PhotoImage(file="assets/images/icon.png")
root.iconphoto(True, icon)
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
width = 233
height = 159
root.geometry(
    f"{width}x{height}+{int((math.ceil(w / 2)) - math.ceil(width / 2))}+{int((math.ceil(h / 2) - math.ceil(height / 2))
                                                                             )}")
root.resizable(False, False)

# Setting variables
font = ("Segoe UI", 10)
radiovar = tk.StringVar()
globalpadx = 5
globalpady = 5
startstop = 0
hovering = 0

# Setting grid rows and columns
root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=0)
root.rowconfigure(3, weight=0)
root.rowconfigure(4, weight=1)

root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)

# Setting objects
label_1 = ttk.Label(root, text="Select mouse button:", font=font)
label_2 = ttk.Label(root, text="Select interval: (ms)", font=font)
label_3 = ttk.Label(root, text="Press F8 to start / stop", font=font)
radio_left = ttk.Radiobutton(root, text="Left", variable=radiovar, value="left")
radio_right = ttk.Radiobutton(root, text="Right", variable=radiovar, value="right")


def button_command():
    global startstop
    startstop = startstop + 1
    if startstop % 2 == 0:
        button.configure(text="Start")
        startstop = 0
    else:
        button.configure(text="Stop")

    interval = entry.get()
    interval = filter_int(interval)
    if interval != "":
        entry.delete(0, "end")
        entry.insert(0, str(interval))
    else:
        entry.delete(0, "end")
        entry.insert(0, "1")
    try:
        if int(interval) > 60000:
            entry.delete(0, "end")
            entry.insert(0, "60000")
        if int(interval) < 1:
            entry.delete(0, "end")
            entry.insert(0, "1")
    except ValueError:
        pass
    rate = int(entry.get())
    mb = radiovar.get()
    start_thread = Thread(target=start_clicking, args=(rate, mb))
    start_thread.start()


button = ttk.Button(root, text="Start", command=button_command)
entry = ttk.Spinbox(root, from_=1, to=60000, width=9)
entry.insert(0, "100")

# Setting objects to grid
label_1.grid(row=0, column=0, sticky="NW", padx=globalpadx, pady=globalpady, columnspan=2)
radio_left.grid(row=1, column=0, sticky="NW", padx=globalpadx, pady=globalpady, columnspan=2)
radio_left.invoke()
radio_right.grid(row=2, column=0, sticky="NW", padx=globalpadx, pady=globalpady, columnspan=2)
label_2.grid(row=3, column=0, sticky="NW", padx=globalpadx, pady=globalpady)
entry.grid(row=3, column=1, sticky="NE", padx=globalpadx, pady=globalpady)

label_3.grid(row=4, column=0, sticky="SW", padx=globalpadx, pady=globalpady)
button.grid(row=4, column=1, sticky="SE", padx=globalpadx, pady=globalpady)

# Start and join listener
listener = keyboard.Listener(on_press=detect_key)
listener_thread = Thread(target=listener.start)
listener_thread.start()

# Start window main loop
root.mainloop()
