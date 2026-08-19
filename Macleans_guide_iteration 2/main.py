# main.py iteration 2

import tkinter as tk
from tkinter import messagebox, ttk
from database import check_login, get_all_markers, init_db

WINDOW_SIZE = "360x640"
APP_TITLE = "Macleans Guide"

frames = {}
entry_user = None#none is used to indicate that the variable is not yet assigned a value
entry_pass = None
map_canvas = None

def show_frame(frame_name: str): # Switches between frames using global dictionary
    frame = frames[frame_name]
    frame.tkraise()

def attempt_login():
    user = entry_user.get() 
    pwd = entry_pass.get()
    
    #Database query check instead of hardcoded values
    if check_login(user, pwd): 
        show_frame("MapPage")
        entry_user.delete(0, tk.END) #clears entry widget
        entry_pass.delete(0, tk.END) 
    else:
        messagebox.showerror("Login Failed", "Invalid credentials stored in database.")

def load_markers_from_database(): 
    #draw pins from SQLite table
    markers = get_all_markers()   
    for marker in markers: #tuple containing marker id, name, x and y coords
        marker_id, name, x, y = marker
        map_canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")

def build_gui():
    global frames, entry_user, entry_pass, map_canvas 
    
        #database
    init_db()
    
    root = tk.Tk() 
    root.title(APP_TITLE)
    root.geometry(WINDOW_SIZE)
    root.resizable(False, False)

    container = tk.Frame(root) #container frame to hold other frames
    container.pack(fill="both", expand=True) 

    # Login Page
    login_frame = tk.Frame(container, bg="#b6c1ff")
    login_frame.place(relwidth=1, relheight=1)
    frames["LoginPage"] = login_frame

    tk.Label(login_frame, text="Macleans Login", font=("Arial", 16, "bold"), bg="#b6c1ff").pack(pady=(80, 20))
    entry_user = tk.Entry(login_frame)
    entry_user.pack(pady=5)
    entry_pass = tk.Entry(login_frame, show="*")
    entry_pass.pack(pady=5)
    tk.Button(login_frame, text="Login", width=15, command=attempt_login).pack(pady=20)

    # Map Page
    map_frame = tk.Frame(container, bg="#ffffff")
    map_frame.place(relwidth=1, relheight=1)
    frames["MapPage"] = map_frame

    tk.Label(map_frame, text=APP_TITLE, font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)

    category_dropdown = ttk.Combobox(map_frame, values=["Houses", "Sports", "Staff"])
    category_dropdown.set("Select Category...")
    category_dropdown.pack(pady=5)

    search_frame = tk.Frame(map_frame, bg="#ffffff")
    search_frame.pack(pady=5)
    search_entry = tk.Entry(search_frame, width=20)
    search_entry.pack(side="left", padx=5)
    tk.Button(search_frame, text="Search").pack(side="left")

    map_canvas = tk.Canvas(map_frame, bg="#d3d3d3", highlightthickness=0)
    map_canvas.pack(fill="both", expand=True)

    # call database load function
    load_markers_from_database()

    nav_frame = tk.Frame(map_frame, bg="#799dff", height=50)
    nav_frame.pack(side="bottom", fill="x")
    nav_frame.pack_propagate(False) #pack_propagate prevents keeps frame from resizing. maintains height of 50

#buttons for navigation
    tk.Button(nav_frame, text="Map").pack(side="left", expand=True, fill="both", padx=1, pady=1)
    tk.Button(nav_frame, text="Info 1").pack(side="left", expand=True, fill="both", padx=1, pady=1)

    show_frame("LoginPage")
    root.mainloop()

if __name__ == "__main__":
    build_gui()