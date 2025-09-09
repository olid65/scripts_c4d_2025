import c4d


"""Sélectionner le cloneur arbres_SITG_2018_cloneur (ou autre
   et régler TAILLE:MAX et DIAM_MAX"""
doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

name_tag_hauteurs = 'hauteurs'
name_tag_dimetres = 'diametres'

TAILLE_MAX = 10
DIAM_MAX = 5

HAUT_SRCE = 10
DIAM_SOURCE = 10

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    cloner = op
    pts_obj = cloner[c4d.MG_OBJECT_LINK]
    tags = [tag for tag in cloner.GetTags() if tag.CheckType(c4d.Tmgweight)]
    
    tag_haut = None
    tag_diam = None
    pts_to_remove = []
    
    for tag in tags:
        if tag.GetName()== name_tag_hauteurs:
            tag_haut = tag
        if tag.GetName()== name_tag_dimetres:
            tag_diam = tag
    
    if tag_haut and TAILLE_MAX:
        hauts = c4d.modules.mograph.GeGetMoDataWeights(tag_haut)

        for i,h in enumerate(hauts):
            haut = (h+1)*HAUT_SRCE
            if haut<TAILLE_MAX:
                pts_to_remove.append(i)
           
    if tag_diam and DIAM_MAX:
        diams = c4d.modules.mograph.GeGetMoDataWeights(tag_diam)

        for i,d in enumerate(diams):
            diam = (h+1)*DIAM_SOURCE
            if diam<DIAM_MAX:
                pts_to_remove.append(i)            
    
    #pour supprimer les doublons et plus rapide quand on fait 'if i in pts_to_remove'
    #mais attention ce n'est plus une liste'
    pts_to_remove = set(pts_to_remove)
    #Suppression des points dans l'objet point
    new_pts = []
    for i,pt in enumerate(pts_obj.GetAllPoints()):
        if not i in pts_to_remove:
            new_pts.append(pt)
    
    pts_obj.ResizeObject(len(new_pts),0)
    pts_obj.SetAllPoints(new_pts)
    pts_obj.Message(c4d.MSG_UPDATE)
    
    for tag in tags:
        weights = c4d.modules.mograph.GeGetMoDataWeights(tag)
        weights = [w for i,w in enumerate(weights) if i not in pts_to_remove]
        c4d.modules.mograph.GeGetMoDataWeights(tag)
        c4d.modules.mograph.GeSetMoDataWeights(tag, weights)
        tag.Message(c4d.MSG_UPDATE)
        
    c4d.EventAdd()
    

if __name__ == '__main__':
    main()