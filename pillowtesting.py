from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import tkinter as tk
import os

#going to add this when everything else is set up.
#for files in os.listdir("Assets/temp"):
#    os.remove("Assets/temp/"+str(files))

class makeButtonImg:
    def __init__(self,text="",length=50,height=50,bg=[255,0,0],fg=[255,255,255],tc=""):
        if tc == "":
            tc = fg
        self.totalSize = length,height
        self.text = text
        buttonImg = Image.new("RGBA",(length,height),(bg[0],bg[1],bg[2]))
        boarderImg = Image.new("RGBA",(length+10,height+10),"black")
        #boarderImg = ImageDraw.Draw(boarderImg)
        font = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf",int(height))
        buttonImgDraw = ImageDraw.Draw(buttonImg)
        tL,tH = buttonImgDraw.textsize(text,font=font)
        print("Text Length: ",tL)

        if tL > length:
            font = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf",int(length/3))
            tL,tH = buttonImgDraw.textsize(text,font=font)
            buttonImgDraw.text(((length - tL)/2,int((height - tH)/2)*(14/16)),text,(tc[0],tc[1],tc[2]),font=font)
        else:
            buttonImgDraw.text(((length - tL)/2,int((height - tH)/2)*(45/16)),text,(tc[0],tc[1],tc[2]),font=font)
        print(tH)

        boarderImg.paste(buttonImg,(0,0))
        boarderImg.show()
        boarderImg.save("Assets/temp/oop.png","PNG")
        button_pic_1 = tk.PhotoImage(file="Assets/buttonTexRaw.png")
        self.buttonPic = tk.PhotoImage(file="Assets/temp/oop.png")
root = tk.Tk()

oof = makeButtonImg(text="Hello",length=6000,height=4000)
testimg = tk.PhotoImage(file="Assets/temp/oop.png")
button1 = tk.Button(root,image=oof.buttonPic,height=100,width=100,relief="flat")
button1.pack()

root.mainloop()

print("Done")