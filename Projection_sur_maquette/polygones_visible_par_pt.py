import c4d


def get_active_camera_view():
    """Récupère la vue de la caméra active"""
    bd = doc.GetActiveBaseDraw()
    if not bd:
        return None

    camera = bd.GetSceneCamera(doc)
    if not camera:
        return None
    # On retourne le BaseDraw au lieu de GetView()
    return bd

def create_point_selection_tag(obj):
    """Crée un tag de sélection de points pour l'objet"""
    tag = c4d.BaseTag(c4d.Tpointselection)
    if tag is None:
        return None
    obj.InsertTag(tag)
    return tag

def test_points_visibility(obj, bd):
    """Teste la visibilité des points d'un objet depuis une vue"""
    if not obj.CheckType(c4d.Opolygon):
        return None

    # Création du tag de sélection
    tag = create_point_selection_tag(obj)
    if not tag:
        return None

    # Récupération des points et matrices
    points = obj.GetAllPoints()
    mg = obj.GetMg()
    camera = bd.GetSceneCamera(doc)
    if not camera:
        return None

    # Matrice inverse de la caméra pour conversion en espace caméra
    cam_mg_inv = ~camera.GetMg()

    # Initialisation de la sélection
    bs = tag.GetBaseSelect()
    bs.DeselectAll()

    # Test de chaque point
    for i, p in enumerate(points):
        # Conversion du point en coordonnées monde puis en espace caméra
        #p_world = p * mg
        p_cam = bd.WC(p*mg)

        # Test de la visibilité du point en espace caméra
        if bd.TestPointZ(p_cam):
            p_scr = bd.CS(p_cam, False)
            if bd.TestPoint(p_scr.x, p_scr.y):
                bs.Select(i)
            else: print(i)

    tag.Message(c4d.MSG_UPDATE)
    return tag

def main() -> None:
    """Fonction principale"""
    # Récupération de la vue caméra active
    bd = get_active_camera_view()
    if not bd:
        c4d.gui.MessageDialog("Pas de caméra active trouvée.")
        return

    # Récupération des objets sélectionnés
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    if not selection:
        c4d.gui.MessageDialog("Aucun objet sélectionné.")
        return

    # Traitement de chaque objet sélectionné
    for obj in selection:
        if obj.CheckType(c4d.Opolygon):
            test_points_visibility(obj, bd)

    c4d.EventAdd()

if __name__ == '__main__':
    main()