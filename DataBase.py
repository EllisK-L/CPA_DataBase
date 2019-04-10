#from tkinter import *
import threading, time, os, webbrowser
from tkinter import messagebox
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import tkinter as tk
#
#
debug = True
#
#

class makeButtonImg:
    def __init__(self,text="",length=50,height=50,bg=[255,0,0],fg=[255,255,255],tc="",textSize=15,yOffset=1,xOffset=1):
        print(length)
        FNF = True
        fileName = str(str(length)+str(height)+str(text)+".png")
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
            font = ImageFont.truetype("Assets/Fonts/ariblk.ttf",int(textSize))
            #font = ImageFont.truetype("TkFixedFont",int(textSize))
            buttonImgDraw = ImageDraw.Draw(buttonImg)
            tL,tH = buttonImgDraw.textsize(text,font=font)
            print("Text Length: ",tL)
            #if tL > length:
            #    font = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf",int(length/4))
            #    tL,tH = buttonImgDraw.textsize(text,font=font)
            #    buttonImgDraw.text(((length - tL)/2,int((height - tH)/2)*(14/16)),text,(tc[0],tc[1],tc[2]),font=font)
            #else:
            #    buttonImgDraw.text(((length - tL)/2,int((height - tH)/2)*(45/16)),text,(tc[0],tc[1],tc[2]),font=font)
            print(tH)
            #buttonImg.show()
            buttonImgDraw.text((int(xOffset*(length - tL)/2),int((height - tH)/2)*yOffset),text,(tc[0],tc[1],tc[2]),font=font)
            buttonImg.save("Assets/temp/"+fileName,"PNG")
        self.buttonPic = tk.PhotoImage(file="Assets/temp/"+fileName)


numOfFrames = 0


root=tk.Tk()
#root.tk_setPalette(background='gray15', foreground='white', activeForeground="red")
button_pic_1 = tk.PhotoImage(file="Assets/buttonTexRaw.png")

root.tk_setPalette(background='gray13', foreground='white',activeBackground='black', activeForeground="red")

root.resizable(False,False)
if os.name ==  "nt":
    root.iconbitmap(default='transparent.ico')
if os.name == "mac":
    pass
root.title("CPA Data Base")
quitThread = False


def openDoc():
    doc = open("Data.txt","r")
    data = doc.readlines()
    for i in range(len(data)):
        data[i] = data[i].split("|")
        del data[i][len(data[i])-1]
    doc.close()
    return data

def addItem(itemName,itemID,itemQuant,searchResultBox,searchFrame,addFrame):
    global numOfFrames
    writeData = ""
    data = openDoc()
    data[0].append(itemName)
    data[1].append(itemID)
    data[2].append(itemQuant)
    data[3].append("0")
    data[4].append(itemQuant)
    doc = open("Data.txt","w")
    for i in range(len(data)):
        for j in range(len(data[i])):
            writeData += data[i][j].strip("\n") + "|"
        writeData += "\n"
    doc.write(writeData)
    doc.close()
    searchResultBox.destroy()
    numOfFrames -= 1
    searchSetup(searchFrame)
    searchFrame.destroy()
    addFrame.destroy()
    setup()

def devider(frame,row,column):
    devider = tk.Label(frame)
    devider.grid(row=row,column=column,columnspan=2)

def searchSelector(frame,searchResultBox,choice):
    print(choice.get())
    if choice.get() == "All Items":
        searchSetup(frame)
    if choice.get() == "Location":
        searchPlace(frame,searchResultBox)


def searchPlace(frame,searchResultBox):
    locations = []
    data = openDoc()
    quitFlag = False
    if len(data[5]) > 1:
        for i in range(1,len(data[5])):
            data[5][i] = data[5][i].split("%")
    #[5][4]
    searchResultBox.delete(0,"end")
    #Getting all locations
    for i in range(1,len(data[5])):
        quitFlag = False
        for j in range(len(locations)):
            if data[5][i][4] == locations[j]:
                quitFlag = True
        if quitFlag == False:
            locations.append(str(data[5][i][4]))
            searchResultBox.insert(tk.END,locations[len(locations)-1])




def searchSetup(frame):
    pass

