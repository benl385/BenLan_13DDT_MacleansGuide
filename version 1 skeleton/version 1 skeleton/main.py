# import module
from tkinter import *

# create root window
root = Tk()
                                                                                                                                                                                                    
#root window title and dimension
root.title("welcome to GeekForGeeks")
# set geometry (widthxheight)
root.geometry('350x200')

button = Tk.Button(root, text="Close", command=root.destroy) #closes the window
button.pack()

# all widgets will be here
# execute TKinter
root.mainloop()
