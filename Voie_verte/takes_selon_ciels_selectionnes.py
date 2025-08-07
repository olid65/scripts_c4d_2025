import c4d
"""Sélectionner les caméras 
(on peut sélectionner aussi d'autres objets -> le script ne garde que les cameras Standard ou RS)"""

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

Ophysicalsky = 1011146

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """

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