from tkinter import *
import threading, time, os



root=Tk()
root.tk_setPalette(background='gray15', foreground='white', activeForeground="red")
button_pic_1 = PhotoImage(file="Assets/button_1.png")

#root.tk_setPalette(background='green', foreground='black',activeBackground='black', activeForeground="red")

root.resizable(False,False)
if os.name ==  "nt":
    root.iconbitmap(default='transparent.ico')
if os.name == "mac":
    pass
root.title("CPA Data Base")
quitThread = False

def openDoc():
    print("openDoc")
    doc = open("Data.txt","r")
    data = doc.readlines()
    for i in range(len(data)):
        data[i] = data[i].split("|")
        del data[i][len(data[i])-1]
    doc.close()
    return data

def addItem(itemName,itemID,itemQuant,searchResultBox,searchFrame):
    print("addItem")
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
    searchSetup(searchFrame)
    setup()

def devider(frame,row,column):
    print("devider")
    devider = Label(frame)
    devider.grid(row=row,column=column,columnspan=2)

def searchSetup(frame):
    print("searchSetup")
    def searchSelect(evt):
        print("searchSelect")
    searchResultBox = Listbox(frame,relief="flat",width=100,height=30,font='TkFixedFont',selectbackground="gray30",highlightcolor="gray15",bg="gray10",selectmode="SINGLE",bd=1)
    searchResultBox.grid(row=2,columnspan=100)
    data = openDoc()
    formatSearchBox(data,searchResultBox)
    searchResultBox.bind('<<ListboxSelect>>', searchSelect)
    return searchResultBox

def setup():
    print("Setup")
    global quitThread
    quitThread = False
    def searchThreadFunc():
        global quitThread
        data = openDoc()
        new = ""
        finalList = []
        while quitThread == False:
            print("Threading")
            time.sleep(.1)
            try:
                userSearch = str(searchBox.get())
            except:
                break
            boxString = ""
            old = new
            new = userSearch
            if new != old:
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
                        searchResultBox.insert(END,finalList[i])
                        if i % 2 == 0:
                            searchResultBox.itemconfig(i, {"bg": "gray20"})
                    finalList = []


    


    searchThread = threading.Thread(target=searchThreadFunc,args="")
    searchThread.start()
    searchFrame = Frame(root)
    searchFrame.grid(row=0,column=0)

    searchLabel = Label(searchFrame,text="Search")
    searchLabel.grid(stick=E)

    searchBox = Entry(searchFrame,width=20)
    searchBox.grid(row=0,column=1)

    searchHeaderData = ""
    data = openDoc()
    for i in range(0,len(data)-2):
        searchHeaderData += data[i][0]
        for j in range(25-len(data[i][0])):
            searchHeaderData += " "
    searchHeader = Label(searchFrame,text=searchHeaderData,font='TkFixedFont')
    searchHeader.grid(row=1,column=0,columnspan=20)
    searchResultBox = searchSetup(searchFrame)

    data = openDoc()

    #Add (right side)-----------------------------------------------

    addFrame = Frame(root)
    addFrame.grid(row=0,column=1,columnspan=3)

    addText = Label(addFrame,text="Add Item\n--------------------------------------")

    addText.grid(row=0,column=0,columnspan=5)

    nameLabel = Label(addFrame,text="Name")
    nameLabel.grid(row=1,column=0,sticky=E)
    nameBox = Entry(addFrame,width=20)
    nameBox.grid(row=1,column=2,columnspan=3)

    devider(addFrame,2,0)

    itemIdLabel = Label(addFrame,text="Item ID")
    itemIdLabel.grid(row=3,column=0,sticky=E)
    itemIDBox = Entry(addFrame,width=20)
    itemIDBox.grid(row=3,column=2,columnspan=3,)

    devider(addFrame,4,0)

    itemQuantLabel = Label(addFrame,text="Quantity")
    itemQuantLabel.grid(row=5,column=0,sticky=E)
    itemQuantBox = Entry(addFrame,width=20)
    itemQuantBox.grid(row=5,column=2,columnspan=3,)

    devider(addFrame,6,0)

    submitButton = Button(addFrame,text="Submit",command= lambda: addItem(nameBox.get(),itemIDBox.get(),itemQuantBox.get(),searchResultBox,searchFrame))
    submitButton.grid(row=7)

    searchResultBox.bind('<Double-Button-1>',lambda eff: getDetails(searchResultBox.get(searchResultBox.curselection()),searchResultBox,searchFrame,addFrame))
    buttons(searchFrame,searchResultBox,addFrame)




