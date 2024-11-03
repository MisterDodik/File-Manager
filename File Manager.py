import os
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
clearConsole()

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image,UnidentifiedImageError
from tkinter import filedialog
from tkinter import messagebox
import shutil
import json 

windows=Tk()

bannedsymbols="!@#$%^&*()_+-=[]\\|';:/.,<>?"
selected_mainfolder=None
selected_subfolder=None


def subfoldertodelet(rootdir):
    global todelete
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        
        if os.path.isdir(d):
            todelete.append(d)
            subfoldertodelet(d)
    return todelete



todelete=[]
def delete_selected_mainfolder():
    global selected_mainfolder
    global next_column_main
    global next_column_sub
    
    global selected_subfolder
    global globalpath

    global file_photo_mapping

    global subfolders_dict
    with open(motherPath+'\\file_photo_mapping.json', 'r') as f:
        file_photo_mapping = json.load(f)

    if selected_mainfolder and selected_subfolder is None:
        path= "PATH: D:\\File Manager\\"
        pathCanvas.itemconfigure(PathText, text=path)

        if selected_mainfolder.cget("text") in file_photo_mapping:
            del file_photo_mapping[selected_mainfolder.cget("text")]
        for i in (subfoldertodelet("D:\\File Manager\\"+selected_mainfolder.cget("text"))):
            if os.path.basename(i) in file_photo_mapping:
                del file_photo_mapping[os.path.basename(i)]


        with open(motherPath+'\\file_photo_mapping.json', 'w') as f:
            json.dump(file_photo_mapping, f)

        for i in subfolders_dict.values():
            for j in i:
                j.destroy()
        shutil.rmtree(motherPath+"\\"+selected_mainfolder.cget("text"))
        selected_mainfolder.grid_forget()
        main_folders_list.remove(selected_mainfolder)
        
        for index, button in enumerate(main_folders_list):
            button.grid(row=1, column=index+1, padx=15, pady=15)
        if len(main_folders_list) == 0:
            next_column_main = 1
        else:
            next_column_main = main_folders_list[-1].grid_info()['column'] + 1
        selected_mainfolder.destroy()
        selected_mainfolder = None

    if selected_subfolder:
        try:     
            row=selected_subfolder.grid_info()["row"]
            selected_subfolder.grid_forget()
            
            names_list = subfolders_dict.get(row, [])

            # Remove the element from the list if it exists
            if selected_subfolder in names_list:
                names_list.remove(selected_subfolder)

            # Update the dictionary with the modified list of names
            subfolders_dict[row] = names_list

            for index, button in enumerate(subfolders_dict.get(row, [])):
                button.grid(row=row, column=index+1, padx=15, pady=15)
            
            if selected_subfolder.cget("text") in file_photo_mapping:
                del file_photo_mapping[selected_subfolder.cget("text")]
                
            if os.path.isdir(globalpath):
                for i in (subfoldertodelet(globalpath)):
                    if os.path.basename(i) in file_photo_mapping:
                        del file_photo_mapping[os.path.basename(i)]
            with open(motherPath+'\\file_photo_mapping.json', 'w') as f:
                json.dump(file_photo_mapping, f)
            
            
            #DA UKLONI SVE SPAWNOWANE SUBFOLDERE
            for i, j in subfolders_dict.items():
                if i>row:
                    for x in j:
                        x.grid_forget()
                        x.destroy()
            
            if os.path.isdir(globalpath):
                shutil.rmtree(globalpath)     
            elif os.path.isfile(globalpath):
                os.remove(globalpath)

            selected_subfolder.destroy()
            selected_subfolder=None
        
        except Exception as e:
            pass
    hierarchy()


changeiconFrame = None
def exitchangeiconFrameFunc():
    global changeiconFrame
    if changeiconFrame:
        changeiconFrame.destroy()
        changeiconFrame = None


def change_icon_func(key):
    global file_photo_mapping
    global selectedimgpathforadd
    with open(motherPath+'\\file_photo_mapping.json', 'r') as f:
        file_photo_mapping = json.load(f)
    file_photo_mapping[key]=selectedimgpathforadd
    
    photo=ImageTk.PhotoImage(Image.open(file_photo_mapping[key]).resize((100, 100)))

    if selected_mainfolder and selected_subfolder is None:
        selected_mainfolder.photo = photo                  
        selected_mainfolder.config(image=photo) 
    elif selected_subfolder:
        selected_subfolder.photo = photo                  
        selected_subfolder.config(image=photo) 

    with open(motherPath+'\\file_photo_mapping.json', 'w') as f:
        json.dump(file_photo_mapping, f)
    exitchangeiconFrameFunc()
    


