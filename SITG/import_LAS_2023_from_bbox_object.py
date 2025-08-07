from typing import Optional
import c4d
import sys
from pathlib import Path

try : import laspy
except :
    sys.path.append('C:\\Users\\olivi\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages')
    import laspy


CONTAINER_ORIGIN = 1026473

classif ={
            1 :("Non classifié","None", c4d.Vector4d(1, 0, 0, 1)),
            2 :("Sol","sol", c4d.Vector4d(0.44, 0.375, 0.141, 1)),
            3 :("Basse végétation (<50cm)","veget_bas", c4d.Vector4d(0.55, 0.73, 0.453, 1)),
            5 :("Haute végétation (>50cm)","veget_haut", c4d.Vector4d(0.213, 0.35, 0.179, 1)),
            6 :("Bâtiments","bati", c4d.Vector4d(0.56, 0.56, 0.56, 1)),
            7 :("Points bas ou isolés","pts_bas", c4d.Vector4d(1, 0.55, 1, 1)),
            9 :("Eau","eau", c4d.Vector4d(0.41, 0.862, 1, 1)),
            13 :("Ponts, passerelles","ponts", c4d.Vector4d(0.23, 0.23, 0.23, 1)),
            15 :("Sol (points complémentaires)","sol", c4d.Vector4d(0.497, 0.5, 0.325, 1)),
            16 :("Bruit","bruit", c4d.Vector4d(1, 0, 0.917, 1)),
            19 :("Points mesurés hors périmètre de l'acquisition","hors_perim", c4d.Vector4d(1, 0.983, 0, 1)),
          }
# cassification pour LIDAR 2023 (https://sitg.ge.ch/donnees/lidar-aerien-2023-03)
classif = {
    1:  ("Non classifié", "None", c4d.Vector(1, 0, 0)),                   # Rouge vif (inchangé)
    2:  ("Sol", "sol", c4d.Vector(0.44, 0.375, 0.141)),                   # Marron terreux (ancien)
    3:  ("Basse végétation (<50cm)", "veget_bas", c4d.Vector(0.55, 0.73, 0.453)), # Vert clair (ancien)
    4:  ("Moyenne végétation (0.5-3m)", "veget_moy", c4d.Vector(0.38, 0.63, 0.28)), # Vert moyen (créé intermédiaire)
    5:  ("Haute végétation (>3m)", "veget_haut", c4d.Vector(0.213, 0.35, 0.179)),  # Vert foncé (ancien)
    6:  ("Bâtiments", "bati", c4d.Vector(0.56, 0.56, 0.56)),                        # Gris clair (ancien)
    7:  ("Points bas ou isolés / erreurs", "erreurs", c4d.Vector(1, 0.55, 1)),      # Rose-violet (ancien)
    9:  ("Eau", "eau", c4d.Vector(0.41, 0.862, 1)),                                 # Bleu clair (ancien)
    11: ("Piles de matériel naturel", "mat_nat", c4d.Vector(0.47, 0.37, 0.22)),     # Brun foncé (interpolé)
    13: ("Ponts, passerelles", "ponts", c4d.Vector(0.23, 0.23, 0.23)),              # Gris foncé (ancien)
    14: ("Câbles", "cables", c4d.Vector(0.8, 0.8, 0.8)),                            # Gris très clair (nouveau)
    15: ("Mâts, antennes", "mats", c4d.Vector(0.7, 0.7, 0.7)),                      # Gris clair (nouveau)
    17: ("Ponts, passerelles", "ponts2", c4d.Vector(0.23, 0.23, 0.23)),             # Gris foncé (copié 13)
    18: ("Bruit", "bruit", c4d.Vector(1, 0, 0.917)),                                # Magenta (ancien 16)
    21: ("Voitures", "voitures", c4d.Vector(1, 0.983, 0)),                          # Jaune vif (ancien 19)
    22: ("Facades", "facades", c4d.Vector(0.7, 0.7, 0.7)),                          # Gris clair (nouveau)
    25: ("Grues, trains, objets temporaires", "objtemps", c4d.Vector(1, 0.6, 0)),   # Orange vif (nouveau)
    26: ("Objets sur les toits", "objtoits", c4d.Vector(0.550, 0.325, 0.188)),      # Brun/marron (interpolé)
    29: ("Murs", "murs", c4d.Vector(0.3, 0.3, 0.3)),                                # Gris foncé (plus sombre)
    31: ("Points de sol additionnels", "soladd", c4d.Vector(0.497, 0.5, 0.325)),    # Brun verdâtre (ancien 15)
}

