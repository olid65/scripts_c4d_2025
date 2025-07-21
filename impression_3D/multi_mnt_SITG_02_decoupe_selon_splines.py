import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


"""Après avoir importer tous les tiff les mettre dans un neutre
   mettre l'objet contenant les splines juste après
   l'ordre doit ^être le m^ême pour les deux et dans le nom de chaque MNT
   on doit retrouver le nom de la spline

   Attention les MNT seront déplacés un neutre appelés découpe_MNT
   sera créé avec tous les objets booléens
   Il faut ensuite manuellement convertir en objet et supprimer
   ce qui n'est pas MNT"""

EXTRUSION_VALUE = 1000

def decoupe(mnt,sp):
    bool_obj = c4d.BaseObject(c4d.Oboole)
    bool_obj[c4d.BOOLEOBJECT_TYPE] = c4d.BOOLEOBJECT_TYPE_INTERSECT
    bool_obj[c4d.BOOLEOBJECT_HIGHQUALITY] = False
    bool_obj.SetMg(sp.GetMg())
    bool_obj.SetName(mnt.GetName())
    extr = c4d.BaseObject(c4d.Oextrude)

    sp_clone = sp.GetClone()
    sp_clone.InsertUnder(extr)
    sp_clone.SetRelPos(c4d.Vector(0))
    
    extr.InsertUnder(bool_obj)
    extr[c4d.EXTRUDEOBJECT_DIRECTION] = c4d.EXTRUDEOBJECT_DIRECTION_Y
    extr[c4d.EXTRUDEOBJECT_EXTRUSIONOFFSET] = EXTRUSION_VALUE

    mnt_mg = mnt.GetMg()
    mnt.InsertUnder(bool_obj)
    mnt.SetMg(mnt_mg)
    
    sp_clone.SetMg(c4d.Matrix(sp.GetMg()))

    return bool_obj


def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    doc.StartUndo()
    res = c4d.BaseObject(c4d.Onull)
    res.SetName('decoupes_MNT')
    doc.InsertObject(res)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,res)


    for mnt,sp in zip(op.GetChildren(),op.GetNext().GetChildren()):
        #on vérifie que le nom de la pièce est bien contenu dans le nom du MNT
        if sp.GetName() in mnt.GetName():
            print('ok')
        else :
            print(sp.GetName(),mnt.GetName())
            continue
        doc.AddUndo(c4d.UNDOTYPE_CHANGE,mnt)
        boole_obj = decoupe(mnt,sp)
        boole_obj.InsertUnderLast(res)


    doc.EndUndo()
    c4d.EventAdd()


if __name__ == '__main__':
    main()