def change_iconFrame():
    global changeiconFrame
    global img
    global selectedimgpathforadd
    
    global file_photo_mapping
    with open(motherPath+'\\file_photo_mapping.json', 'r') as f:
        file_photo_mapping = json.load(f)
    
    key=None
    canChange=None
    if selected_mainfolder and selected_subfolder is None:
        key=selected_mainfolder.cget("text")
        canChange=True
    elif selected_subfolder:
        key=selected_subfolder.cget("text")
        if key not in file_photo_mapping.keys():
            canChange=False
        else:
            canChange=True
    if (changeiconFrame is None or not changeiconFrame.winfo_exists()) and (selected_subfolder is not None or selected_mainfolder is not None) and canChange==True:
        changeiconFrame= Frame(windows, width=500, height=300)
        changeiconFrame.place(relx=0.3, rely=0.3, )

        
        photo=ImageTk.PhotoImage(Image.open(file_photo_mapping[key]).resize((100, 100)))
        selectedImg = Label(changeiconFrame, image=photo)
        selectedImg.place(relx=0.25, rely=0.52, anchor=CENTER)
        
        selectedImg.photo = photo                  
        selectedImg.config(image=photo) 
    
    
    
        exitchangeiconFrame=Button(changeiconFrame, command=exitchangeiconFrameFunc,borderwidth=0, highlightthickness=0,image=normal_exitButtonImg )
        exitchangeiconFrame.place(relx=1,rely=0,x=-20,y=15,  anchor=CENTER)
        exitchangeiconFrame.bind('<Enter>', lambda event:exitchangeiconFrame.config(image=hover_exitButtonImg))
        exitchangeiconFrame.bind('<Leave>', lambda event:exitchangeiconFrame.config(image=normal_exitButtonImg))
        Label(changeiconFrame, text="Change Icon",font=("Arial",20, "bold")).place(relx=0.5, rely=0.08, anchor=CENTER)
        select_image = Button(changeiconFrame, text="Select an image", font=("Arial", 15, "normal"),command=lambda:[on_select(selectedImg),])
        select_image.place(relx=0.65,rely=0.45,anchor=CENTER,relwidth=0.4, relheight=0.1)
        

        confirm_button = Button(changeiconFrame, background="#479ef5",text="Confirm", font=("Arial", 15, "normal"),
                                command=lambda:
                                [change_icon_func(key)])
        
        confirm_button.place(relx=0.65,rely=0.63,anchor=CENTER,relwidth=0.4, relheight=0.1)


#TOOLBAR FRAME
tools=Frame(windows, background="#f0f0f0" )
tools.pack(side=TOP, anchor="nw", fill=X)
Button(tools, text="CHANGE ICON", background="#8bc34a", width=20, font=("Arial", 12, "bold"), command=change_iconFrame).pack(side=LEFT)
Button(tools, text="DELETE FOLDER", background="#8bc34a", width=20, font=("Arial", 12, "bold"), command=delete_selected_mainfolder).pack(side=LEFT)







#PATH ADDRESS FRAME
pathAddress=Frame(windows, )
pathAddress.pack(fill=X)
pathCanvas=Canvas(pathAddress, background="#dedede", height=50)
path="PATH: D:\\File Manager\\"
PathText=pathCanvas.create_text(10,15, text="PATH: ", font=('Helvetica 15 bold'), anchor=NW)
pathCanvas.pack(fill=X)





def changePath(text):
    if canCreate==True:
        pathCanvas.itemconfigure(PathText, text="PATH:")
        global path
        path= "PATH: D:\\File Manager\\"+text
        pathCanvas.itemconfigure(PathText, text=path)






#ZA RESIZABLE PANE
resizablePane=PanedWindow(windows,sashwidth = 7, bg = "black", bd = 0)
resizablePane.pack(side=LEFT, expand=1, fill=BOTH, anchor=W)








#HIERARCHY FRAME (LEFT)
hierarchyFrame=Frame(windows, )
hierarchyCanvas=Canvas(resizablePane,background="#caffff", width=150)
resizablePane.add(hierarchyCanvas, width=150)





folders=[]

tree = ttk.Treeview(hierarchyCanvas, selectmode=BROWSE)
tree.tag_configure("fontTag", font=("Arial", 15, "normal"))
style = ttk.Style()
style.configure("Treeview", padding=(10, 10),rowheight=40)


def getFolders(motherPath):
    global folders
    folders=[]
    for dirpath, dirnames, filenames in os.walk(motherPath):
        for dirname in dirnames:
            folders.append(os.path.join(dirpath, dirname))
    
        for filename in filenames:
            # Check if file does not end with ".jpg", ".png", or ".jpeg" extensions
            if not filename.lower().endswith((".jpg", ".png", ".jpeg",".json")):
                folders.append(os.path.join(dirpath, filename))

