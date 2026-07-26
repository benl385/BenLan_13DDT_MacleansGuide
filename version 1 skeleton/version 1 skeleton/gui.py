import tkinter as tk #imports tkinter as name "tk" for short
from tkinter import ttk #ttk imports themed widges, more modern, more aesthetic

root = tk.Tk() #creates main window, assings variabe "root"
root.title("Macleans Guide") 
root.geometry("360x640")

# Header
header = tk.Label(root, text="Macleans Guide", font=("Arial", 16))
header.pack(pady=10) 

# Map placeholder
map_label = tk.Label( #placeholder for map image
    root,
    text="MAP IMAGE",
    width=30,
    height=15,
    relief="solid" #relief is to make it look like a box, creates simple border
)
map_label.pack(pady=10) #pady = padding .pack tells tkinter to add the widget to the window.

# Dropdown
location = ttk.Combobox(
    root,
    values=["Location 1", "Location 2", "Location 3"]
)
location.pack(pady=5)

# Entry box
search = tk.Entry(root)
search.pack(pady=5)

# Button
search_button = tk.Button(root, text="Search")
search_button.pack(pady=5)

# Bottom navigation
nav_frame = tk.Frame(root) 
nav_frame.pack(side="bottom", fill="x")

tk.Button(nav_frame, text="navbtn1").pack(side="left", expand=True) #creates button, tells tkinter put this button inside left of nav frame
tk.Button(nav_frame, text="navbtn2").pack(side="left", expand=True) #expand = true means take up any extra avaliable space
tk.Button(nav_frame, text="navbtn3").pack(side="left", expand=True)

root.mainloop()