def buttons(frame,searchBox,addFrame):
    print("Buttons")
    deleteButton = Button(frame,text="Delete",fg="red",command=lambda :deleteInit(searchBox.get(searchBox.curselection()),searchBox,frame))
    deleteButton.grid(row=4,column=0)

    detailButton = Button(frame,text="Details",image=button_pic_1,relief="flat",height=20,width=100,command=lambda : getDetails(searchBox.get(searchBox.curselection()),searchBox,frame,addFrame))
    detailButton.grid(row=4,column=3)

#flat, groove, raised, ridge, solid, or sunken

def formatSearchBox(data,box):
    print("formatSearchBox")
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
        box.insert(END,finalList[i])
        if i % 2 == 0:
            box.itemconfig(i, {"bg": "gray17"})



def deleteInit(line,searchResultBox,searchFrame):
    print("deleteInit")
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

    uSure = Tk()
    uSure.title("Attention!")
    uSure.resizable(False,False)
    uSure.geometry("250x75+450+400")
    uSure.attributes("-topmost", True)
    textForUSure = "Are you sure you want to Delete\n" + data[0][indexToRead] + "?"
    uSureText = Label(uSure,text=textForUSure)
    uSureText.pack()
    uSureYesButton = Button(uSure,text="Yes",height=2,width=7,command= lambda :deleteing("Y",indexToRead,searchResultBox,searchFrame,uSure))
    uSureYesButton.pack(side=RIGHT)
    uSureNoButton = Button(uSure, text="No",height=2,width=7,relief="solid",command= lambda :deleteing("N",indexToRead,searchResultBox,searchFrame,uSure))
    uSureNoButton.pack(side=LEFT)

def deleteing(yOrN,indexValueToDel,searchResultBox,searchFrame,newFrame):
    print("deleting")
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
    newFrame.destroy()





def getDetails(line,searchResultBox,frame,addFrame):
    print("getDetails")
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
    def back(oldFrame):
        print("back")
        oldFrame.destroy()
        setup()