def hierarchy():
    global tree
    global folders
    for item in tree.get_children():
        tree.delete(item)
    getFolders(motherPath+"\\")

    #Insert a folder item
    for folder in folders:
        if folder.count("\\")==2:
            tree.insert('', iid=folder[folder.rfind("\\")+1:], 
                        index="end", 
                        text=folder[folder.rfind("\\")+1:],tags=("fontTag"), )   
        else:
            tree.insert(folder[the_last_nth(folder,"\\",2)+1:folder.rfind("\\")], 
                        iid=folder[folder.rfind("\\")+1:], 
                        index="end", 
                        text=folder[folder.rfind("\\")+1:],tags=("fontTag"),)



paths=[]
def getpaths(event):
    global paths
    paths = []
    try:
        paths.append(tree.selection()[0])
    except IndexError:
        return 
    item_iid = tree.selection()[0]
    parent_iid = tree.parent(item_iid)
    
    while True:   
        paths.append(parent_iid)
        parent_iid=tree.parent(parent_iid)
        if not parent_iid:
            break
    
    hierarchyOpen=motherPath+"\\"+"\\".join(paths[::-1])
    if os.path.isfile(hierarchyOpen):
    # Path corresponds to a file
        try:
            os.startfile(hierarchyOpen)
                
        except FileNotFoundError:
            print(f"File not found at path: {hierarchyOpen}")
        except Exception as e:
            print(f"An error occurred while opening the file: {e}")
    elif os.path.isdir(hierarchyOpen):
        # Path corresponds to a folder
        # Perform operations for opening a folder here
        os.startfile(hierarchyOpen)
        print(f"Path corresponds to a folder: {hierarchyOpen}")
    else:
        print(f"Path does not correspond to a valid file or folder: {hierarchyOpen}")

        
tree.bind("<Double-1>", getpaths)

# Pack the Treeview widget
tree.pack(fill=BOTH, expand=True)









#MAIN FRAME ZA FOLDERE, SUBFOLDERE...
defaultMainFrame=Frame(resizablePane,background="#f5f5f5",)
resizablePane.add(defaultMainFrame, )
FMcan=Canvas(defaultMainFrame, background="#e3fafa" )
FMcan.place(relx=0, rely=0, relwidth=1, relheight=1)


ver_scrollbar = Scrollbar(defaultMainFrame, orient="vertical", command=FMcan.yview)
ver_scrollbar.place(relx=1, x=-15, relheight=0.5)
FMcan.configure(yscrollcommand=ver_scrollbar.set)

hor_scrollbar = Scrollbar(defaultMainFrame, orient="horizontal", command=FMcan.xview)
hor_scrollbar.place(relx=0, rely=1, y=-15, relwidth=0.5)
FMcan.configure(xscrollcommand=hor_scrollbar.set)

FMcan.bind("<Configure>", lambda e: FMcan.configure(scrollregion=FMcan.bbox("all")))

mainframeFM = Frame(FMcan, background="#e3fafa")
mainframeFM.place(relx=0, rely=0, relheight=1, relwidth=1)

FMcan.create_window((0,0), window=mainframeFM, width=1280, height=720, anchor='nw') 
FMcan.configure(scrollregion=(0, 0, mainframeFM.winfo_width(), mainframeFM.winfo_height()))
def skrolregion(x,y):
    FMcan.create_window((0,0), window=mainframeFM, width=x, height=y, anchor='nw') 
    FMcan.configure(scrollregion=(0, 0, x, y))





#WHERE EVERYTHING IS STORED
motherPath="D:\\File Manager"

file_photo_mapping={}
if not os.path.exists(motherPath):
    os.makedirs(motherPath)  
if not os.path.exists(motherPath+"\\file_photo_mapping.json"):
    with open(motherPath+"\\file_photo_mapping.json", 'w') as f:
        json.dump({}, f)
    
with open(motherPath+"\\file_photo_mapping.json", 'r') as f:
    file_photo_mapping = json.load(f) 







def change_json(folderName, selectedimgpathforadd, button, default):
    global file_photo_mapping
    if canCreate==True:
        if len(selectedimgpathforadd)>0:
            file_photo_mapping[folderName] = selectedimgpathforadd
        else:
            file_photo_mapping[folderName] = default
        with open(motherPath+"\\file_photo_mapping.json", 'w') as f:
            json.dump(file_photo_mapping, f)
        if button==1:
            createmainfolders(folderName)



#open path on double click
def on_double_click(event):
    try:
        os.startfile(globalpath)
    except Exception as e:
            pass 



