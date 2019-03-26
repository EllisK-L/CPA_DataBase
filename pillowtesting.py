from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import tkinter as tk
import os

#going to add this when everything else is set up.
#for files in os.listdir("Assets/temp"):
#    os.remove("Assets/temp/"+str(files))

class makeButtonImg:
    def __init__(self,text="",length=50,height=50,bg=[255,0,0],fg=[255,255,255],tc=""):
        FNF = True
        fileName = str(str(length)+str(height)+str(text)+"png")
        for f in os.listdir("Assets/temp"):
            if f == fileName:
                FNF = False
                break
        if FNF == True:
            if tc == "":
                tc = fg
            self.totalSize = length,height
            self.text = text
            buttonImg = Image.new("RGBA",(length,height),(bg[0],bg[1],bg[2]))
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
            buttonImg.show()
            buttonImg.save(fileName,"PNG")
        self.buttonPic = tk.PhotoImage(file=fileName)
root = tk.Tk()
pic = tk.PhotoImage(file="Assets/temp/100100Hello.png")
oof = makeButtonImg(text="Hello",length=100,height=100)
button1 = tk.Button(root,image=pic,height=100,width=100,relief="flat")
button1.grid()

root.mainloop()

print("Done")