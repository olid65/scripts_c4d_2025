import c4d
import shapefile
import os

# ATTENTION les points des segments doivent être en principe dans le sens horaire
# si on a un TROU, il doivent être antihoraire

# TODO -> détecter ce qui est polygones et trou et vérifier le sens des points

# TODO -> gérer les points intermédiaires selon le type (non linear)
#avec GetCache() -> mais ne supporte pas les segments

CONTAINER_ORIGIN =1026473

def fichierPRJ(fn):
    fn = os.path.splitext(fn)[0]+'.prj'
    f = open(fn,'w')
    f.write("""PROJCS["CH1903+_LV95",GEOGCS["GCS_CH1903+",DATUM["D_CH1903+",SPHEROID["Bessel_1841",6377397.155,299.1528128]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Hotine_Oblique_Mercator_Azimuth_Center"],PARAMETER["latitude_of_center",46.95240555555556],PARAMETER["longitude_of_center",7.439583333333333],PARAMETER["azimuth",90],PARAMETER["scale_factor",1],PARAMETER["false_easting",2600000],PARAMETER["false_northing",1200000],UNIT["Meter",1]]""")
    f.close()

        return None

def shapefileFromSplines(paarent,doc,fn = None):
    origine = doc[CONTAINER_ORIGIN]
    if not origine:
        print("pas d'origine")
        return

    if not paarent:
        print("pas d'objet' sélectionnée")
        return

    if not fn :
        fn = c4d.storage.LoadDialog(flags = c4d.FILESELECT_SAVE)
        if not fn : return

    polys = []
    for sp in parent.GetChildren():
        if not sp.CheckType(c4d.Ospline):
            return

        nb_seg = sp.GetSegmentCount()
        mg = sp.GetMg()
        pts = [p*mg+origine for p in sp.GetAllPoints()]
    
        #UN SEUL SEGMENT
        if not nb_seg :
            poly = [[[p.x,p.z,p.y] for p in pts]]
    
        #MULTISEGMENT (attention ne foncntionne pas avec segments interne à un autre)
        else:
            poly = []
            id_pt = 0
            for i in range(nb_seg):
                cnt = sp.GetSegment(i)['cnt']
                poly.append([[p.x,p.z,p.y] for p in pts[id_pt:id_pt+cnt]])
                id_pt +=cnt
        polys+=poly
    if not fn : return
    with shapefile.Writer(fn,shapefile.POLYGON) as w:
        w.field('id','I')
        w.field('name','I')
        for i,poly in enumerate(polys):
            
            w.field()
            w.record(1)
            w.poly(poly)

        fichierPRJ(fn)

def main():

    shapefileFromSplines(paarent,doc, buffer = 0)

if __name__=='__main__':
    main()