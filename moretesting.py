import tkinter as tk
root = tk.Tk()

oof = tk.Frame(root)
oof.pack()
labelnub = tk.Label(oof,text="Hello")
labelnub.grid()

Entrynub = tk.Entry(oof)
Entrynub.grid()

values = oof.winfo_children()

for i in range(len(values)):
    values[i].grid_forget()

newLabel = tk.Label(oof,text="worked?")
newLabel.grid()

root.mainloop()