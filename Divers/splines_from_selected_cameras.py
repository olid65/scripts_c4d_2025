import c4d
from pathlib import Path
import math

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

DISTANCE = 250

def create_camera_fov_spline(cam):
    # Récupérer les paramètres de la caméra
    #fov = cam[c4d.CAMERAOBJECT_FOV]  # Champ de vision horizontal en radians
    fov = cam[c4d.RSCAMERAOBJECT_FOV].x
    print(fov)
    target_dist = DISTANCE  # Distance arbitraire pour la visualisation
    
    # Calculer la largeur du champ de vision à la distance cible
    half_width = math.tan(fov / 2) * target_dist
    
    # Position de la caméra (origine)
    cam_pos = cam.GetMg().off
    
    # Direction de visée
    cam_dir = cam.GetMg().v3
    
    # Vecteur perpendiculaire horizontal
    right = cam.GetMg().v1
    
    # Calculer les points extrêmes gauche/droit
    left_point = cam_pos + (cam_dir * target_dist) - (right * half_width)
    right_point = cam_pos + (cam_dir * target_dist) + (right * half_width)
    
    # Créer le spline avec 3 points
    spline = c4d.SplineObject(3, c4d.SPLINETYPE_LINEAR)
    spline.SetName(cam.GetName())
    spline.SetPoint(0, left_point)        # Point 0 : position caméra
    spline.SetPoint(1, cam_pos)     # Point 1 : extrémité gauche
    spline.SetPoint(2, right_point)    # Point 2 : extrémité droite
    
    # Configuration du spline
    spline[c4d.SPLINEOBJECT_CLOSED] = False

    spline.Message(c4d.MSG_UPDATE)
    
    return spline

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    
    cams = [o for o in doc.GetActiveObjectsFilter(True, c4d.Orscamera, c4d.NOTOK)]

    if not cams :
        c4d.gui.MessageDialog("Vous devez sélectionner au moins une caméra")
        return
    
    for cam in cams:
        sp = create_camera_fov_spline(cam)
        doc.InsertObject(sp)
        continue
        pos = cam.GetMg().off
        direction = cam.GetMg().v3
        angle = [c4d.RSCAMERAOBJECT_FOV][0]
        p = pos+direction*DISTANCE
        print(p)
        sp = c4d.SplineObject(2, c4d.SPLINETYPE_LINEAR)
        pts = [c4d.Vector(pos),p]
        sp.SetAllPoints(pts)
        sp.Message(c4d.MSG_UPDATE)
        print(sp)
        doc.InsertObject(sp)
    c4d.EventAdd()
    return
    pth = Path(r"C:\Users\olivi\switchdrive\Mandats\Facade_sud_GVA_Cointrin\Rendus\20250623_maquette_par_piece")

    for file in pth.glob('*.jpg'):
        if '0001' in file.stem:
            new_name = file.stem.replace('0001', '') + file.suffix
            new_path = file.with_name(new_name)
            file.rename(new_path)
            print(f"Renamed: {file.name} -> {new_name}")

if __name__ == '__main__':
    main()