#FOR CREATING MAIN FOLDERS  
lenght_of_mainframe=mainframeFM.winfo_width()                       #changing scrollregion

globalpath=""

main_folders_list=[]
def on_mainfolder_click(event):                                     #SELECT FOLDER
    global selected_mainfolder
    global globalpath
    global subfolders_list
    global selected_subfolder
    selected_mainfolder= event.widget
    # Change background color of clicked button
    event.widget.config(bg='#aebad1')
    path= "PATH: D:\\File Manager\\"+event.widget.cget("text")
    pathCanvas.itemconfigure(PathText, text=path)
    for i in subfolders_list:
        i.destroy()
    subfolders_list.clear()
    globalpath=motherPath+"\\"+event.widget.cget("text")

    selected_subfolder=None
    updateSubDict()
    create_subfolders(path.strip()[6:], None)
    
    # Reset background color of other buttons
    for folder in main_folders_list:
        if folder!= event.widget and folder is not None:
           folder.config(bg='SystemButtonFace')


def createmainfolders(path):
    global file_photo_mapping
    global globalpath
    with open(motherPath+"\\file_photo_mapping.json", 'r') as f:
        file_photo_mapping = json.load(f)  
    image=file_photo_mapping[path]
    creation(image, path)



next_column_main = 1  
def creation(path, filename):   
    global lenght_of_mainframe      
    global main_folders_list  
    global next_column_main
    photo = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
    folder = Button(mainframeFM, image=photo, text=filename, compound=TOP, font=("Arial", 10, "normal"))
    folder.image = photo # Store a reference to the photo to prevent it from being garbage collected

    main_folders_list.append(folder)                    #SELECT FOLDER

    folder.grid(row=1, column=next_column_main,padx=15, pady=15)
    folder.grid_propagate(False)
    folder.configure(width=100)
    
    lenght_of_mainframe+=130
    next_column_main+=1
    folder.bind("<Double-Button-1>", on_double_click)
    folder.bind("<Button-1>", on_mainfolder_click)
    for folder in main_folders_list:                    #SVAKI KAD SE SPAWN, OSTALI DOBIJU NORMALNU BOJU
        folder.config(bg='SystemButtonFace')            
    folder.config(bg='#aebad1')                         #NEWLY CREATED FOLDER IS SELECTED BY DEFAULT

    if lenght_of_mainframe>1280:
        skrolregion(lenght_of_mainframe+200,mainframeFM.winfo_height())
    FMcan.update()




#STARTUP MAIN LOADING
def startup_loading():
    global file_photo_mapping
    global subfolders_dict
    with open(motherPath+"\\file_photo_mapping.json", 'r') as f:
        file_photo_mapping = json.load(f)  

    d=[os.path.join(motherPath, file) for file in os.listdir(motherPath)]
    for i, j in file_photo_mapping.items():    
        if motherPath+"\\"+i in d:
            creation(j, i)

    for folder in main_folders_list:                            #ALL STARTUP LOADED FOLDERS
        folder.bind("<Button-1>", on_mainfolder_click)
startup_loading()



#DESELECT EVERYTHING WHEN CLICKED ON MAINFRAME
def deselect_mainfolder(event):
    global selected_mainfolder
    global selected_subfolder
    if selected_mainfolder:
        selected_mainfolder.config(bg='SystemButtonFace')
        selected_mainfolder = None
        path= "PATH: D:\\File Manager\\"
        pathCanvas.itemconfigure(PathText, text=path)
        selected_subfolder=None
        for i in subfolders_list:
            i.destroy()
        subfolders_list.clear()
mainframeFM.bind("<Button-1>", deselect_mainfolder)




#FOR REMOVING SEGMENTS IF SUBFOLDERS FROM DIFFERENT ROWS ARE SELECTED
def the_last_nth(string, substring, number):
    found=0
    index=0
    for i in string[::-1]:
        index+=1
        if i==substring:
            found+=1
        if found==number:
            return len(string)-index



