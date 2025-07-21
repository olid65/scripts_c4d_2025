import c4d
"""régler l'altitude de base ci-dessous
   sélectionner l'objet parent contenant les terrain auxquels on veut ajouter un socle
   Attention c'est un peu bricolé, faire un sauvagarde avant'
   """
ALT_BASE_SOCLE = 400


def selectEdgesContour(op):

    nb = c4d.utils.Neighbor(op)
    nb.Init(op)
    bs = op.GetSelectedEdges(nb,c4d.EDGESELECTIONTYPE_SELECTION)
    bs.DeselectAll()
    for i,poly in enumerate(op.GetAllPolygons()):
        inf = nb.GetPolyInfo(i)
        if nb.GetNeighbor(poly.a, poly.b, i)==-1:
            bs.Select(inf['edge'][0])

        if nb.GetNeighbor(poly.b, poly.c, i)==-1:
            bs.Select(inf['edge'][1])


        #si pas triangle
        if not poly.c == poly.d :
            if nb.GetNeighbor(poly.c, poly.d, i)==-1:
                bs.Select(inf['edge'][2])

        if nb.GetNeighbor(poly.d, poly.a, i)==-1:
            bs.Select(inf['edge'][3])

    op.SetSelectedEdges(nb,bs,c4d.EDGESELECTIONTYPE_SELECTION)

def socle(op):
    doc.AddUndo(c4d.UNDOTYPE_CHANGE,op)
    doc.SetActiveObject(op, mode= c4d.SELECTION_NEW)
    nb_pts_before = op.GetPointCount()
    #Sélection des arrêtes du contour
    selectEdgesContour(op)
    #Extrusion à zéro
    settings = c4d.BaseContainer()                 # Settings
    settings[c4d.MDATA_EXTRUDE_OFFSET] = 0      # Length of the extrusion

    res = c4d.utils.SendModelingCommand(command = c4d.ID_MODELING_EXTRUDE_TOOL,
                                    list = [op],
                                    mode = c4d.MODELINGCOMMANDMODE_EDGESELECTION,
                                    bc = settings,
                                    doc = doc)
    

    #Valeurs commune des points

    settings = c4d.BaseContainer()                 # Settings
    settings[c4d.MDATA_SETVALUE_SETY] = c4d.MDATA_SETVALUE_SET_SET
    settings[c4d.MDATA_SETVALUE_VAL] = c4d.Vector(0,ALT_BASE_SOCLE,0)
    #settings[c4d.TEMP_MDATA_SETVALUE_VAL_Y] = -2000
    settings[c4d.MDATA_SETVALUE_SYSTEM] = c4d.MDATA_SETVALUE_SYSTEM_WORLD

    res = c4d.utils.SendModelingCommand(command = c4d.ID_MODELING_SETVALUE_TOOL,
                                    list = [op],
                                    mode = c4d.MODELINGCOMMANDMODE_EDGESELECTION,
                                    bc = settings,
                                    doc = doc)
    
    #optimization (je ne sais pas pourquoi mai il y des points superposés)
    settings = c4d.BaseContainer()                 # Settings
    settings[c4d.MDATA_OPTIMIZE_TOLERANCE] = 0.0
    settings[c4d.MDATA_OPTIMIZE_POINTS] = True
    settings[c4d.MDATA_OPTIMIZE_POLYGONS] = True
    settings[c4d.MDATA_OPTIMIZE_UNUSEDPOINTS] = True
    
    bs = op.GetPointS()
    bs.SelectAll(op.GetPointCount()-1)
    
    res = c4d.utils.SendModelingCommand(command = c4d.MCOMMAND_OPTIMIZE,
                                    list = [op],
                                    mode = c4d.MODELINGCOMMANDMODE_POINTSELECTION,
                                    bc = settings,
                                    doc = doc)
    
    c4d.CallCommand(16351) # Mode Edges
    c4d.CallCommand(1009671) # Edge to Spline
    sp = op.GetDown()
    loft = c4d.BaseObject(c4d.Oloft)
    loft.InsertUnder(op)
    sp.InsertUnder(loft)
    
    c4d.CallCommand(100004768) # Select Children
    c4d.CallCommand(16768) # Connect Objects + Delete
    
    #optimization 2
    obj = doc.GetActiveObject()
    bs = obj.GetPointS()
    bs.SelectAll(obj.GetPointCount()-1)
    
    res = c4d.utils.SendModelingCommand(command = c4d.MCOMMAND_OPTIMIZE,
                                    list = [doc.GetActiveObject()],
                                    mode = c4d.MODELINGCOMMANDMODE_POINTSELECTION,
                                    bc = settings,
                                    doc = doc)

def main():
    mode_start = doc.GetMode()
    doc.StartUndo()
    for o in op.GetChildren():
        socle(o)
    


    doc.EndUndo()
    doc.SetMode(mode_start)
    c4d.EventAdd()


if __name__=='__main__':
    main()