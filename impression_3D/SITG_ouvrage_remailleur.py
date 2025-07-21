import c4d

"""sélectionner les ouvrages d'art à remailler
   crée un générateur + mailleur de volume
   avec les régalges qui vont bien (adapter au beoin)
   J'ai testé uniquement avec un objet polygonal unique"""

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    
    for o in doc.GetActiveObjects(0):
        mg = o.GetMg()
        gen_vol = c4d.BaseObject(c4d.Ovolumebuilder)
        gen_vol[c4d.ID_VOLUMEBUILDER_GRID_SIZE] = 0.25
        gen_vol.SetName(op.GetName()+'_gen_vol')
    
        mesh_vol = c4d.BaseObject(c4d.Ovolumemesher)
        mesh_vol[c4d.ID_VOLUMETOMESH_THRESHOLD] = 0.65
        mesh_vol.SetName(op.GetName()+'_mesh_vol')
        gen_vol.InsertUnder(mesh_vol)
        mesh_vol.SetMg(c4d.Matrix(mg))
    
    
        doc.InsertObject(mesh_vol, pred = o)
        o.InsertUnder(gen_vol)
        o.SetMg(c4d.Matrix(mg))
    doc.SetActiveObject(mesh_vol)
    c4d.EventAdd()


if __name__ == '__main__':
    main()