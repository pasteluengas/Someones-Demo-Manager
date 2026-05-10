import os
import shutil
from pathlib import Path


demos = []
folder = ".demosfiles"
path = Path(folder)


# devuelve la carpeta raiz donde esta todo el contenido
def init():
    global folder
    if not os.path.isdir(folder):
        print("no hay carpeta socio creala")
        try:
            os.mkdir(folder)
        except: 
            print("Couln't create source folder... retrying")
            init()
            print("fuck off")

    if not os.path.isdir(".tmp"):
        print("no hay tmp")
        try:
            os.mkdir(".tmp")
        except:
            print("Pues a la mierda")

    return folder

#devuelve la ip local donde la app se esta ejecutando
def getURL(urls):
    for url in urls:
        if "127.0.0.1" not in url and "localhost" not in url:
            return url

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
        

def update_demos():
    global demos
    global path
    demos.clear()
    for subfolder in path.iterdir():
        if not subfolder.is_dir():
            continue
        demos.append(demo(subfolder.name))
    demos.sort(key=lambda demo: demo.id)

def newDemo(elementtype, name):
    global folder
    global demos

    os.mkdir(str(folder + "/" + str(len(demos) + 1)  + "_" + elementtype + "_" + name))
    update_demos()
    return int(len(demos))

def selectDemoById(id):
    for subfolder in path.iterdir():
        if not subfolder.is_dir():
            continue

        if subfolder.name.startswith(str(id) + "_"):
            return demo(subfolder.name)

    return 0

#esto para mover los archivos de tmp a donde deberian aja?
# files = array de ".tmp/"
#destine = la carpeta
def movFromTmp(files, destine): # destine jaja
    for file in files:
        shutil.move(".tmp/" + file, destine + "/" + file)
    
def emtpyTmp():
    shutil.rmtree(".tmp")
    os.makedirs(".tmp")
