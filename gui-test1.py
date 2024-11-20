import tkinter as tk
from tkinter import ttk

# Create main window.
root = tk.Tk()
root.title('Table with TreeView (Grid Layout)')

# Configure grid layout of main window.
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Create the frame to house the TreeView and Scrollbars.
frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky="nsew")

# Define columns for the table.
columns = ("ID", "Name", "Age", "Department")

# Configure the grid layout of the frame.
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)

# Define headings & column config
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=100)

# Add sample data to the table.
data = [
    (1, "Alice", 30, "HR"),
    (2, "Bob", 25, "Engineering"),
    (3, "Charlie", 35, "Finance"),
    (4, "Diana", 28, "Marketing"),
    (5, "Eve", 40, "Legal"),
]

for row in data:
    tree.insert("", tk.END, values=row)

# Add TreeView widgets to frame
tree.grid(row=0, column=0, sticky="nsew")

# Add a vertical scrollbar.
v_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
v_scroll.grid(row=0, column=1, sticky="ns")

# Add horizontal scrollbar.
h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
h_scroll.grid(row=1, column=0, sticky="ew")

root.mainloop()