#--------------------------------------------------
    #Details template: |item Number\Checked in or out\time stamp\time due\where is it\what tech\person responsibal|

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
    detailFrame = Frame(root)
    detailFrame.grid(row=0,column=0)
    detailBox = Listbox(detailFrame,relief="solid",width=100,height=30,font='TkFixedFont',selectbackground="gray30",highlightcolor="black")
    detailBox.grid(row=2,columnspan=100)
    backButton = Button(detailFrame,text="Back",command=lambda :back(detailFrame))
    backButton.grid(row=0,column=0)
    nameString = data[0][indexToRead]

    nameLabel = Label(detailFrame,text=nameString,font=("Comic Sans MS", 20))
    nameLabel.grid(row=1,column=50-(len(nameString)//2))

    boxString = "Checked in:"
    for i in range(50-len(boxString)):
        boxString += " "
    boxString += str(data[2][indexToRead])
    detailBox.insert(END,boxString)
    detailBox.itemconfigure(0,{"bg":"gray10"})

    boxString = "Checked out:"
    for i in range(50-len(boxString)):
        boxString += " "
    boxString += str(data[3][indexToRead])
    detailBox.insert(END,boxString)

    detailBox.bind("<Double-Button-1>",lambda eff: details2(detailFrame,detailBox.get(detailBox.curselection()),indexToRead,addFrame))

    detailButton = Button(detailFrame,text="Details",height=2,width=10,command=lambda :details2(detailFrame,detailBox.get(detailBox.curselection()),indexToRead,addFrame))
    detailButton.grid(row=3,column=3,columnspan=73)
    frame.destroy()

def details2(oldFrame,line,indexToRead,addFrame):
    print("details2")
    '''
On this screen, there will be, The name of the item at the top of the screen, below there will be a set of items:
TIme stamp, time due, Where is it, person responsible, tech signed out, quantity.

#|item Number\Checked in or out\time stamp\time due\where is it\what tech\person responsible|
    '''
    def back():
        print("back")
        newDetailFrame.destroy()
        quantFrame.destroy()
        addFrame.destroy()
        try:
            checkInFrame.destroy()
        except:
            pass
            #checkOutFrame.destroy()
        setup()
    addFrame.destroy()
    oldFrame.destroy()
    newDetailFrame = Frame(root)
    newDetailFrame.grid(row=0,column=0,sticky=W)
    backButton = Button(newDetailFrame, text="Back", command=back)
    backButton.grid(row=0, column=0)

    data = openDoc()

    nameString = data[0][indexToRead]

    nameLabel = Label(newDetailFrame,text=nameString,font=("Comic Sans MS", 20))
    nameLabel.grid(row=1,column=50-(len(nameString)//2))

    returnDefaultButton = Button(newDetailFrame, text="Return to Default State", fg="red")
    returnDefaultButton.grid(row=4, column=0)
    if "Checked in" in line:
        temp = "Time Punched In"
        tempSpace = "     "
    else:
        temp = "Time Punched Out"
        tempSpace = "     "
    #TIme stamp, time due, Where is it, person responsible, tech signed out, quantity.
    #Header----------------------------------------------------
    
#21 character in each

    boxString = ""
    if "Checked in" in line:
        detailBox = Listbox(newDetailFrame, relief="solid", width=115, height=30, font='TkFixedFont',selectbackground="gray30",highlightcolor="black")
        detailBox.grid(row=3, columnspan=100)
        headerString = "Signed Out By" + "        "+"Person Responsible"+ "   "+"Where It Is"+"          "+temp+tempSpace+"Time Due"+"             "+"Quantity"
        headerLabel = Label(newDetailFrame,text=headerString,font='TkFixedFont')
        headerLabel.grid(row=2,columnspan=100,sticky=W)    

        data = openDoc()

        if len(data[5]) > 1:
            for i in range(1,len(data[5])):
                data[5][i] = data[5][i].split("%")
        defaultState = int(data[4][indexToRead])
        #Adding Default state to list
        if defaultState > 0:
            boxString = "---"+"                  "+"---"+"                  "+"---"+"                  "+"---"+"                  "+"---"+"                  "+str(defaultState)
            detailBox.insert(END,boxString)
            detailBox.itemconfig(0, {"bg": "gray10"})        
        #-----------------------------
        #Adding all detail data in data.txt to detail2 box
        # |item Number\Checked in or out\what tech\person responsible\where is it\time punch\time due\quantity|
        boxString = ""
        indexList = []
        detailList = [defaultState]
        counter = 0
        for i in range(1,len(data[5])):
            if data[5][i][0] == data[1][indexToRead] and data[5][i][1] == "in":
                indexList.append(i)
                for j in range(2,len(data[5][i])):
                    boxString += data[5][i][j]
                    for k in range(21-len(data[5][i][j])):
                        boxString += " "
                detailBox.insert(END,boxString)
                counter += 1
                print(counter)
                if counter % 2 == 0:
                    detailBox.itemconfig(counter, {"bg": "gray10"})
                detailList.append(boxString)
                boxString = ""
                print(data[5][i])
        #------------------------------
        checkInFrame = Frame(root)
        checkInFrame.grid(row=0,column=2)
        titleLabel = Label(checkInFrame,text="Check Out Item(s)")
        titleLabel.grid(row=0,column=0)
        devider(checkInFrame,1,0)

        techLabel = Label(checkInFrame,text="Tech Checking Item(s) in")
        techLabel.grid(row=2,column=0)
        techEntry = Entry(checkInFrame)
        techEntry.grid(row=3,column=0)
        devider(checkInFrame,4,0)

        personLabel = Label(checkInFrame,text="Person Responsible For Item(s)")
        personLabel.grid(row=5,column=0)
        personEntry = Entry(checkInFrame)
        personEntry.grid(row=6,column=0)
        devider(checkInFrame,7,0)

        whereLabel = Label(checkInFrame,text="Item Location")
        whereLabel.grid(row=8,column=0)
        whereEntry = Entry(checkInFrame)
        whereEntry.grid(row=9,column=0)
        devider(checkInFrame,10,0)

        timePunchLabel = Label(checkInFrame,text="Time of Action")
        timePunchLabel.grid(row=11,column=0)
        timePunchEntry = Entry(checkInFrame)
        timePunchEntry.grid(row=12,column=0)
        devider(checkInFrame,13,0)

        timeDueLabel = Label(checkInFrame,text="Time Item(s) Is Due")
        timeDueLabel.grid(row=14,column=0)
        timeDueEntry = Entry(checkInFrame)
        timeDueEntry.grid(row=15,column=0)
        devider(checkInFrame,16,0)

        #Choose Quantity Code------------------------------------------------------------------------------------------------

        quantFrame = Frame(root)
        quantFrame.grid(row=1,column=0,sticky=W,columnspan=150)

        quantListBox = Listbox(quantFrame,width=115,height=5,font='TkFixedFont')
        quantListBox.grid(row=0,column=0,rowspan=5)

        removeQuantButton = Button(quantFrame,text="Remove",fg="red")
        removeQuantButton.grid(row=6,column=0)

        quantEntryLabel = Label(quantFrame,text="Enter Quantity")
        quantEntryLabel.grid(row=0,column=1)

        quantEntry = Entry(quantFrame)
        quantEntry.grid(row=1,column=1)
        quantList = []
        submitCurrentQuant = Button(quantFrame,text="Submit Quantity",height=3,command= lambda :insertQuantToSelection(quantListBox,quantEntry,quantList))
        submitCurrentQuant.grid(row=0,column=3,rowspan=2)

        finishedButton = Button(checkInFrame,text="Check Out",height=3,command=lambda : finalSubmit(detailBox,quantListBox,quantList,"out",techEntry,personEntry,timeDueEntry,timePunchEntry,data[1][indexToRead],data,whereEntry,indexList))
        finishedButton.grid()
        detailBox.bind("<Double-Button-1>",lambda eff:selectItemToQuant(detailBox,detailList,quantListBox,detailBox.get(detailBox.curselection()),quantList,indexList))
    else:
        print("Checked out")

#Check Out Code-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#
#
        detailBox = Listbox(newDetailFrame, relief="solid", width=80, height=30, font='TkFixedFont',selectbackground="gray30",highlightcolor="black")
        detailBox.grid(row=3, columnspan=100)
        headerString = "Signed Out By" +"        "+"Where It Is"+"          "+temp+tempSpace+"Quantity"
        headerLabel = Label(newDetailFrame,text=headerString,font='TkFixedFont')
        headerLabel.grid(row=2,columnspan=100,sticky=W)
        data = openDoc()

        if len(data[5]) > 1:
            for i in range(1,len(data[5])):
                data[5][i] = data[5][i].split("%")
        defaultState = int(data[4][indexToRead])
        #Adding Default state to list
        #if defaultState > 0:
        #    boxString = "---"+"                  "+"---"+"                  "+"---"+"                  "+"---"+"                  "+"---"+"                  "+str(defaultState)
        #    detailBox.insert(END,boxString)
        #    detailBox.itemconfig(0, {"bg": "gray10"})        
        #-----------------------------
        #Adding all detail data in data.txt to detail2 box
        # |item Number\Checked in or out\what tech\person responsible\where is it\time punch\time due\quantity|
        boxString = ""
        indexList = []
        detailList = [defaultState]
        counter = 0
        for i in range(1,len(data[5])):
            if data[5][i][0] == data[1][indexToRead] and data[5][i][1] == "out":
                indexList.append(i)
                for j in range(2,len(data[5][i])):
                    boxString += data[5][i][j]
                    for k in range(21-len(data[5][i][j])):
                        boxString += " "
                detailBox.insert(END,boxString)
                counter += 1
                print(counter)
                if counter % 2 == 0:
                    detailBox.itemconfig(counter, {"bg": "gray10"})
                detailList.append(boxString)
                boxString = ""
                print(data[5][i])
        #------------------------------
        checkInFrame = Frame(root)
        checkInFrame.grid(row=0,column=2)
        titleLabel = Label(checkInFrame,text="Check In Item(s)")
        titleLabel.grid(row=0,column=0)
        devider(checkInFrame,1,0)

        techLabel = Label(checkInFrame,text="Tech Checking Item(s) In")
        techLabel.grid(row=2,column=0)
        techEntry = Entry(checkInFrame)
        techEntry.grid(row=3,column=0)
        devider(checkInFrame,4,0)


        whereLabel = Label(checkInFrame,text="Item Location")
        whereLabel.grid(row=8,column=0)
        whereEntry = Entry(checkInFrame)
        whereEntry.grid(row=9,column=0)
        devider(checkInFrame,10,0)

        timePunchLabel = Label(checkInFrame,text="Time of Action")
        timePunchLabel.grid(row=11,column=0)
        timePunchEntry = Entry(checkInFrame)
        timePunchEntry.grid(row=12,column=0)
        devider(checkInFrame,13,0)


        #Choose Quantity Code------------------------------------------------------------------------------------------------

        quantFrame = Frame(root)
        quantFrame.grid(row=1,column=0,sticky=W,columnspan=150)

        quantListBox = Listbox(quantFrame,width=80,height=5,font='TkFixedFont')
        quantListBox.grid(row=0,column=0,rowspan=5)

        removeQuantButton = Button(quantFrame,text="Remove",fg="red")
        removeQuantButton.grid(row=6,column=0)

        quantEntryLabel = Label(quantFrame,text="Enter Quantity")
        quantEntryLabel.grid(row=0,column=1)

        quantEntry = Entry(quantFrame)
        quantEntry.grid(row=1,column=1)
        quantList = []
        submitCurrentQuant = Button(quantFrame,text="Submit Quantity",height=3,command= lambda :insertQuantToSelection(quantListBox,quantEntry,quantList))
        submitCurrentQuant.grid(row=0,column=3,rowspan=2)

        finishedButton = Button(checkInFrame,text="Check Out",height=3,command=lambda : finalSubmit(detailBox,quantListBox,quantList,"out",techEntry,personEntry,timeDueEntry,timePunchEntry,data[1][indexToRead],data,whereEntry,indexList))
        finishedButton.grid()
        detailBox.bind("<Double-Button-1>",lambda eff:selectItemToQuant(detailBox,detailList,quantListBox,detailBox.get(detailBox.curselection()),quantList,indexList))








        
 
def selectItemToQuant(detailBox,detailList,quantBox,userSelect,quantList,indexList):
    inQuantList = False
    iTemp = 0
    for i in range(len(quantList)):
        if userSelect == quantList[i][0]:
            inQuantList = True
    if inQuantList == False:
        quantBox.insert(END,userSelect)
        for i in range(detailBox.size()):
            if detailBox.get(i) == userSelect:
                iTemp = i
        quantList.append([userSelect,0,iTemp])
        quantBox.itemconfig(END, {"bg": "red"})

def insertQuantToSelection(quantBox,quantEntry,quantList):
    currentSelection = quantBox.get(quantBox.curselection())
    for i in range(quantBox.size()):
        if quantBox.get(i) == currentSelection:
            currentSelectionIndex = i
    print(currentSelectionIndex)
    quantBox.itemconfig(currentSelectionIndex,{"bg":"green"})

    if quantEntry.get() == "":
        quant = 0
    else:
        quant = quantEntry.get()

    quantList[currentSelectionIndex][1] = quant
    print(quantList)

# |item Number\Checked in or out\what tech\person responsible\where is it\time punch\time due\quantity|
def finalSubmit(detailBox,quantBox,quantList,inout,who,person,timeDue,timePunch,itemNumber,fixedData,where,indexList):
    data = openDoc()
    print(itemNumber)
    #Getting indexes
    #print(quantList)
    print(indexList)
    for i in range(len(quantList)):
        for j in range(1,detailBox.size()):
            if quantList[i][0] == detailBox.get(j):
                print(fixedData[5])
                print(quantList)
                print(fixedData[5][1])
                print("Yes")
                print("I ",i)
                print("J ",j)
                quantList[i][2] = indexList[j-1]

    print(quantList)
    print(indexList)
    print(fixedData[5][1])
    #Changing info in data
    for i in range(len(quantList)):
        if int(fixedData[5][quantList[i][2]][7]) < int(quantList[i][1]):
            print("TOO BIG")
        elif int(fixedData[5][quantList[i][2]][7]) == int(quantList[i][1]):
            print("Equal")
            del fixedData[5][quantList[i][2]]
            newListEntry = [fixedData[5][quantList[i][2]][0],"in",who.get(),person.get(),where.get(),timePunch.get(),timeDue.get(),int(quantList[i][1])]
            fixedData[5].append(newListEntry)
            fixedDataSave(fixedData)
        else:
            print("Less")
            newListEntry = [fixedData[5][quantList[i][2]][0],"in",who.get(),person.get(),where.get(),timePunch.get(),timeDue.get(),int(quantList[i][1])]
            #fixedData[5][quantList[i][2]][1] = "in" #CHANGE THIS TO OUT LATER!
            #fixedData[5][quantList[i][2]][2] = who.get()
            #fixedData[5][quantList[i][2]][3] = person.get()
            #fixedData[5][quantList[i][2]][4] = where.get()
            #fixedData[5][quantList[i][2]][5] = timePunch.get() 
            #fixedData[5][quantList[i][2]][6] = timeDue.get()
            fixedData[5][quantList[i][2]][7] = int(fixedData[5][quantList[i][2]][7]) - int(quantList[i][1])
            fixedData[5].append(newListEntry)
            fixedDataSave(fixedData)


def fixedDataSave(writeData):
    print("fixedDataSave")
    doc = open("Data.txt","w")
    writeString = ""
    for i in range(len(writeData)-1):
        for j in range(len(writeData[i])):
            writeString += writeData[i][j].strip("\n") + "|"
        writeString += "\n"
    writeString += "Info: |"
    for i in range(1,len(writeData[5])):
        for j in range(len(writeData[5][i])):
            writeString += str(writeData[5][i][j])
            if j != len(writeData[5][i])-1:
                writeString += "%"
        writeString += "|"
    print(writeString)
    doc.write(writeString)
    doc.close()   






#Main Code

setup()








root.mainloop()