def onsubfolder_click(event):
    global selected_subfolder
    global globalpath
    global globalpath
    global subfolders_dict

    selected_subfolder = event.widget

    # Get the subfolder name
    subfolder_name = event.widget.cget("text")
    if globalpath[globalpath.rfind("\\")+1:] in [button["text"] for button in subfolders_dict.get(event.widget.grid_info()["row"], [])]:
        globalpath=globalpath[:globalpath.rfind("\\")+1]+subfolder_name
    else:
        if not globalpath.endswith(subfolder_name):
            globalpath=globalpath+"\\"+subfolder_name
    rowclicked=event.widget.grid_info()["row"]
    if rowclicked<globalpath.count("\\"):
        segments_remove=globalpath.count("\\")-rowclicked+1
        globalpath=globalpath[:the_last_nth(globalpath,"\\",segments_remove)]+"\\"+subfolder_name


    # Update the path text
    path = "PATH: " + globalpath
    pathCanvas.itemconfigure(PathText, text=path)

    # Reset background color of other buttons
    for folder in subfolders_list:
        if folder != event.widget and folder is not None and folder.winfo_exists():
            folder.config(bg='SystemButtonFace')

    updateSubDict()
    create_subfolders(globalpath, None)


    folders = globalpath.split(os.path.sep)
    subfolder_names = folders[3:]

    #SELECT ALL FROM PATH
    for folder in [button for buttonsub in subfolders_dict.values() for button in buttonsub]:
        # Get the text of the button
        button_text = folder.cget("text")
        # Check if the button text matches with any subfolder name
        if button_text in subfolder_names:
            # Set the button color to blue (selected)
            folder.config(bg="#aebad1")
        else:
            # Set the button color to normal (deselected)
            folder.configure(bg="SystemButtonFace")


def updateSubDict():
    global globalpath
    global subfolders_dict
    if globalpath.count("\\") + 1 in subfolders_dict:
        for key, value in subfolders_dict.items():
            if key >= globalpath.count("\\") + 1:
                for i in value:
                    if i.winfo_exists():  # Check if widget still exists
                        i.destroy()
        new_dict = {key: value for key, value in subfolders_dict.items() if key <globalpath.count("\\")+1}
        subfolders_dict=new_dict




subfolders_list=[]
subfolders_dict={}
next_column_sub=1
def create_subfolders(rootdir, filename):
    global globalpath
    global next_column_sub
    next_column_sub=1
    x=globalpath.count("\\")
    
    global file_photo_mapping
    with open(motherPath+"\\file_photo_mapping.json", 'r') as f:
        file_photo_mapping = json.load(f)  

    if os.path.isdir(rootdir):
        for file in (os.listdir(rootdir)):
            d = os.path.join(rootdir, file)
            global lenght_of_mainframe      
            global subfolders_list  
            try:
                photo = ImageTk.PhotoImage(Image.open(file_photo_mapping[os.path.basename(d)]).resize((100, 100)))
            except Exception:
                photo = ImageTk.PhotoImage(Image.open(os.path.dirname(__file__)+"\\Images\\SUBFOLDER ICON.png").resize((100, 100)))
            folder = Button(mainframeFM, image=photo, text=os.path.basename(d), compound=TOP, font=("Arial", 10, "normal"),wraplength=100)
            folder.image = photo # Store a reference to the photo to prevent it from being garbage collected

            folder.grid(row=x+1, column=next_column_sub,padx=15, pady=15)
            folder.grid_propagate(False)
            folder.configure(width=100)
            lenght_of_mainframe+=130

            next_column_sub+=1
            if x+1 in subfolders_dict:
                subfolders_dict[x+1].append(folder)
            else:
                subfolders_dict[x+1] = [folder]
            subfolders_list.append(folder)                    #SELECT FOLDER
            folder.bind("<Double-Button-1>", on_double_click)
            folder.bind("<Button-1>", onsubfolder_click)
            if lenght_of_mainframe>1280:
                skrolregion(lenght_of_mainframe+200,mainframeFM.winfo_height())
            FMcan.update()








#"ADD NEW" BUTTON
addButtonImg = (Image.open(os.path.dirname(__file__)+"\\Images\\addnew.png"))
addButtonImg=addButtonImg.resize((70, 70))
addButtonImg=ImageTk.PhotoImage(addButtonImg)
normal_exitButtonImg=ImageTk.PhotoImage(Image.open(os.path.dirname(__file__)+"\\Images\\exit button1.png"))
hover_exitButtonImg=ImageTk.PhotoImage(Image.open(os.path.dirname(__file__)+"\\Images\\exit button2.png"))

newFoldericon=ImageTk.PhotoImage((Image.open(os.path.dirname(__file__)+"\\Images\\FOLDER ICON.png")).resize((100, 100)))
newSubFoldericon=ImageTk.PhotoImage((Image.open(os.path.dirname(__file__)+"\\Images\\SUBFOLDER ICON.png")).resize((100, 100)))
newFileicon=ImageTk.PhotoImage((Image.open(os.path.dirname(__file__)+"\\Images\\FILE ICON.png")).resize((100, 100)))





#add new entry boxes, icon picker
addCertainFrame = None
def exitAddCertainFrameFunc():
    global addCertainFrame
    if addCertainFrame:
        addCertainFrame.destroy()
        addCertainFrame = None


