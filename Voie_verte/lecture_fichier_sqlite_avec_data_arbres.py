import c4d
from pathlib import Path
import sqlite3


doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.
CONTAINER_ORIGIN = 1026473
TAILLE_OBJ_SRCE = c4d.Vector(10)

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    fn_db = Path(r"C:\Users\olivi\switchdrive\Mandats\Voie_verte\DOC\CFF200-61-AFS-T301-P01 Etats editions Voie Verte_OD_for_db.db")
    if not fn_db.exists():
        c4d.gui.MessageDialog(f"Database file not found: {fn_db}")
        return

    origin = doc[CONTAINER_ORIGIN]
    res = c4d.BaseObject(c4d.Onull)
    res.SetName('arbres_voies_verte')

    conn = sqlite3.connect(fn_db)
    cursor = conn.cursor()


    # Print all columns in the 'editions' table
    # cursor.execute("PRAGMA table_info(editions);")
    # columns = cursor.fetchall()
    # print("Columns in 'editions' table:")
    # for i,column in enumerate(columns):
    #     print(f"   {i} ->{column[1]}, Type: {column[2]}")

    # Example: Fetching data from a specific table
    # cursor.execute("SELECT * FROM editions LIMIT 10;")  # Adjust the table name
    # rows = cursor.fetchall()
    # print("Sample data from 'editions' table:")
    # for row in rows:
    #     print(row[37], row[38])
    # print('-' * 40 + "\n")

    # récupération de tous les éléments de la colonne 'x', 'y', 'numero','nom', 'haut','rayon_couronne'
    # et stockage dans des variable du même nom
    cursor.execute("SELECT x, y, numero, nom, haut, rayon_couronne FROM editions;")
    rows = cursor.fetchall()
    for x, y, numero, nom, haut, rayon_couronne in rows:
        if x and y:
            pos = c4d.Vector(x,0,y)
            if not origin:
                origin = c4d.Vector(pos)
                doc[CONTAINER_ORIGIN] = origin
            pos = pos-origin
            #instance
            inst = c4d.BaseObject(c4d.Oinstance)
            inst.SetAbsPos(pos)
            inst.SetName(f"{str(numero).zfill(3)}_{nom}")
            if rayon_couronne and haut:
                diam = rayon_couronne *2
                scale = c4d.Vector(diam/TAILLE_OBJ_SRCE.x, haut/TAILLE_OBJ_SRCE.y,diam/TAILLE_OBJ_SRCE.z)
                inst.SetAbsScale(scale)
            else:
                inst[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = c4d.ID_BASELIST_ICON_COLORIZE_MODE_CUSTOM
                inst[c4d.ID_BASELIST_ICON_COLOR] = c4d.Vector(1,0,0)
                inst[c4d.ID_BASEOBJECT_USECOLOR] = c4d.ID_BASEOBJECT_USECOLOR_ALWAYS
                inst[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(1,0,0)
                print(inst.GetName())
            inst.InsertUnderLast(res)
    doc.InsertObject(res)
    c4d.EventAdd()

if __name__ == '__main__':
    main()