def setup():

    global numOfFrames, quitThread, searchState, var
    searchState = "All Items"
    quitThread = False
    def searchThreadFunc():
        global quitThread, searchState, var
        pause = False
        data = openDoc()
        new = ""
        finalList = []
        while quitThread == False:
            time.sleep(.1)
            if var.get() == "All Items":
                print("Threading")
                try:
                    userSearch = str(searchBox.get())
                except:
                    break
                boxString = ""
                old = new
                new = userSearch
                if new != old or pause == True:
                    if userSearch == "":
                        searchResultBox.delete(0,"end")
                        formatSearchBox(data,searchResultBox)
                    else:
                        searchResultBox.delete(0,"end")
                        boxString = ""
                        for i in range(1,len(data[0])):
                            for j in range(len(data)-2):
                                boxString += data[j][i].strip("\n")
                                if j != 3:
                                    for k in range(30-len(str(data[j][i]))):
                                        boxString += " "
                            if userSearch.upper() in boxString.upper():
                                finalList.append(boxString)
                                #searchResultBox.insert(END,boxString)
                            boxString = ""
                        for i in range(len(finalList)):
                            searchResultBox.insert(tk.END,finalList[i])
                            if i % 2 == 0:
                                searchResultBox.itemconfig(i, {"bg": "gray20"})
                        finalList = []
                pause = False
            else:
                pause = True


    


    searchThread = threading.Thread(target=searchThreadFunc,args="")
    searchThread.start()
    searchFrame = tk.Frame(root)
    numOfFrames += 1
    searchFrame.grid(row=0,column=0)

    searchLabel = tk.Label(searchFrame,text="Search")
    searchLabel.grid(stick=tk.E)

    searchBox = tk.Entry(searchFrame,width=20)
    searchBox.grid(row=0,column=1)


    searchHeaderData = ""
    data = openDoc()
    if len(data[5]) > 1:
        for i in range(1,len(data[5])):
            data[5][i] = data[5][i].split("%")

    for i in range(0,len(data)-2):
        searchHeaderData += data[i][0]
        for j in range(25-len(data[i][0])):
            searchHeaderData += " "

    searchHeader = tk.Label(searchFrame,text=searchHeaderData,font='TkFixedFont')
    searchHeader.grid(row=1,column=0,columnspan=20)
    def searchSelect(evt):
                value = searchResultBox.get(searchResultBox.curselection())
    searchResultBox = tk.Listbox(searchFrame,relief="flat",width=100,height=30,font='TkFixedFont',selectbackground="gray30",highlightcolor="gray15",bg="gray10",selectmode="SINGLE",bd=1)
    searchResultBox.grid(row=2,columnspan=100)
    data = openDoc()
    formatSearchBox(data,searchResultBox)
    searchResultBox.bind('<<ListboxSelect>>', searchSelect)

    var = tk.StringVar(root)
    var.set("Item Name")
    searchOptions = tk.OptionMenu(searchFrame,var,"All Items","Location",command=lambda x:searchSelector(searchFrame,searchResultBox,var))
    searchOptions.grid(row=0,column=3,sticky=tk.W)

    searchOptionLabel = tk.Label(searchFrame,text="Search By: ")
    searchOptionLabel.grid(row=0,column=2,sticky=tk.E)

    data = openDoc()

    #Add (right side)-----------------------------------------------

    addFrame = tk.Frame(root)
    numOfFrames += 1
    addFrame.grid(row=0,column=1,columnspan=3)

    addText = tk.Label(addFrame,text="Add Item\n—————————————————")

    addText.grid(row=0,column=0,columnspan=5)

    nameLabel = tk.Label(addFrame,text="Name")
    nameLabel.grid(row=1,column=0,sticky=tk.E)
    nameBox = tk.Entry(addFrame,width=20)
    nameBox.grid(row=1,column=2,columnspan=3)

    devider(addFrame,2,0)

    itemIdLabel = tk.Label(addFrame,text="Item ID")
    itemIdLabel.grid(row=3,column=0,sticky=tk.E)
    itemIDBox = tk.Entry(addFrame,width=20)
    itemIDBox.grid(row=3,column=2,columnspan=3,)

    devider(addFrame,4,0)

    itemQuantLabel = tk.Label(addFrame,text="Quantity")
    itemQuantLabel.grid(row=5,column=0,sticky=tk.E)
    itemQuantBox = tk.Entry(addFrame,width=20)
    itemQuantBox.grid(row=5,column=2,columnspan=3,)

    devider(addFrame,6,0)
    submitButtonImg = makeButtonImg(text="Submit",length=65,height=30,bg=[64,64,64],yOffset=.7)
    submitButton = tk.Button(addFrame,relief="flat",image=submitButtonImg.buttonPic,command= lambda: addItem(nameBox.get(),itemIDBox.get(),itemQuantBox.get(),searchResultBox,searchFrame,addFrame))
    submitButton.image = submitButtonImg.buttonPic
    submitButton.grid(row=7,column=2)

    searchResultBox.bind('<Double-Button-1>',lambda eff: getDetails(searchResultBox.get(searchResultBox.curselection()),searchResultBox,searchFrame,addFrame))
    buttons(searchFrame,searchResultBox,addFrame)


def bugReport():
    webbrowser.open("https://docs.google.com/forms/d/e/1FAIpQLSeJ7VBd0OkONfw9PMq4C4dx7BhxgOXACpDsVKdUTAT7ICWApg/viewform?usp=sf_link")


