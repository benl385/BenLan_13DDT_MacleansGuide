# main.py

import tkinter as tk
from tkinter import messagebox, ttk

# App Configuration
WINDOW_SIZE = "360x640"
APP_TITLE = "Macleans Guide" 

# Global GUI variables
frames = { }
entry_user = None #none is used to indicate that the variable is not yet assigned a value
entry_pass = None

def show_frame(frame_name: str):
    # Switches between frames using global dictionary
    frame = frames[frame_name] 
    frame.tkraise() #tkraise is used to bring the frame to the front

def attempt_login(): 
    user = entry_user.get() #.get used to retrieve the text entered in the entry widget
    pwd = entry_pass.get() #same
     
    if user == "student1" and pwd == "password1":
        show_frame("MapPage") #shows page if login is successful 
        entry_user.delete(0, tk.END) #.delete used to clear the entry widget after login
        entry_pass.delete(0, tk.END) 
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")

def build_gui():
    global frames, entry_user, entry_pass #entry variables declared as global to be used in other functions
    
    root = tk.Tk()
    root.title(APP_TITLE) #title of the window
    root.geometry(WINDOW_SIZE) #sets the size of the window
    root.resizable(False, False)


    container = tk.Frame(root)
    container.pack(fill="both", expand=True) #fills window, expands to fill space

#login page
    login_frame = tk.Frame(container, bg="#b6c1ff")
    login_frame.place(relwidth=1, relheight=1) #relwidth/height used to set frame to fil the container
    frames["LoginPage"] = login_frame # adds login frame to global dictionary of frames

    tk.Label(login_frame, text="Macleans Login", font=("Arial", 16, "bold"), bg="#b6c1ff").pack(pady=(80, 20))
    #.pack used to place the label in the frame
    
    tk.Label(login_frame, text="Username:", bg="#b6c1ff").pack(pady=(5, 2))
    entry_user = tk.Entry(login_frame)
    entry_user.pack(pady=5)

    tk.Label(login_frame, text="Password:", bg="#b6c1ff").pack(pady=(5, 2))
    entry_pass = tk.Entry(login_frame, show="*")
    entry_pass.pack(pady=5)

    tk.Button(login_frame, text="Login", width=15, command=attempt_login).pack(pady=20)

    #map page
    map_frame = tk.Frame(container, bg="#ffffff")
    map_frame.place(relwidth=1, relheight=1)
    frames["MapPage"] = map_frame

    #HEader
    tk.Label(map_frame, text=APP_TITLE, font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)

    # Combobox
    category_dropdown = ttk.Combobox(map_frame, values=["Location 1", "Location 2", "Location 3"])
    category_dropdown.set("Select Location...")
    category_dropdown.pack(pady=5)

    # Search bar row
    search_frame = tk.Frame(map_frame, bg="#ffffff")
    search_frame.pack(pady=5)
    search_entry = tk.Entry(search_frame, width=20)
    search_entry.pack(side="left", padx=5)
    tk.Button(search_frame, text="Search").pack(side="left")

    # Map canvas placeholder
    map_canvas = tk.Canvas(map_frame, bg="#d3d3d3", highlightthickness=0)
    map_canvas.pack(fill="both", expand=True)
    map_canvas.create_text(180, 150, text="MAP IMAGE PLACEHOLDER", justify="center")

    # Hardcoded map pins directly drawn on canvas
    map_canvas.create_oval(140, 140, 160, 160, fill="red") # Batten House
    map_canvas.create_oval(190, 90, 210, 110, fill="red")   # Kupe House

    # Bottom Navigation
    nav_frame = tk.Frame(map_frame, bg="#799dff", height=50)
    nav_frame.pack(side="bottom", fill="x")
    nav_frame.pack_propagate(False)

    tk.Button(nav_frame, text="Map").pack(side="left", expand=True, fill="both", padx=1, pady=1)
    tk.Button(nav_frame, text="Info 1").pack(side="left", expand=True, fill="both", padx=1, pady=1)
    tk.Button(nav_frame, text="Info 2").pack(side="left", expand=True, fill="both", padx=1, pady=1)

    # Show login frame by default
    show_frame("LoginPage")
    root.mainloop()

if __name__ == "__main__":
    build_gui()