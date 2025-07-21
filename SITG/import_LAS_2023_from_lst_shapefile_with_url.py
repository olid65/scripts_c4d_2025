import c4d
import shapefile
from pathlib import Path
import urllib.request
import zipfile
import sys

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

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def extract_points_veget(las_file_path, origine,veget_only = True):
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
            #mask = (x >= xmin) & (x <= xmax) & (y >= ymin) & (y <= ymax)

            ##################################################################
            #MASK MASK MASK CLASSIFICATION
            ##################################################################
            if veget_only:
                #inside = points[((classif == 5) | (classif == 4) | (classif == 3))]
                inside = points[((classif == 5) | (classif == 4))]
                #inside = points[((classif == 5))]
            else:
                inside = points
            if  inside:
                pts_res.extend([c4d.Vector(x,y,z)-origine for x,y,z in zip(inside.x,inside.z,inside.y)])
                clas.extend([c for c in inside.classification])
    return pts_res, clas

def extractLAS(list_fn,doc, veget_only = True):
    origine = doc[CONTAINER_ORIGIN]
    for fn in list_fn:
        if not fn.exists():
            print(f"Le fichier {fn} n'existe pas")
            continue
        pts, lst_classif = extract_points_veget(fn,origine,veget_only=veget_only)

        if pts:
            nb_pts = len(pts)
            res = c4d.PolygonObject(nb_pts,0)
            res.SetName(fn.stem)
            res.SetAllPoints(pts)
            res.Message(c4d.MSG_UPDATE)
            doc.InsertObject(res)

            #A ENLEVER SI ON VEUT LE VERTEX COLOR PAR CLASSE
            continue

            #vertexcolor tag
            tag = c4d.VertexColorTag(len(pts))
            res.InsertTag(tag)
            tag[c4d.ID_VERTEXCOLOR_DRAWPOINTS] = True
            data = tag.GetDataAddressW()
            white = c4d.Vector4d(1.0, 1.0, 1.0, 1.0)
            pointCount = res.GetPointCount()
            for idx in range(pointCount):
                class_color = classif.get(lst_classif[idx],None)
                if class_color:
                    color = class_color[2]
                else:
                    color = c4d.Vector4d(0, 0, 0, 1)


def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    fn = Path(r"C:\Users\olivi\switchdrive\Mandats\2025_Prairie\lidar_2023.shp")

    path_dir_dwnld = Path(r"C:\Temp\LAS_LIDAR_TEMP")
    lst_url = []
    origin = doc[CONTAINER_ORIGIN]
    if not origin:
        c4d.gui.MessageDialog("Document non géoréférencé")
        return
    with shapefile.Reader(str(fn)) as shp:
        #lecture du champs 'url_telech' pour chaque enregistrement
        for record in shp.records():
            lst_url.append(record['url_telech'])

    lst_fn = []
    lat_non_present = []
    for url in lst_url:
        name = url.split('/')[-1][:-4]
        fn_las = path_dir_dwnld / Path(name)
        if fn_las.exists:
            lst_fn.append(fn_las)
        else:
            lat_non_present.append(name)
    if lat_non_present:
        rep = c4d.gui.QuestionDialog(f'Il manque {len(lat_non_present)}/{len(lst_url)}. Voulez vous continuer ?')
        if not rep : return

    extractLAS(lst_fn,doc, veget_only = True)
    c4d.EventAdd()

if __name__ == '__main__':
    main()