def buttons(frame,searchBox,addFrame):
    deleteButtonImg = makeButtonImg(text="X",bg=[255,0,0],height=20,length=30,yOffset=-2)
    deleteButton = tk.Button(frame,relief="flat",image=deleteButtonImg.buttonPic,command=lambda :deleteInit(searchBox.get(searchBox.curselection()),searchBox,frame,addFrame))
    deleteButton.image = deleteButtonImg.buttonPic
    deleteButton.grid(row=4,column=0)

    detailButtonImg = makeButtonImg(height=35,length=85,text="Details",bg=[64,64,64],textSize=15,yOffset=.7)
    detailButton = tk.Button(frame,relief="flat",image=detailButtonImg.buttonPic,height=35,width=85,command=lambda : getDetails(searchBox.get(searchBox.curselection()),searchBox,frame,addFrame))
    detailButton.image = detailButtonImg.buttonPic

    detailButton.grid(row=4,column=4)

#flat, groove, raised, ridge, solid, or sunken

def formatSearchBox(data,box):
    finalList = []
    boxString = ""
    for i in range(1,len(data[0])):
        for j in range(len(data)-2):
            boxString += data[j][i].strip("\n")
            if j != 3:
                for k in range(30-len(str(data[j][i]))):
                    boxString += " "
        finalList.append(boxString)
        boxString = ""
    for i in range(len(finalList)):
        box.insert(tk.END,finalList[i])
        if i % 2 == 0:
            box.itemconfig(i, {"bg": "gray17"})



def deleteInit(line,searchResultBox,searchFrame,addFrame):
    indexToRead = ""
    text = line
    text = text[30:]
    #print(text)
    tempText = ""
    for i in range(len(text)):
        if text[i] != " ":
            tempText = text[:i+1]
        else:
            break
    data = openDoc()
    for i in range(len(data[1])):
        if data[1][i] == tempText:
            indexToRead = i

    textForUSure = "Are you sure you want to Delete\n" + data[0][indexToRead] + "?"
    if messagebox.askyesno("CPA",textForUSure,icon="warning") == True:
        deleteing("Y",indexToRead,searchResultBox,searchFrame,addFrame)
    else:
        pass

def deleteing(yOrN,indexValueToDel,searchResultBox,searchFrame,addFrame):
    global numOfFrames
    writeData = ""
    data = openDoc()
    if yOrN == "Y":
        for i in range(len(data)-1):
            del data[i][indexValueToDel]
        doc = open("Data.txt", "w")
        for i in range(len(data)):
            for j in range(len(data[i])):
                writeData += data[i][j] + "|"
            writeData += "\n"
        doc.write(writeData)
        doc.close()
        setup()
    else:
        pass
    numOfFrames -= 1
    searchFrame.destroy()
    addFrame.destroy()




def getDetails(line,searchResultBox,frame,addFrame):
    global numOfFrames
    global quitThread
    quitThread = True
    indexToRead = ""
    text = line
    text = text[30:]
    #print(text)
    tempText = ""
    for i in range(len(text)):
        if text[i] != " ":
            tempText = text[:i+1]
        else:
            break
    data = openDoc()
    for i in range(len(data[1])):
        if data[1][i] == tempText:
            indexToRead = i

#--------------------------------------------------
    def back(oldFrame,addFrame):
        global numOfFrames
        oldFrame.destroy()
        addFrame.destroy()
        numOfFrames -= 2
        setup()
