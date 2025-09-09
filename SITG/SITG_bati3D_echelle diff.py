import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


""" ATTENTION les batiments doivent être sépaarés et leur axe poser sur le terrain
    -> utiliser d'abord SITG_bati3D_plaquer axes de chaque batiment sur terrain pour mise echelle diff.py
    TODO : dans la vieille ville il y a des batiment qui ne touchent pas partout le sol
           -> script pour baisser la base"""
SCALE_MNT = 2.5
SCALE_BATI = 1.25

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    doc.StartUndo()
    for o in op.GetChildren():
        doc.AddUndo(c4d.UNDOTYPE_CHANGE,o)
        
        pos = o.GetAbsPos()
        pos.y *= SCALE_MNT
        o.SetAbsPos(pos)
        
        scale = o.GetAbsScale()
        scale.y = SCALE_BATI
        o.SetAbsScale(scale)
        
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()