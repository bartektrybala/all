from tkinter import *

window = Tk()

ww = 1000
wh = 500

canvas = Canvas(window, width=ww, height=wh, bg='white')
canvas.grid(row=0, column=0)
window.title('Collins')

window.mainloop()