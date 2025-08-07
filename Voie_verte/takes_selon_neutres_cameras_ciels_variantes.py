import c4d
"""Sélectionner les caméras
(on peut sélectionner aussi d'autres objets -> le script ne garde que les cameras Standard ou RS)"""

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

Ophysicalsky = 1011146

CAMERAS_NAME = 'CAMERAS'
SKIES_NAME = 'CIELS'
VARIANTES_NAMES = 'VARIANTES_ARBRES'


"""ATTENTION de bien désactiver les ciels et les variantes avant
   et de mettre en autotake
   Modifier les noms des constantes ci-dessus selon besoins"""

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    # Gets the TakeData from the active document (holds all information about Takes)
    takeData = doc.GetTakeData()
    if takeData is None:
        raise RuntimeError("Failed to retrieve the take data.")

    if not takeData.GetTakeMode() == c4d.TAKE_MODE_AUTO:
        c4d.gui.MessageDialog("Vous devez activer l'Auto Take (bouton A de la palette take)")
        return
    doc.StartUndo()
    
    cameras_parent = doc.SearchObject(CAMERAS_NAME)
    skies_parent = doc.SearchObject(SKIES_NAME)
    variantes_parent = doc.SearchObject(VARIANTES_NAMES)
    if cameras_parent and cameras_parent.GetChildren():
        for cam in cameras_parent.GetChildren():
            if skies_parent and skies_parent.GetChildren():
                for sky in skies_parent.GetChildren():
                    if variantes_parent and variantes_parent.GetChildren():
                        for variante in variantes_parent.GetChildren():
                            name = f"{cam.GetName()}_{sky.GetName()}_{variante.GetName()}"
                            sky_clone = sky.GetClone()
                            variante_clone = variante.GetClone()
                            newTake = takeData.AddTake(name, None, None)
                            newTake.SetChecked(True)
                            if newTake is None:
                                raise RuntimeError("Failed to add a new take.")
                            # Checks if there is some TakeData and the current mode is set to auto Take
                            if takeData and takeData.GetTakeMode() == c4d.TAKE_MODE_AUTO:
                                sky[c4d.ID_BASEOBJECT_GENERATOR_FLAG]=True
                                newTake.AutoTake(takeData, sky, sky_clone)
                                sky[c4d.ID_BASEOBJECT_GENERATOR_FLAG]=False
                                
                                variante[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = c4d.OBJECT_ON
                                variante[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = c4d.OBJECT_ON
                                newTake.AutoTake(takeData, variante, variante_clone)
                                variante[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = c4d.OBJECT_OFF
                                variante[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = c4d.OBJECT_OFF
                            newTake.SetCamera(takeData, cam)
                            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,newTake)
    
    
    doc.EndUndo()
    c4d.EventAdd()                
    return

    skies = [o for o in doc.GetActiveObjectsFilter(True,Ophysicalsky, c4d.NOTOK)]

    if not skies :
        c4d.gui.MessageDialog("Vous devez sélectionner au moins un ciel")
        return

    # Gets the TakeData from the active document (holds all information about Takes)
    takeData = doc.GetTakeData()
    if takeData is None:
        raise RuntimeError("Failed to retrieve the take data.")

    if not takeData.GetTakeMode() == c4d.TAKE_MODE_AUTO:
        c4d.gui.MessageDialog("Vous devez activer l'Auto Take (bouton A de la palette take)")
        return
    doc.StartUndo()
    for sky in skies :
        sky_clone = sky.GetClone()
        newTake = takeData.AddTake(sky.GetName(), None, None)
        newTake.SetChecked(True)
        if newTake is None:
            raise RuntimeError("Failed to add a new take.")

        # Checks if there is some TakeData and the current mode is set to auto Take
        if takeData and takeData.GetTakeMode() == c4d.TAKE_MODE_AUTO:
            sky[c4d.ID_BASEOBJECT_GENERATOR_FLAG]=True
            newTake.AutoTake(takeData, sky, sky_clone)
            sky[c4d.ID_BASEOBJECT_GENERATOR_FLAG]=False
        #newTake.SetCamera(takeData, cam)
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,newTake)
    doc.EndUndo()
    c4d.EventAdd()


if __name__ == '__main__':
    main()