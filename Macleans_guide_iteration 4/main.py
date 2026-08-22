# main.py
# Macleans Guide App - Mobile layout.

import os
import tkinter as tk
from tkinter import messagebox, ttk #messagebox is used to display popups

from constants import (
    APP_TITLE, COLOR_BG, COLOR_NAV, COLOR_WHITE,
    FONT_HEADER, FONT_TITLE, WINDOW_SIZE
)
from database import check_login, init_db, get_all_markers
from validation import validate_login_input

QUICK_CHECK_MODE = True

class MacleansApp:
    # Main GUI application class.
    
    def __init__(self, root: tk.Tk): #self is used to refer to instance of class
        self.root = root # root is the main window of the application
        self.root.title(APP_TITLE) 
        self.root.geometry(WINDOW_SIZE) 
        self.root.resizable(False, False) # does not allow resizing of the window

        init_db()  # Initialize database setup

        #tk.frame is a container widget that can hold other widgets
        self.container = tk.Frame(self.root)  # .container is a frame that will hold all other frames (pages)
        self.container.pack(fill="both", expand=True)

        self.frames = {} # frames dictionary will hold all the different pages of the app
        self.is_panning = False

        self.info_page_names = [
            "Extra curriculars",
            "School rules",
            "Macleans Information",
        ]

        #other pages
        self._create_login_page()
        self._create_map_page()
        for page_name in self.info_page_names:
            if page_name == "Extra curriculars":
                self._create_info_page(page_name, "Extra Curriculars page")
            elif page_name == "School rules":
                self._create_info_page(page_name, "School Rules page")
            else:
                self._create_info_page(page_name, "Macleans Information page")

        if QUICK_CHECK_MODE:
            self.show_frame("MapPage")
        else:
            self.show_frame("LoginPage")

    def show_frame(self, frame_name: str): #str used to specify name of frame is string
        # Brings selected page to front. Login page is shown first
        frame = self.frames[frame_name]
        frame.tkraise() #tkraise brings the frame to the front of the stacking order

    #PAGE LAYOUTS

    def _create_login_page(self):
        # Builds the login page.
        frame = tk.Frame(self.container, bg=COLOR_BG)
        frame.place(relwidth=1, relheight=1) #relwidth and relheight set the frame to fill the entire container relative
        self.frames["LoginPage"] = frame

        tk.Label( #tk.label is a widget that displays text or images. used to display the title of the app
            frame, text="Macleans Login", font=FONT_HEADER, bg=COLOR_BG
        ).pack(pady=(80, 20)) #pack is used to add the widget to the frame

        tk.Label(frame, text="Username:", bg=COLOR_BG).pack(pady=(5, 2))
        self.entry_user = tk.Entry(frame) #self.entry_user is an entry widget for the user to write their username
        self.entry_user.pack(pady=5)

        tk.Label(frame, text="Password:", bg=COLOR_BG).pack(pady=(5, 2))
        self.entry_pass = tk.Entry(frame, show="*") #self.entry_pass is another entry widget for the password
        self.entry_pass.pack(pady=5)

        tk.Button( #login buton
            frame, text="Login", width=15, command=self.attempt_login
        ).pack(pady=20)

    def _create_map_page(self):
        # Builds main map page
        frame = tk.Frame(self.container, bg=COLOR_WHITE)
        frame.place(relwidth=1, relheight=1)
        self.frames["MapPage"] = frame

        # Header
        tk.Label(frame, text=APP_TITLE, font=FONT_HEADER, bg=COLOR_WHITE).pack(pady=10)

        #Dropdown Menu
        self.category_var = tk.StringVar() #tk.stringvar is a variable class. used to change the value of the dropdown menu
        categories = ["All Categories", "Whanau Houses", "Sports", "Staff"] #will add more categories in future
        dropdown = ttk.Combobox( #combobox is a widget allowing user to select from list.
            frame, textvariable=self.category_var, values=categories, state="readonly", width=25
        )
        dropdown.set("Select Category...")
        dropdown.pack(pady=5)

        #Search Bar Row
        search_frame = tk.Frame(frame, bg=COLOR_WHITE) 
        search_frame.pack(pady=5)
        self.search_entry = tk.Entry(search_frame, width=20)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search").pack(side="left") #.pack is used to add the button to the search_frame
        self.marker_status = tk.Label(frame, text="", bg=COLOR_WHITE, height=1)
        self.marker_status.pack()

        #Map Canvas (Expands to fill all remaining space, no borders)
        self.map_canvas = tk.Canvas(
            frame, bg="#d3d3d3", highlightthickness=0
        )
        self.map_canvas.pack(fill="both", expand=True) #expand used to make the canvas expand fill all space in the frame

        # Load image safely if present
        try:
            #os.path is module joins paths together to create a path to the map image.
            img_path = os.path.join(os.path.dirname(__file__), "assets", "map.png") 
            self.map_image = tk.PhotoImage(file=img_path) #tk.photoimage is a class used to display images in tkinter
            self.map_canvas.create_image(0, 0, image=self.map_image, anchor="nw")
            self.map_canvas.configure(
                scrollregion=(0, 0, self.map_image.width(), self.map_image.height())
            )
        except Exception:
            self.map_canvas.create_text(
                180, 150, text="MAP IMAGE PLACEHOLDER\n(Add assets/map.png)", justify="center"
            )

        #Draw markers/pins from the database
        self._load_markers_from_db()
        
        # Enable panning/dragging so the user can explore map
        self.map_canvas.bind("<ButtonPress-1>", self.start_pan)
        self.map_canvas.bind("<B1-Motion>", self.pan_map)

        #  Bottom Navigation Bar
        self._add_bottom_navigation(frame, self.info_page_names)

    def _load_markers_from_db(self):
        # Pulls marker data from SQLite and draws them on the canvas
        markers = get_all_markers()
        
        for marker in markers:
            marker_id, name, x, y = marker
            
            # Draw a red circle
            circle = self.map_canvas.create_oval(x-12, y-12, x+12, y+12, fill="red")
            
            # Added hover tooltips
            self.map_canvas.tag_bind(
                circle, 
                "<Enter>", 
                lambda e, m_name=name, m_x=x, m_y=y: self.on_pin_hover(e, m_name, m_x, m_y)
            )
            self.map_canvas.tag_bind(
                circle, 
                "<Leave>", 
                self.on_pin_leave
            )

            # Make the marker clickable by tying an event to it
            self.map_canvas.tag_bind(
                circle,
                "<ButtonRelease-1>",
                lambda e, m_name=name: self.on_pin_click(e, m_name) #will add proper information later
                #lambda function is used to create a small function that will be used when the marker is clicked
            )
            
    def on_pin_hover(self, event, name: str, x: int, y: int):
        self.marker_status.config(text=name)

    def on_pin_leave(self, event):
        self.marker_status.config(text="")

    def on_pin_click(self, event, name: str):
    
        if not self.is_panning:
            messagebox.showinfo("Location", f"clicked on {name}", parent=self.root)

    def _create_info_page(self, frame_name: str, title: str): #info pages, will add proper information in later iterations
        frame = tk.Frame(self.container, bg=COLOR_WHITE)
        frame.place(relwidth=1, relheight=1)
        self.frames[frame_name] = frame

        tk.Label(frame, text=title, font=FONT_TITLE, bg=COLOR_WHITE).pack(pady=20)
        tk.Label(frame, text="(Content will be added later)", bg=COLOR_WHITE).pack(pady=50)

        self._add_bottom_navigation(frame, self.info_page_names)

    def _add_bottom_navigation(self, parent_frame: tk.Frame, info_page_names: list[str] | None = None):
        # Adds consistent bottom navigation bar.
        nav_frame = tk.Frame(parent_frame, bg=COLOR_NAV, height=50)
        nav_frame.pack(side="bottom", fill="x")
        nav_frame.pack_propagate(False) #pack propagate prevents frame from resizing, keeps height fixed at 50

        tk.Button(
            nav_frame, text="Map", command=lambda: self.show_frame("MapPage")
        ).pack(side="left", expand=True, fill="both", padx=1, pady=1)

        if info_page_names:
            for page_name in info_page_names:
                tk.Button(
                    nav_frame,
                    text=page_name,
                    command=lambda name=page_name: self.show_frame(name),
                ).pack(side="left", expand=True, fill="both", padx=1, pady=1)

    #actions:

    def attempt_login(self):
        # Validates user input and verifies against database.
        user = self.entry_user.get()
        pwd = self.entry_pass.get() 

        is_valid, error_msg = validate_login_input(user, pwd)
        if not is_valid:
            messagebox.showwarning("Input Error", error_msg)
            return

        if check_login(user, pwd):
            self.show_frame("MapPage")
            self.entry_user.delete(0, tk.END)
            self.entry_pass.delete(0, tk.END)
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid credentials.\nTry one of these:\nstudent1 / studentpassword1\nteacher1 / teacherpassword1\nadmin1 / adminpassword1"
            )#will add more realistic usernames and passwords to database later, for now these are just placeholders

    def start_pan(self, event):
        # Records the starting point when the user clicks the map.
        self.is_panning = False
        self.map_canvas.scan_mark(event.x, event.y)
        
    def pan_map(self, event):
        # Updates the canvas view as the user drags the mouse allows navigation of the image
        self.is_panning = True
        self.map_canvas.scan_dragto(event.x, event.y, gain=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = MacleansApp(root)
    root.mainloop()