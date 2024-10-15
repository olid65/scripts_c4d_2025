import c4d

"""Sélectionner l'objet polygonal contenant les points des arbres sélectionnés
   supprime les points de l'objet et corrige sur le cloneur les tags Zone influence Mograph
   en supprimant les valeurs des points à supprimer
   
   Le cloneur avecc les tags doit être à la suite dans la même hiérarchie"""
   
doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    

    cloner = None
    obj = op.GetNext()
    
    while obj:
        if obj.CheckType(c4d.Omgcloner):
            cloner = obj
        obj = obj.GetNext()

    
    if not cloner or not op :
        print('pas ok')
        return
    
    tags = [tag for tag in cloner.GetTags() if tag.CheckType(c4d.Tmgweight)]
    
    bs = op.GetPointS()
    
    to_remove = []
    new_pts = []
    for i,pt in enumerate(op.GetAllPoints()):
        if bs.IsSelected(i):
            #bs.Select(i)
            to_remove.append(i)
        else:
            new_pts.append(pt)
 
    op.ResizeObject(len(new_pts),0)
    op.SetAllPoints(new_pts)
    op.Message(c4d.MSG_UPDATE)
    
    
    for tag in tags:
        weights = c4d.modules.mograph.GeGetMoDataWeights(tag)
        weights = [w for i,w in enumerate(weights) if i not in to_remove]
        c4d.modules.mograph.GeGetMoDataWeights(tag)
        c4d.modules.mograph.GeSetMoDataWeights(tag, weights)
        tag.Message(c4d.MSG_UPDATE)
    
    bs.DeselectAll()
    
    c4d.EventAdd()


if __name__ == '__main__':
    main()