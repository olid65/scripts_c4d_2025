import c4d
from pathlib import Path
import sys

#ATTENTION BIEN REGLER LES PREFS D'IMPORT EN IMPORTANT UN FICHIER obj
#SCALE : 1 mETERS
#DECOCHER TOUTES LES CASES Flip et Swap

#Changer la variable swap avec l'emplacement du dossier principal


#le dossier importe tous les fichiers .obj, règle la position d'après les fichiers .wld3
#l'origine de l'objet neutre est stockée dans l'onglet annotation'

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def xyz_from_wld3(wld3_file):
    """
    Extracts the x, y, z coordinates from a .wld3 file.
    The coordinates are expected to be in the last three positions of the first line.
    """
    with open(wld3_file, "r") as f:
        # Read the first line and split by commas
        xyz = f.readline().strip().split(" ")[1].split(",")
        # Extract the last three values
        x = float(xyz[0])
        y = float(xyz[1])
        z = float(xyz[2])
    return c4d.Vector(x,z,y)

def main():
    pth = r"C:\Users\olivi\Downloads\footprint_LasBuildingMultipa3_Export3DObjects1 (2)"
    pth = Path(pth)
    origin = None

    #récupération recursive de tous les fichiers .obj et .wld3
    obj_files = list(pth.rglob("*.obj"))
    wld3_files = list(pth.rglob("*.wld3"))
    
    onull = c4d.BaseObject(c4d.Onull)
    onull.SetName(pth.name)
    doc.InsertObject(onull)
    

    #parcours des fichiers .obj et .wld3 avec  zip (un fichier .obj a un seul .wld3)
    for obj_file, wld3_file in zip(obj_files, wld3_files):
        c4d.documents.MergeDocument(doc, str(obj_file), c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MERGESCENE)
        obj = doc.GetFirstObject()
        pos = xyz_from_wld3(wld3_file)
        if not origin : origin = pos
        obj.SetAbsPos(pos-origin)
        obj.SetName(wld3_file.parent.name)
        obj.InsertUnderLast(onull)

        
    tag = c4d.BaseTag(c4d.Tannotation)
    tag[c4d.ANNOTATIONTAG_TEXT] = f"ORIGINE : \nx={origin.x} \ny={origin.y} \nz={origin.z} \n{origin}"
    onull.InsertTag(tag)
    c4d.EventAdd()

if __name__ == '__main__':
    main()