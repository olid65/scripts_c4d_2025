

import c4d
import re,os

#valeurs de décalage des fichiers 3DS
DECAL_X = 2480000.00
DECAL_Z = 1109000.00
DECALAGE = c4d.Vector(2480000.00,0,1109000.00)

NOM_BAT3D = 'BATIMENTS_PROJETS'
NOM_BAT_PROJET = 'BATIMENTS'


CONTAINER_ORIGIN =1026473

ID_EGID_BC = 1030877 #no unique pour stocker les EGID et les polygones s'y rapportant (voir connectSupprim())

    
def centrerAxe(obj):
    mg = obj.GetMg()
    trans = obj.GetMp()
    trans.y = 0
    mg.off += trans
    if obj.GetPointCount():
        pts = [p-trans for p in obj.GetAllPoints()]
        obj.SetAllPoints(pts)
    obj.SetMg(mg)
    obj.Message(c4d.MSG_UPDATE)

def main(fn = None):
    res = c4d.BaseObject(c4d.Onull)
    #mise en cm des option d'importation 3DS
    plug = c4d.plugins.FindPlugin(1001037, c4d.PLUGINTYPE_SCENELOADER)
    if plug is None:
        print ("pas de module d'import 3DS")
        return 
    op = {}
   
    if plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, op):
        
        import_data = op.get("imexporter",None)
        if not import_data:
            print ("pas de data pour l'import 3Ds")
            return
        
        # Change 3DS import settings
        scale = import_data[c4d.F3DSIMPORTFILTER_SCALE]
        scale.SetUnitScale(1,c4d.DOCUMENT_UNIT_M)
        import_data[c4d.F3DSIMPORTFILTER_SCALE] = scale

    
    doc = c4d.documents.GetActiveDocument()

    if not fn:
        fn = c4d.storage.LoadDialog(type = c4d.FILESELECTTYPE_SCENES,
                                title= "Fichier 3DS")

    if not fn : return
    nom, ext =  os.path.splitext(os.path.basename(fn))

    if not ext == '.3ds' : 
        c4d.gui.MessageDialog("Ce n'est pas un fichier 3ds")
        return
    
    doc.StartUndo()
    first_object = doc.GetFirstObject()
    
    c4d.documents.MergeDocument(doc, fn, c4d.SCENEFILTER_OBJECTS)
    
    objs = []
    obj = doc.GetFirstObject()
    while obj:
        if obj == first_object : break
        objs.append(obj)
        obj = obj.GetNext()
        
    #si on a des batiments existants ou projet on stocke les
    #les polygones pour pouvoir mettre à l'échelle différenciée
    #type échelle Magnin'
    #bc = None
    #if nom == NOM_BAT3D or nom == NOM_BAT_PROJET: bc = True
    #connectSupprim(objs,nom,doc,bc)
    
    for obj in objs :
        if obj == first_object : break
        centrerAxe(obj)
        mg = obj.GetMg()
        if not doc[CONTAINER_ORIGIN]:
            doc[CONTAINER_ORIGIN] = mg.off + DECALAGE
            mg.off = c4d.Vector()
        else :
            mg.off += DECALAGE - doc[CONTAINER_ORIGIN]
        obj.SetMg(mg)
        obj.InsertUnderLast(res)   
        obj = obj.GetNext()
    doc.InsertObject(res)
    res.SetName(nom)
    doc.SetActiveObject(res, mode=c4d.SELECTION_NEW)
    #c4d.CallCommand(12148) # Cadrer la géométrie
    c4d.EventAdd()
    doc.EndUndo()
    
    
if __name__=='__main__':
    main()