def empriseObject(obj, origine):
    geom = obj
    if not geom.CheckType(c4d.Opoint):
        geom = geom.GetCache()
        if not geom.CheckType(c4d.Opoint) : return None
    mg = obj.GetMg()
    pts = [p*mg+origine for p in geom.GetAllPoints()]
    lst_x = [p.x for p in pts]
    lst_y = [p.y for p in pts]
    lst_z = [p.z for p in pts]

    xmin = min(lst_x)
    xmax = max(lst_x)
    ymin = min(lst_y)
    ymax = max(lst_y)
    zmin = min(lst_z)
    zmax = max(lst_z)

    mini = c4d.Vector(xmin,ymin,zmin)
    maxi = c4d.Vector(xmax,ymax,zmax)

    return mini, maxi

def extract_points_within_bounding_box(las_file_path,  xmin, xmax, ymin, ymax, origine,veget_only = True):
    pts_res = []
    clas = []
    with laspy.open(las_file_path) as file:

        for points in file.chunk_iterator(1024):
            #print(f"{count / file.header.point_count * 100}%")

            # For performance we need to use copy
            # so that the underlying arrays are contiguous
            x, y = points.x.copy(), points.y.copy()
            classif = points.classification.copy()
            #r,v,b = points.r.copy(), points.v.copy(), points.b.copy()
            mask = (x >= xmin) & (x <= xmax) & (y >= ymin) & (y <= ymax)

            ##################################################################
            #MASK MASK MASK CLASSIFICATION
            ##################################################################
            if veget_only:
                inside = points[mask & ((classif == 5) | (classif == 4) | (classif == 3))]
            else:
                inside = points[mask]
            if  inside:
                pts_res.extend([c4d.Vector(x,y,z)-origine for x,y,z in zip(inside.x,inside.z,inside.y)])
                clas.extend([c for c in inside.classification])
    return pts_res, clas

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def extractLAS(list_fn, bbox,doc, veget_only = True):
    origine = doc[CONTAINER_ORIGIN]
    xmin,ymin,xmax,ymax = bbox
    for fn in list_fn:
        if not fn.exists():
            print(f"Le fichier {fn} n'existe pas")
            continue
        pts, lst_classif = extract_points_within_bounding_box(fn, xmin, xmax, ymin, ymax,origine,veget_only=veget_only)
        print(lst_classif[:5])
        if pts:
            nb_pts = len(pts)
            res = c4d.PolygonObject(nb_pts,0)
            res.SetAllPoints(pts)
            res.Message(c4d.MSG_UPDATE)
            doc.InsertObject(res)
            #vertexcolor tag
            tag = c4d.VertexColorTag(len(pts))
            res.InsertTag(tag)
            tag[c4d.ID_VERTEXCOLOR_DRAWPOINTS] = True
            data = tag.GetDataAddressW()
            white = c4d.Vector(1.0, 1.0, 1.0)
            pointCount = res.GetPointCount()
            for idx in range(pointCount):
                class_color = classif.get(lst_classif[idx],None)
                if class_color:
                    color = class_color[2]
                else:
                    color = c4d.Vector(1, 0, 0)
                c4d.VertexColorTag.SetColor(data, None, None, idx, color)
    c4d.EventAdd()

def main() -> None:
    #fn = '/Users/olivierdonze/Downloads/2501750_1126250.las'
    list_fn = [r"C:\Temp\LAS_LIDAR_TEMP\2494250_1120750.las"]
    list_fn = [Path(r'C:\Temp\LAS_LIDAR_TEMP\2496750_1119250.las'),Path(r'C:\Temp\LAS_LIDAR_TEMP\2496750_1119500.las')]
    if not op:
        print("pas d'objet sélectionné")
        return
    origine = doc[CONTAINER_ORIGIN]
    mini,maxi = empriseObject(op, origine)
    bbox = mini.x,mini.z,maxi.x,maxi.z
    extractLAS(list_fn, bbox,doc,veget_only = False)
    return



"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()