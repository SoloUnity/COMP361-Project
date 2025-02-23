import tkinter as tk
from tkinter.filedialog import askopenfilename
tk.Tk().withdraw() # part of the import if you are not using other tkinter functions

fn = askopenfilename()
print("user chose", fn)