from tkinter import *
import platform


if platform.system() == "Darwin":   ### if its a Mac
    B = Button(text="Refersh All Windows", highlightbackground="Yellow", fg="Black", highlightthickness=30)
else:  ### if its Windows or Linux
    B = Button(text="Refresh All Windows", bg="Yellow", fg="Black")

B.place(x=5, y=10, width=140, height=30)

mainloop()