#TO CREATE A NEW MAIN FOLDER
def addmainFolder(path):
    if canCreate==True:
        path="D:\\File Manager\\"+path
        if not os.path.exists(path):
            os.makedirs(path) 
            hierarchy()




def addsubFolder(path,):
    global selected_dir
    global globalpath
    if canCreate==True:
        path=globalpath+"\\"+path
        if selected_dir=="":      
            if not os.path.exists(path):
                os.makedirs(path) 
        else:
            src = selected_dir
            dst = path

            shutil.copytree(src, dst, dirs_exist_ok=False)
        hierarchy()



extensionChosen = None
#PANEL AFTER ADD FOLDER, SUBFOLDER OR FILE GETS PRESSED
def addCertain_Panel(button):
    global addCertainFrame
    if addCertainFrame is None or not addCertainFrame.winfo_exists():
        addCertainFrame= Frame(windows, width=500, height=300)
        addCertainFrame.place(relx=0.3, rely=0.3, )

    exitAddCertainFrame=Button(addCertainFrame, command=exitAddCertainFrameFunc,borderwidth=0, highlightthickness=0,image=normal_exitButtonImg )
    exitAddCertainFrame.place(relx=1,rely=0,x=-20,y=15,  anchor=CENTER)
    exitAddCertainFrame.bind('<Enter>', lambda event:exitAddCertainFrame.config(image=hover_exitButtonImg))
    exitAddCertainFrame.bind('<Leave>', lambda event:exitAddCertainFrame.config(image=normal_exitButtonImg))
    panelName=Label(addCertainFrame, text="Add New",font=("Arial",20, "bold")).place(relx=0.5, rely=0.08, anchor=CENTER)

    

    #NEW FILE NAME AND os.path.dirname(__file__)++
    filename= Entry(addCertainFrame,font=("Arial", 15, "normal") )
    filename.insert(END, "Enter a file name")
    filename.bind("<FocusIn>", lambda event: filename.delete(0, END) if filename.get() == "Enter a file name" else None)
    filename.place(relx=0.5,rely=0.3,anchor=CENTER,relwidth=0.7, relheight=0.1)
    if button==1:
        selectedImg = Label(addCertainFrame, image=newFoldericon)
        addingMainFolderSystem(filename,selectedImg,)
        y=0.6
    elif button==2:
        selectedImg = Label(addCertainFrame, image=newSubFoldericon)
        if len(filename.get())>14 and filename.get() != "Enter a file name":
            messagebox.showerror("Error", "Name too long")
        else:
            addingSubfolderFolderSystem(filename,selectedImg,)
        y=0.70
    elif button==3:
        def on_option_selected(*args):
            global extensionChosen
            extensionChosen = clicked.get()

        clicked = StringVar()
        drop = OptionMenu(addCertainFrame, clicked, *files_extensions, command=on_option_selected)
        drop.place(relx=0.82, rely=0.3, anchor=CENTER)

        selectedImg = Label(addCertainFrame, image=newFileicon)
        addingFilesSystem(filename, selectedImg)
        y=0.70

    selectedImg.place(relx=0.25, rely=y, anchor=CENTER)
       



#OVE DVIJE SU UNIVERSALNE ZA DODAVANJE SVIH
def on_select(selectedImg):
    try:
        global img
        global selectedimgpathforadd
        file_path = filedialog.askopenfilename()
        selectedimgpathforadd=file_path

        photo = ImageTk.PhotoImage(Image.open(file_path).resize((100, 100)))
        selectedImg.photo = photo                   # Store a reference to the photo to prevent it from being garbage collected
        selectedImg.config(image=photo)            
        img=photo
    except(AttributeError):
        pass
    except(UnidentifiedImageError):
        messagebox.showerror("Error", "Please input jpg/jpeg or png file!")


def getFolderName(filename):
    global folderName
    global canCreate
    global file_photo_mapping
    with open(motherPath+"\\file_photo_mapping.json", 'r') as f:
        file_photo_mapping = json.load(f)

    for i in filename.get():
        if i in bannedsymbols:
            messagebox.showerror("Error", "Please don't use special characters!")
            canCreate=False
    if len(filename.get())==0:
        messagebox.showerror("Error", "Please enter a valid name!")
        canCreate=False
    elif filename.get()=="Enter a file name":
        messagebox.showerror("Error", "Please enter a valid name!")
        canCreate=False
    elif len(filename.get())>15:
        messagebox.showerror("Error", "Name is too long!")
        canCreate=False
    elif filename.get() in file_photo_mapping:
        messagebox.showerror("Error", "Name already exists!")
        canCreate=False
    else:
        folderName=filename.get()
        canCreate=True




