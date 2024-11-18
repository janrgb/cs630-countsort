import tkinter as tk
from tkinter import ttk

# Set up the window and title it.
root = tk.Tk()
root.title("Feet to Meters")

# Create a "content frame" or "frame widget".
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)