#--------------------------------------------------
    #Details template: |item Number\Checked in or out\time stamp\time due\where is it\what tech\person responsible|

    indexToRead = ""
    text = line
    text = text[30:]
    tempText = ""
    for i in range(len(text)):
        if text[i] != " ":
            tempText = text[:i + 1]
        else:
            break

    data = openDoc()
    for i in range(len(data[1])):
        if data[1][i] == tempText:
            indexToRead = i
    detailFrame = tk.Frame(root)
    numOfFrames += 1
    detailFrame.grid(row=0,column=0)
    detailBox = tk.Listbox(detailFrame,relief="solid",width=100,height=30,font='TkFixedFont',selectbackground="gray30",highlightcolor="black")
    detailBox.grid(row=2,columnspan=100)
    backButtonImg = makeButtonImg(text="←",bg=[64,64,64],textSize=50,length=80,height=30,yOffset=2)
    backButton = tk.Button(detailFrame,relief="flat",image=backButtonImg.buttonPic,height=30,width=80,command=lambda :back(detailFrame,addFrame))
    backButton.image = backButtonImg
    backButton.grid(row=1,column=0)
    nameString = data[0][indexToRead]

    nameLabel = tk.Label(detailFrame,text=nameString,font=("Comic Sans MS", 20))
    nameLabel.grid(row=1,column=50-(len(nameString)//2))

    numChecked = 0

    if len(data[5]) > 1:
        for i in range(1,len(data[5])):
            data[5][i] = data[5][i].split("%")

    boxString = "Checked in:"
    for i in range(50-len(boxString)):
        boxString += " "
    for i in range(1,len(data[5])):
        if data[5][i][1] == "}in{":
            numChecked += int(data[5][i][7])
    boxString += str(numChecked)
    detailBox.insert(tk.END,boxString)
    detailBox.itemconfigure(0,{"bg":"gray10"})
    
    numChecked = 0

    boxString = "Checked out:"
    for i in range(50-len(boxString)):
        boxString += " "
    for i in range(1,len(data[5])):
        if data[5][i][1] == "}out{":
            numChecked += int(data[5][i][7])
    boxString += str(numChecked)
    detailBox.insert(tk.END,boxString)

    boxString = "'Limbo' State"
    for i in range(50-len(boxString)):
        boxString += " "
    boxString += str(data[4][indexToRead])
    detailBox.insert(tk.END,boxString)


    detailBox.bind("<Double-Button-1>",lambda eff: details2(detailFrame,detailBox.get(detailBox.curselection()),indexToRead,addFrame))

    detailButtonImg = makeButtonImg(height=35,length=85,text="Details",bg=[64,64,64],textSize=15,yOffset=.7)
    detailButton = tk.Button(detailFrame,relief="flat",image=detailButtonImg.buttonPic,height=35,width=85,command=lambda :details2(detailFrame,detailBox.get(detailBox.curselection()),indexToRead,addFrame))
    detailButton.image = detailButtonImg.buttonPic
    detailButton.grid(row=3,column=3,columnspan=73)
    frame.destroy()
    numOfFrames -= 1

def details2(oldFrame,line,indexToRead,addFrame):
    global numOfFrames
    '''
On this screen, there will be, The name of the item at the top of the screen, below there will be a set of items:
TIme stamp, time due, Where is it, person responsible, tech signed out, quantity.

#|item Number\Checked in or out\time stamp\time due\where is it\what tech\person responsible|
    '''
    def back():
        global numOfFrames
        newDetailFrame.destroy()
        quantFrame.destroy()
        addFrame.destroy()
        numOfFrames -= 3
        checkInFrame.destroy()
        setup()
    addFrame.destroy()
    oldFrame.destroy()
    numOfFrames -= 2
    newDetailFrame = tk.Frame(root)
    numOfFrames += 1
    newDetailFrame.grid(row=0,column=0,sticky=tk.W)
    backButtonImg = makeButtonImg(text="←",bg=[64,64,64],textSize=50,length=80,height=30,yOffset=2)
    backButton = tk.Button(newDetailFrame,relief="flat",image=backButtonImg.buttonPic,height=30,width=80,command=back)
    backButton.image = backButtonImg.buttonPic
    backButton.grid(row=1, column=0,stick=tk.W)

    data = openDoc()

    nameString = data[0][indexToRead]

    nameLabel = tk.Label(newDetailFrame,text=nameString,font=("Comic Sans MS", 20))
    nameLabel.grid(row=1,column=50-(len(nameString)//2))
    returnDefaultButtonImg = makeButtonImg(text="Reset Items",height=20,length=110,yOffset=-1,bg=[255,0,0])
    returnDefaultButton = tk.Button(newDetailFrame,relief="flat",image=returnDefaultButtonImg.buttonPic, fg="red")
    returnDefaultButton.image = returnDefaultButtonImg.buttonPic
    returnDefaultButton.grid(row=4, column=0)
    if "Checked out" in line:
        temp = "Time Punched In"
        tempSpace = "     "
    else:
        temp = "Time Punched Out"
        tempSpace = "     "
    #TIme stamp, time due, Where is it, person responsible, tech signed out, quantity.
    #Header----------------------------------------------------
    
#21 character in each

    boxString = ""
    if "out" in line:
        detailBox = tk.Listbox(newDetailFrame, relief="solid", width=115, height=30, font='TkFixedFont',selectbackground="gray30",highlightcolor="black")
        detailBox.grid(row=3, columnspan=100)
        headerString = "Signed Out By" + "        "+"Person Responsible"+ "   "+"Where It Is"+"          "+temp+tempSpace+"Time Due"+"             "+"Quantity"
        headerLabel = tk.Label(newDetailFrame,text=headerString,font='TkFixedFont')
        headerLabel.grid(row=2,columnspan=100,sticky=tk.W)    

        data = openDoc()

        if len(data[5]) > 1:
            for i in range(1,len(data[5])):
                data[5][i] = data[5][i].split("%")
        #-----------------------------
        #Adding all detail data in data.txt to detail2 box
        # |item Number\Checked in or out\what tech\person responsible\where is it\time punch\time due\quantity|
        boxString = ""
        indexList = []
        detailList = []
        counter = 0
        for i in range(1,len(data[5])):
            if data[5][i][0] == data[1][indexToRead] and data[5][i][1] == "}out{":
                indexList.append(i)
                for j in range(2,len(data[5][i])):
                    boxString += data[5][i][j]
                    for k in range(21-len(data[5][i][j])):
                        boxString += " "
                detailBox.insert(tk.END,boxString)
                #if i % 2 == 0:
                #    detailBox.itemconfig(i-1, {"bg": "gray10"})
                detailList.append(boxString)
                boxString = ""
                counter += 1
        #------------------------------
        checkInFrame = tk.Frame(root)
        numOfFrames += 1
        checkInFrame.grid(row=0,column=2)
        titleLabel = tk.Label(checkInFrame,text="Check In Item(s)")
        titleLabel.grid(row=0,column=0)
        devider(checkInFrame,1,0)

        techLabel = tk.Label(checkInFrame,text="Tech Checking Item(s) In")
        techLabel.grid(row=2,column=0)
        techEntry = tk.Entry(checkInFrame)
        techEntry.grid(row=3,column=0)
        devider(checkInFrame,4,0)


        whereLabel = tk.Label(checkInFrame,text="Item Location")
        whereLabel.grid(row=8,column=0)
        whereEntry = tk.Entry(checkInFrame)
        whereEntry.grid(row=9,column=0)
        devider(checkInFrame,10,0)

        timePunchLabel = tk.Label(checkInFrame,text="Time of Action")
        timePunchLabel.grid(row=11,column=0)
        timePunchEntry = tk.Entry(checkInFrame)
        timePunchEntry.grid(row=12,column=0)
        devider(checkInFrame,13,0)

        #Choose Quantity Code------------------------------------------------------------------------------------------------

        quantFrame = tk.Frame(root)
        numOfFrames += 1
        quantFrame.grid(row=1,column=0,sticky=tk.W,columnspan=150)

        quantListBox = tk.Listbox(quantFrame,width=115,height=6,font='TkFixedFont')
        quantListBox.grid(row=0,column=0,rowspan=5)

        removeQuantButtonImg = makeButtonImg(text="Remove Selection",length=160,height=35,bg=[255,0,0],yOffset=.8)
        removeQuantButton = tk.Button(quantFrame,image=removeQuantButtonImg.buttonPic)
        removeQuantButton.image = removeQuantButtonImg.buttonPic
        removeQuantButton.grid(row=6,column=0)

        quantEntryLabel = tk.Label(quantFrame,text="Enter Quantity")
        quantEntryLabel.grid(row=0,column=1)

        quantEntry = tk.Entry(quantFrame)
        quantEntry.grid(row=1,column=1)
        quantList = []
        submitCurrentQuantImg = makeButtonImg(text="Submit Quantity",length=135,height=40,bg=[64,64,64])
        submitCurrentQuant = tk.Button(quantFrame,image=submitCurrentQuantImg.buttonPic,command= lambda :insertQuantToSelection(quantListBox,quantEntry,quantList))
        submitCurrentQuant.image = submitCurrentQuantImg.buttonPic
        devider(quantFrame,2,1)
        submitCurrentQuant.grid(row=3,column=1,rowspan=2)
        finishedButtonImg = makeButtonImg(text="Check In",length=90,height=30,bg=[64,64,64])
        finishedButton = tk.Button(checkInFrame,image=finishedButtonImg.buttonPic,command=lambda : finalSubmitIn(detailBox,quantListBox,quantList,"out",techEntry,timePunchEntry,data[1][indexToRead],data,whereEntry,indexList,quantFrame,newDetailFrame,checkInFrame))
        finishedButton.image = finishedButtonImg.buttonPic
        finishedButton.grid()
        detailBox.bind("<Double-Button-1>",lambda eff:selectItemToQuant(detailBox,detailList,quantListBox,detailBox.get(detailBox.curselection()),quantList,indexList))
    elif "in" in line:


#Checked in Items Code-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#
        detailBox = tk.Listbox(newDetailFrame, relief="solid", width=80, height=30, font='TkFixedFont',selectbackground="gray30",highlightcolor="black")
        detailBox.grid(row=3, columnspan=100)
        headerString = "Signed Out By" +"        "+"Where It Is"+"          "+temp+tempSpace+"Quantity"
        headerLabel = tk.Label(newDetailFrame,text=headerString,font='TkFixedFont')
        headerLabel.grid(row=2,columnspan=100,sticky=tk.W)
        data = openDoc()

        if len(data[5]) > 1:
            for i in range(1,len(data[5])):
                data[5][i] = data[5][i].split("%")
        defaultState = int(data[4][indexToRead])
        #-----------------------------
        #Adding all detail data in data.txt to detail2 box
        # |item Number\Checked in or out\what tech\person responsible\where is it\time punch\time due\quantity|
        
        boxString = ""
        indexList = []
        detailList = []

        for i in range(1,len(data[5])):
            if data[5][i][0] == data[1][indexToRead] and data[5][i][1] == "}in{":
                indexList.append(i)
                for j in range(2,len(data[5][i])):
                    if j == 2 or j == 4 or j == 5 or j == 7:
                        boxString += data[5][i][j]
                        for k in range(21-len(data[5][i][j])):
                            boxString += " "
                detailBox.insert(tk.END,boxString)
                #if i % 2 == 0:
                #    detailBox.itemconfig(i-1, {"bg": "gray10"})
                detailList.append(boxString)
                boxString = ""
        #------------------------------
        checkInFrame = tk.Frame(root)
        numOfFrames += 1
        checkInFrame.grid(row=0,column=2)
        titleLabel = tk.Label(checkInFrame,text="Check Out Item(s)")
        titleLabel.grid(row=0,column=0)
        devider(checkInFrame,1,0)

        techLabel = tk.Label(checkInFrame,text="Tech Checking Item(s) out")
        techLabel.grid(row=2,column=0)
        techEntry = tk.Entry(checkInFrame)
        techEntry.grid(row=3,column=0)
        devider(checkInFrame,4,0)

        personLabel = tk.Label(checkInFrame,text="Person Responsible For Item(s)")
        personLabel.grid(row=5,column=0)
        personEntry = tk.Entry(checkInFrame)
        personEntry.grid(row=6,column=0)
        devider(checkInFrame,7,0)

        whereLabel = tk.Label(checkInFrame,text="Item Location")
        whereLabel.grid(row=8,column=0)
        whereEntry = tk.Entry(checkInFrame)
        whereEntry.grid(row=9,column=0)
        devider(checkInFrame,10,0)

        timePunchLabel = tk.Label(checkInFrame,text="Time of Action")
        timePunchLabel.grid(row=11,column=0)
        timePunchEntry = tk.Entry(checkInFrame)
        timePunchEntry.grid(row=12,column=0)
        devider(checkInFrame,13,0)

        timeDueLabel = tk.Label(checkInFrame,text="Time Item(s) are Due")
        timeDueLabel.grid(row=14,column=0)
        timeDueEntry = tk.Entry(checkInFrame)
        timeDueEntry.grid(row=15,column=0)
        devider(checkInFrame,16,0)


        #Choose Quantity Code------------------------------------------------------------------------------------------------

        quantFrame = tk.Frame(root)
        numOfFrames += 1
        quantFrame.grid(row=1,column=0,sticky=tk.W,columnspan=150)

        quantListBox = tk.Listbox(quantFrame,width=80,height=6,font='TkFixedFont')
        quantListBox.grid(row=0,column=0,rowspan=5)

        removeQuantButton = tk.Button(quantFrame,text="Remove",fg="red")
        removeQuantButton.grid(row=6,column=0)

        quantEntryLabel = tk.Label(quantFrame,text="Enter Quantity")
        quantEntryLabel.grid(row=0,column=1)

        quantEntry = tk.Entry(quantFrame)
        quantEntry.grid(row=1,column=1)
        quantList = []
        submitCurrentQuantImg = makeButtonImg(text="Submit Quantity",length=135,height=40,bg=[64,64,64])
        submitCurrentQuant = tk.Button(quantFrame,image=submitCurrentQuantImg.buttonPic,command= lambda :insertQuantToSelection(quantListBox,quantEntry,quantList))
        submitCurrentQuant.image = submitCurrentQuantImg.buttonPic
        devider(quantFrame,2,1)
        submitCurrentQuant.grid(row=3,column=1,rowspan=2)
        finishedButtonImg = makeButtonImg(text="Check Out",length=90,height=30,bg=[64,64,64])
        finishedButton = tk.Button(checkInFrame,image=finishedButtonImg.buttonPic,command=lambda : finalSubmitOut(detailBox,quantListBox,quantList,"out",techEntry,personEntry,timeDueEntry,timePunchEntry,data[1][indexToRead],data,whereEntry,indexList,quantFrame,newDetailFrame,checkInFrame))
        finishedButton.image = finishedButtonImg.buttonPic
        finishedButton.grid()
        detailBox.bind("<Double-Button-1>",lambda eff:selectItemToQuant(detailBox,detailList,quantListBox,detailBox.get(detailBox.curselection()),quantList,indexList))

    else:

        detailBox = tk.Listbox(newDetailFrame, relief="solid", width=80, height=30, font='TkFixedFont',selectbackground="gray30",highlightcolor="black")
        detailBox.grid(row=3, columnspan=100)
        headerString = "Quantity"
        headerLabel = tk.Label(newDetailFrame,text=headerString,font='TkFixedFont')
        headerLabel.grid(row=2,columnspan=100,sticky=tk.W)
        data = openDoc()

        if len(data[5]) > 1:
            for i in range(1,len(data[5])):
                data[5][i] = data[5][i].split("%")
        defaultState = int(data[4][indexToRead])
        detailBox.insert(tk.END,defaultState)
        #-----------------------------
        #Adding all detail data in data.txt to detail2 box
        # |item Number\Checked in or out\what tech\person responsible\where is it\time punch\time due\quantity|
        
        boxString = ""
        indexList = []
        detailList = []

        boxString = ""

        #------------------------------
        checkInFrame = tk.Frame(root)
        numOfFrames += 1
        checkInFrame.grid(row=0,column=2)
        titleLabel = tk.Label(checkInFrame,text="Check Out Item(s)")
        titleLabel.grid(row=0,column=0)
        devider(checkInFrame,1,0)

        techLabel = tk.Label(checkInFrame,text="Tech Checking Item(s) out")
        techLabel.grid(row=2,column=0)
        techEntry = tk.Entry(checkInFrame)
        techEntry.grid(row=3,column=0)
        devider(checkInFrame,4,0)

        personLabel = tk.Label(checkInFrame,text="Person Responsible For Item(s)")
        personLabel.grid(row=5,column=0)
        personEntry = tk.Entry(checkInFrame)
        personEntry.grid(row=6,column=0)
        devider(checkInFrame,7,0)

        whereLabel = tk.Label(checkInFrame,text="Item Location")
        whereLabel.grid(row=8,column=0)
        whereEntry = tk.Entry(checkInFrame)
        whereEntry.grid(row=9,column=0)
        devider(checkInFrame,10,0)

        timePunchLabel = tk.Label(checkInFrame,text="Time of Action")
        timePunchLabel.grid(row=11,column=0)
        timePunchEntry = tk.Entry(checkInFrame)
        timePunchEntry.grid(row=12,column=0)
        devider(checkInFrame,13,0)

        timeDueLabel = tk.Label(checkInFrame,text="Time Item(s) are Due")
        timeDueLabel.grid(row=14,column=0)
        timeDueEntry = tk.Entry(checkInFrame)
        timeDueEntry.grid(row=15,column=0)
        devider(checkInFrame,16,0)


        #Choose Quantity Code------------------------------------------------------------------------------------------------

        quantFrame = tk.Frame(root)
        numOfFrames += 1
        quantFrame.grid(row=1,column=0,sticky=tk.W,columnspan=150)

        quantListBox = tk.Listbox(quantFrame,width=80,height=5,font='TkFixedFont')
        quantListBox.grid(row=0,column=0,rowspan=5)

        removeQuantButton = tk.Button(quantFrame,text="Remove",fg="red")
        removeQuantButton.grid(row=6,column=0)

        quantEntryLabel = tk.Label(quantFrame,text="Enter Quantity")
        quantEntryLabel.grid(row=0,column=1)

        quantEntry = tk.Entry(quantFrame)
        quantEntry.grid(row=1,column=1)
        quantList = []
        submitCurrentQuantImg = makeButtonImg(text="Submit Quantity",length=135,height=40,bg=[64,64,64])
        submitCurrentQuant = tk.Button(quantFrame,image=submitCurrentQuantImg.buttonPic,command= lambda :insertQuantToSelection(quantListBox,quantEntry,quantList))
        submitCurrentQuant.image = submitCurrentQuantImg.buttonPic
        devider(quantFrame,2,1)
        submitCurrentQuant.grid(row=3,column=1,rowspan=2)
        finishedButtonImg = makeButtonImg(text="Check In",length=90,height=30,bg=[64,64,64])
        finishedButton = tk.Button(checkInFrame,image=finishedButtonImg.buttonPic,command=lambda : finalSubmitDS(detailBox,quantListBox,quantList,"out",techEntry,personEntry,timeDueEntry,timePunchEntry,data[1][indexToRead],data,whereEntry,indexList,quantFrame,newDetailFrame,checkInFrame))
        finishedButton.image = finishedButtonImg.buttonPic
        finishedButton.grid()
        detailBox.bind("<Double-Button-1>",lambda eff:selectItemToQuant(detailBox,detailList,quantListBox,detailBox.get(detailBox.curselection()),quantList,indexList))



        
 
def selectItemToQuant(detailBox,detailList,quantBox,userSelect,quantList,indexList):
    inQuantList = False
    iTemp = 0
    for i in range(len(quantList)):
        if userSelect == quantList[i][0]:
            inQuantList = True
    if inQuantList == False:
        quantBox.insert(tk.END,userSelect)
        for i in range(detailBox.size()):
            if detailBox.get(i) == userSelect:
                iTemp = i
        quantList.append([userSelect,0,iTemp])
        quantBox.itemconfig(tk.END, {"bg": "red"})

def insertQuantToSelection(quantBox,quantEntry,quantList):
    currentSelection = quantBox.get(quantBox.curselection())
    for i in range(quantBox.size()):
        if quantBox.get(i) == currentSelection:
            currentSelectionIndex = i
    quantBox.itemconfig(currentSelectionIndex,{"bg":"green"})

    if quantEntry.get() == "":
        quant = 0
    else:
        quant = quantEntry.get()

    quantList[currentSelectionIndex][1] = quant

# |item Number\Checked in or out\what tech\person responsible\where is it\time punch\time due\quantity|
def finalSubmitOut(detailBox,quantBox,quantList,inout,who,person,timeDue,timePunch,itemNumber,fixedData,where,indexList,quantFrame,newDetailFrame,checkInFrame):
    indexToDel = []
    #Getting indexes
    for i in range(len(quantList)):
        for j in range(detailBox.size()):
            if quantList[i][0] == detailBox.get(j):
                quantList[i][2] = indexList[j]
    quantList.sort(key=lambda x: x[2])
    for i in range(len(quantList)):
        if int(fixedData[5][quantList[i][2]][7]) < int(quantList[i][1]):
            print("TOO BIG")

        elif int(fixedData[5][quantList[i][2]][7]) == int(quantList[i][1]):
            indexToDel.append(i)
        else:
            fixedData[5][quantList[i][2]][7] = int(fixedData[5][quantList[i][2]][7]) - int(quantList[i][1])
    
    for i in range(len(indexToDel)-1,-1,-1):
        del fixedData[5][quantList[indexToDel[i]][2]]
        fixedDataSave(fixedData)
    totalQuant = 0
    for i in range(len(quantList)):
        totalQuant += int(quantList[i][1])
    newListEntry = [itemNumber,"}out{",who.get(),person.get(),where.get(),timePunch.get(),timeDue.get(),totalQuant]
    fixedData[5].append(newListEntry)
    fixedDataSave(fixedData)

    newDetailFrame.destroy()
    quantFrame.destroy()
    checkInFrame.destroy()
    setup()




def finalSubmitIn(detailBox,quantBox,quantList,inout,who,timePunch,itemNumber,fixedData,where,indexList,quantFrame,newDetailFrame,checkInFrame):
    indexToDel = []

    #Getting indexes
    #print(quantList)
    for i in range(len(quantList)):
        for j in range(detailBox.size()):
            if quantList[i][0] == detailBox.get(j):
                quantList[i][2] = indexList[j]

    #Changing info in data

    for i in range(len(quantList)):
        quantList[i][2] = int(quantList[i][2]) 
    for i in range(len(quantList)): 
        if int(fixedData[5][quantList[i][2]][7]) < int(quantList[i][1]):
            print("TOO BIG")
        elif int(fixedData[5][quantList[i][2]][7]) == int(quantList[i][1]):
            indexToDel.append(i)
        else:
            fixedData[5][quantList[i][2]][7] = int(fixedData[5][quantList[i][2]][7]) - int(quantList[i][1])

    for i in range(len(indexToDel)-1,-1,-1):
        del fixedData[5][quantList[indexToDel[i]][2]]
        fixedDataSave(fixedData)
    totalQuant = 0
    for i in range(len(quantList)):
        totalQuant += int(quantList[i][1])
    newListEntry = [itemNumber,"}in{",who.get(),"---",where.get(),timePunch.get(),"---",totalQuant]
    fixedData[5].append(newListEntry)
    fixedDataSave(fixedData)
    newDetailFrame.destroy()
    quantFrame.destroy()
    checkInFrame.destroy()
    setup()

def finalSubmitDS(detailBox,quantBox,quantList,inout,who,person,timeDue,timePunch,itemNumber,fixedData,where,indexList,quantFrame,newDetailFrame,checkInFrame):
    #Getting indexes
    for i in range(len(fixedData[4])):
        if fixedData[1][i] == itemNumber:
            index = i
            break

    if int(fixedData[4][index]) < int(quantList[0][1]):
        print("TOO BIG")
    else:
        fixedData[4][index] = int(fixedData[4][index]) - int(quantList[0][1])
    newListEntry = [itemNumber,"}out{",who.get(),person.get(),where.get(),timePunch.get(),timeDue.get(),quantList[0][1]]
    fixedData[5].append(newListEntry)
    fixedDataSave(fixedData)

    newDetailFrame.destroy()
    quantFrame.destroy()
    checkInFrame.destroy()
    setup()
    






def fixedDataSave(writeData):
    doc = open("Data.txt","w")
    writeString = ""
    for i in range(len(writeData)-1):
        for j in range(len(writeData[i])):
            writeString += str(str(writeData[i][j]).strip("\n")) + "|"
        writeString += "\n"
    writeString += "Info: |"
    for i in range(1,len(writeData[5])):
        for j in range(len(writeData[5][i])):
            writeString += str(writeData[5][i][j])
            if j != len(writeData[5][i])-1:
                writeString += "%"
        writeString += "|"
    doc.write(writeString)
    doc.close()   

def passwordCheck(event):
    if passwordEntry.get() == "":
        logInFrame.destroy()
        setup()



#Main Code
if debug == False:
    logInFrame = tk.Frame(root)
    logInFrame.grid()
    logInLabel  = tk.Label(logInFrame,text="Log In")
    logInFrame.grid(row=0,column=0)

    userNameLabel = tk.Label(logInFrame,text="Username: ")
    userNameLabel.grid(row=0,column=0)
    userNameEntry = tk.Entry(logInFrame)
    userNameEntry.grid(row=1,column=1)
    #devider(logInFrame,2,0)
    passwordLabel = tk.Label(logInFrame,text="Password")
    passwordLabel.grid(row=3,column=0)
    passwordEntry = tk.Entry(logInFrame,show="*")
    passwordEntry.grid(row=4,column=1)
    passwordEntry.bind("<Return>",passwordCheck)


    bugReportImg = makeButtonImg(text="Report Bug",length=100,height=30)
    bugReportButton = tk.Button(root,image=bugReportImg.buttonPic,relief="flat",command=bugReport)
    bugReportButton.image = bugReportImg.buttonPic
    bugReportButton.grid(sticky=tk.S,column=2,row=5)
else:
    setup()


root.mainloop()

for f in os.listdir("Assets/temp"):
    os.remove("Assets/temp/"+f)
print("Temp Deleted")