#KONKRETNO ZA MAIN FOLDERE
def addingMainFolderSystem(filename,selectedImg):    
    global img                  #ovo 3 je kad se pravi folder, da uzme sliku i njen path
    img=newFoldericon                   
    global selectedimgpathforadd

    selectedimgpathforadd=os.path.dirname(__file__)+"\\Images\\FOLDER ICON.png"           #path slike da sacuva da moze zapisati
    select_image = Button(addCertainFrame, text="Select an image", font=("Arial", 15, "normal"),command=lambda:[on_select(selectedImg),])
    select_image.place(relx=0.65,rely=0.6,anchor=CENTER,relwidth=0.4, relheight=0.1)
    
    confirm_button = Button(addCertainFrame, background="#479ef5",text="Confirm", font=("Arial", 15, "normal"),
                            command=lambda:
                            [getFolderName(filename),
                             changePath(filename.get()),
                             addmainFolder(filename.get()),
                             change_json(filename.get(),selectedimgpathforadd, 1, os.path.dirname(__file__)+"\\Images\\FOLDER ICON.png"),
                             exitAddCertainFrameFunc(), 
                             exitAddNewFrameFunc(),])
    
    confirm_button.place(relx=0.65,rely=0.78,anchor=CENTER,relwidth=0.4, relheight=0.1)




selected_dir=""
#KONKRETNO ZA SUBFOLDERE
def addingSubfolderFolderSystem(filename,selectedImg):    
    global img                  #ovo 3 je kad se pravi folder, da uzme sliku i njen path
    img=newFoldericon                   
    global selectedimgpathforadd
    selectedimgpathforadd=os.path.dirname(__file__)+"\\Images\\SUBFOLDER ICON.png"           #path slike da sacuva da moze zapisati
    select_image = Button(addCertainFrame, text="Select an image", font=("Arial", 15, "normal"),command=lambda:[on_select(selectedImg),])
    select_image.place(relx=0.65,rely=0.6,anchor=CENTER,relwidth=0.4, relheight=0.1)

    #DA SE DOBIJE DIRECTORY EXISTING FOLDERA
    def askexistingDir():
        global selected_dir
        selected_dir=filedialog.askdirectory()
    global newSubFoldericon
    addExisting=Button(addCertainFrame, text="Add existing", font=("Arial", 15, "normal"),command=lambda:[askexistingDir()])
    addExisting.place(relx=0.5,rely=0.425,anchor=CENTER,relwidth=0.7, relheight=0.1)

    confirm_button = Button(addCertainFrame, background="#479ef5",text="Confirm", font=("Arial", 15, "normal"),
                                            command=lambda:[getFolderName(filename),
                                                            addsubFolder(filename.get(),),
                                                            change_json(filename.get(),selectedimgpathforadd, 2, os.path.dirname(__file__)+"\\Images\\SUBFOLDER ICON.png"),
                                                            exitAddCertainFrameFunc(), 
                                                            exitAddNewFrameFunc(),])
    confirm_button.place(relx=0.65,rely=0.78,anchor=CENTER,relwidth=0.4, relheight=0.1)
    


 


#ADDING FILES
chosenFilepath=""
lastPartofthechosenfilepath=""
files_extensions=[".txt", ".xls", ".docx"]

def addingFilesSystem(filename, selectedImg):
    global img                  #ovo 3 je kad se pravi folder, da uzme sliku i njen path
    img=newFileicon                   
    global selectedimgpathforadd
    global extensionChosen
    
    selectedimgpathforadd=os.path.dirname(__file__)+"\\Images\\FILE ICON.png"           #path slike da sacuva da moze zapisati
    select_image = Button(addCertainFrame, text="Select an image", font=("Arial", 15, "normal"),command=lambda:[on_select(selectedImg),])
    select_image.place(relx=0.65,rely=0.6,anchor=CENTER,relwidth=0.4, relheight=0.1)

    
    #DA SE DOBIJE DIRECTORY EXISTING FOLDERA
    def choose_file():
        global chosenFilepath
        chosenFilepath = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), 
                                                        ("Word documents", "*.docx"), 
                                                        ("Excel files", "*.xlsx"), 
                                                        ("JPG os.path.dirname(__file__)++", "*.jpg"),
                                                        ("JPEG os.path.dirname(__file__)++", "*.jpeg"),
                                                        ("PNG os.path.dirname(__file__)++", "*.png")))
        global lastPartofthechosenfilepath
        lastPartofthechosenfilepath=(os.path.basename(chosenFilepath))   
       
    addExisting=Button(addCertainFrame, text="Add existing", font=("Arial", 15, "normal"),command=lambda:[choose_file()])
    addExisting.place(relx=0.5,rely=0.425,anchor=CENTER,relwidth=0.7, relheight=0.1)

    confirm_button = Button(addCertainFrame, background="#479ef5",text="Confirm", font=("Arial", 15, "normal"),
                                            command=lambda:[exitAddCertainFrameFunc(), 
                                                            exitAddNewFrameFunc(),
                                                            addFile(None,True),
                                                            change_json(lastPartofthechosenfilepath,selectedimgpathforadd, 3, os.path.dirname(__file__)+"\\Images\\FILE ICON.png"),
                                                            ] 
                                                            if len(chosenFilepath)!=0 else 
                                                            [
                                                            getFolderName(filename),
                                                            addFile(filename.get()+extensionChosen,False),
                                                            change_json(filename.get()+extensionChosen,selectedimgpathforadd, 3, os.path.dirname(__file__)+"\\Images\\FILE ICON.png"),
                                                            exitAddCertainFrameFunc(), 
                                                            exitAddNewFrameFunc(),                                                          
                                                            ])
    confirm_button.place(relx=0.65,rely=0.78,anchor=CENTER,relwidth=0.4, relheight=0.1)


