import os
import shutil
from pathlib import Path

import urllib.request
import urllib.parse
import urllib.error


demos = []
folder = ".demosfiles"
path = Path(folder)
folderexists = False

if os.path.isdir(folder):
        folderexists = True

# devuelve la carpeta raiz donde esta todo el contenido
def init():
    global folder
    if not os.path.isdir(folder):
        print("No demos folder found, creating one")
        try:
            os.mkdir(folder)
        except: 
            print("Couln't create source folder... retrying")
            return init()

    if not os.path.isdir(".tmp"):
        print("No .tmp folder found, creating one")
        try:
            os.mkdir(".tmp")
        except:
            print("No .tmp Folder created")

    return folder

#devuelve la ip local donde la app se esta ejecutando
def getURL(urls):
    for url in urls:
        if "127.0.0.1" not in url and "localhost" not in url:
            return url
        return "... you cant?!"

class demo:
    def __init__(self, path):
        data  = path.split("_")
        self.id = int(data[0])
        self.type = data[1]
        self.name = data[2]
        self.path = folder + "/" + path

    def changeName(self, name):
        self.name = name
        self.path = folder + "/"  + (str(self.id)  + "_" + self.type + "_" + self.name)
        Path(self.path).rename(self.path)

    def changeType(self, type):
        self.type = type
        self.path = folder + "/"  + (str(self.id)  + "_" + self.type + "_" + self.name)
        Path(self.path).rename(self.path)

    def delete(self):
        try:
            shutil.rmtree(self.path)
            return
        except:
            return

    def add_note(self, note):
        with open(self.path + "/notes.txt", "w", encoding="utf-8") as notesfile:
            notesfile.write(note)
        

def update_demos(fromNewDemo = False):
    global demos
    global path
    demos.clear()
    for subfolder in path.iterdir():
        if not subfolder.is_dir():
            continue
        if subfolder.name.split("_")[1] == "init" and not fromNewDemo:
            try:
                subfolder.rmdir()
            except:
                print("The init element contains files, not deleted.")
            continue
        demos.append(demo(subfolder.name))    
    demos.sort(key=lambda demo: demo.id)
    if not demos and not fromNewDemo:
        newDemo("init", "Add a new demo in the 'Add new material' section")

def newDemo(elementtype, name):
    global folder
    global demos

    update_demos(fromNewDemo = True)
    newid = 0 if not demos else int(demos[-1].id) + 1
    os.mkdir(str(folder + "/" + str(newid)  + "_" + elementtype + "_" + name))
    update_demos(fromNewDemo = True)
    return int(demos[-1].id)

def selectDemoById(id):
    for subfolder in path.iterdir():
        if not subfolder.is_dir():
            continue

        if subfolder.name.startswith(str(id) + "_"):
            return demo(subfolder.name)

    return 0

def listFiles(demo, formats):
    files = []
    for file in Path(demo.path).iterdir():
        if file.is_dir():
            continue
        if file.name == "notes.txt":
            continue

        if file.name.split(".")[-1] in formats or not formats:
            files.append(file.name)
    return files
        
    
#esto para mover los archivos de tmp a donde deberian aja?
# files = array de ".tmp/"
#destine = la carpeta
def movFromTmp(files, destine): # destine jaja
    for file in files:
        shutil.move(".tmp/" + file, destine + "/" + file)
    
def emtpyTmp():
    shutil.rmtree(".tmp")
    os.makedirs(".tmp")


class qrcode:
    def __init__(self, text):
        safe_text = urllib.parse.quote(text)
        try:
            req = urllib.request.Request("https://google.io/", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5):
                self.success = True
                self.image = f"https://quickchart.io/qr?text={text}&size=300"
        except (requests.ConnectionError, requests.Timeout):
            self.success = False
            self.image = None
