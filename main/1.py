from tkinter import *

window = Tk()
window.geometry('600x400')

# set widget object
label = Label(window, text="Vertical lab 1")
# set position of widget into grid
label.grid(column=0, row=0)

label = Label(window, text="Vertical lab 2")
label.grid(column=0, row=1)
label = Radiobutton(window, text="Horizontal lab 1", value=0)
label.grid(column=0, row=2)
label = Radiobutton(window, text="Horizontal lab 2", value=1)
label.grid(column=1, row=2)
label = Radiobutton(window, text="Horizontal lab 3", value=0)
label.grid(column=0, row=3)
label = Radiobutton(window, text="Horizontal lab 4", value=1)
label.grid(column=1, row=3)
label = Label(window, text="Vertical lab 3")
label.grid(column=0, row=4)

window.mainloop()