def addFile(path,isExistingFile):
    global globalpath
    if isExistingFile==False:
        if canCreate==True:   
            path=globalpath+"\\"+path  
            if not os.path.exists(path):
                with open(path, "w") as file:
                    pass
    else:   
        path=globalpath
        src = chosenFilepath
        dst = path

        shutil.copy(src, dst)

    hierarchy()    


#add new folder, subfolder, file frame 
def whichButtClicked(buttonRole):
    if buttonRole!=1:
        #if selected_subfolder is None or len(contents) == 0 or selected_mainfolder is None :
        if globalpath.count("\\")<2:
            messagebox.showerror("Error", "Parent folder is not selected!")
        else:
            if os.path.splitext(globalpath)[1]=="":
                addCertain_Panel(buttonRole)
            else:
                messagebox.showerror("Error", "Parent folder cannot be file!")

    else:
        addCertain_Panel(1)




addNewFrame = None
def exitAddNewFrameFunc():
    global addNewFrame
    if addNewFrame:
        addNewFrame.destroy()
        addNewFrame = None

def addAny_Panel():
    global addNewFrame
    if addNewFrame is None or not addNewFrame.winfo_exists():
        addNewFrame= Frame(windows, width=500, height=300)
        addNewFrame.place(relx=0.3, rely=0.3, )

    panelName=Label(addNewFrame, text="Add New",font=("Arial",20, "bold")).place(relx=0.5, rely=0.08, anchor=CENTER)

    exitAddNewFrame=Button(addNewFrame, command=exitAddNewFrameFunc,borderwidth=0, highlightthickness=0,image=normal_exitButtonImg )
    exitAddNewFrame.place(relx=1,rely=0,x=-20,y=15,  anchor=CENTER)
    exitAddNewFrame.bind('<Enter>', lambda event:exitAddNewFrame.config(image=hover_exitButtonImg))
    exitAddNewFrame.bind('<Leave>', lambda event:exitAddNewFrame.config(image=normal_exitButtonImg))

    newFolderButton=Button(addNewFrame,text="Add new folder",font=("Arial",10, "bold"), compound=TOP,command=lambda: [whichButtClicked(1),addCertain_Panel(1)],borderwidth=0, highlightthickness=0,image=newFoldericon,).place(relx=0.2,rely=0.5,  anchor=CENTER,)

    newSubFolderButton=Button(addNewFrame,text="Add new subfolder",font=("Arial",10, "bold"), command=lambda: [whichButtClicked(2)],compound=TOP,borderwidth=0, highlightthickness=0,image=newSubFoldericon ).place(relx=0.5,rely=0.5,  anchor=CENTER,)

    newFileButton=Button(addNewFrame,text="Add new file",font=("Arial",10, "bold"), compound=TOP,command=lambda: [whichButtClicked(3)],borderwidth=0, highlightthickness=0,image=newFileicon ).place(relx=0.8,rely=0.5,  anchor=CENTER,)








#button in the SE corner
addNew=Button(defaultMainFrame,state=ACTIVE,image=addButtonImg, command=addAny_Panel,borderwidth=0, highlightthickness=0)
addNew.place(x=100, y=720, anchor=SE)


#keep button on the SE corner
def on_resize(event):
    width = event.width
    height = event.height
    addNew.place(x=width-100, y=height-100, anchor='nw')

FMcan.bind("<Configure>", on_resize)
windows.update()



hierarchy()



windows.minsize(width=1280, height=720)
windows.config(background="black")
windows.title("File manager")  #promijeni ime prozora

windows.mainloop()