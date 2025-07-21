import c4d
from math import pi

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


"""Sélectionner le neutre Forêts de la maquette swisstopo
   Remplace tous les effecteur random de la hiérarchie 
   (attention avec valeurs par défauts"""

def rdm_effector():
    rdm_effector = c4d.BaseObject(c4d.Omgrandom)

    rdm_effector[c4d.ID_MG_BASEEFFECTOR_POSITION_ACTIVE] = False
    rdm_effector[c4d.ID_MG_BASEEFFECTOR_ROTATE_ACTIVE] = True
    rdm_effector[c4d.ID_MG_BASEEFFECTOR_ROTATION, c4d.VECTOR_X] = pi * 2

    rdm_effector[c4d.ID_MG_BASEEFFECTOR_SCALE_ACTIVE] = True
    rdm_effector[c4d.ID_MG_BASEEFFECTOR_UNIFORMSCALE] = True
    rdm_effector[c4d.ID_MG_BASEEFFECTOR_POSITIVESCALE] = True
    rdm_effector[c4d.ID_MG_BASEEFFECTOR_USCALE] = 0.5
    return rdm_effector

def get_all_children_obj_type(obj_type,obj,lst = []):
    while obj :
        if obj.CheckType(obj_type):
            lst.append(obj)
            #print(obj)
        get_all_children_obj_type(obj_type,obj.GetDown(),lst)
        obj = obj.GetNext()
    return lst


def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    #get_all_children_obj_type(c4d.Omgrandom,op.GetDown(), lst = [])
    cloners = get_all_children_obj_type(c4d.Omgcloner,op.GetDown(), lst = [])
    doc.StartUndo()
    for cloner in cloners:
        in_ex_data = cloner[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]
        for i in range(in_ex_data.GetObjectCount()):
            effector = in_ex_data.ObjectFromIndex( doc, i)
            if effector.CheckType(c4d.Omgrandom):
                new_effector = rdm_effector()
                new_effector.InsertAfter(effector)
                doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,new_effector)
                in_ex_data.DeleteObject(i)
                in_ex_data.InsertObject(new_effector,1)
                doc.AddUndo(c4d.UNDOTYPE_CHANGE,cloner)
                doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, effector)
                effector.Remove()
        cloner[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST] = in_ex_data
    doc.EndUndo()
    c4d.EventAdd()
    return


    res =  clonerFromPolyObject(op,50, objs_to_clone=None)
    doc.InsertObject(res)
    c4d.EventAdd()

if __name__ == '__main__':
    main()