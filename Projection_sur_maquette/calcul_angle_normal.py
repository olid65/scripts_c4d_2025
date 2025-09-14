import c4d
from c4d import gui
from collections import defaultdict
from typing import Tuple, List
import math

doc: c4d.documents.BaseDocument
op: c4d.BaseObject | None

OcamerasRS = 1057516
TAG_NON_VISIBLES = "polygones_non_visibles"

def get_camera_fov(camera: c4d.BaseObject) -> Tuple[float, float]:
    """Retourne les angles horizontaux et verticaux de la caméra en radians"""
    if camera.CheckType(OcamerasRS):
        fov = camera[c4d.RSCAMERAOBJECT_FOV]
        return fov.x, fov.y
    else:
        return (camera[c4d.CAMERAOBJECT_FOV], 
                camera[c4d.CAMERAOBJECT_FOV_VERTICAL])

def is_point_in_camera_view(point: c4d.Vector, camera: c4d.BaseObject) -> bool:
    """Vérifie si un point est dans le champ de vision de la caméra"""
    cam_mg = camera.GetMg()
    point_local = point * ~cam_mg
    
    # Si le point est derrière la caméra, il n'est pas visible
    if point_local.z < 0:  # Changé de > à <
        print(f"Point {point} is behind camera {camera.GetName()}")
        return False
        
    # Calcul des angles de vue
    fov_h, fov_v = get_camera_fov(camera)
    
    # Pour éviter la division par zéro
    if abs(point_local.z) < 0.0001:
        return False
    
    # Calcul des ratios x/z et y/z (équivalent à tan(angle))
    ratio_h = abs(point_local.x / point_local.z)  # Supprimé le -
    ratio_v = abs(point_local.y / point_local.z)  # Supprimé le -
    
    # Comparaison avec les tangentes des demi-angles de vue
    tan_fov_h = math.tan(fov_h/2)
    tan_fov_v = math.tan(fov_v/2)
    
    # print(f"Camera: {camera.GetName()}")
    # print(f"Point local: {point_local}")
    # print(f"Ratios H/V: {ratio_h}, {ratio_v}")
    # print(f"Tan FOV H/V: {tan_fov_h}, {tan_fov_v}")
    
    return ratio_h <= tan_fov_h and ratio_v <= tan_fov_v

def is_point_visible(point: c4d.Vector, camera: c4d.BaseObject, 
                    rayCollider: c4d.utils.GeRayCollider, exclude_poly_id: int) -> bool:
    """Vérifie si un point est visible depuis la caméra sans obstacles"""
    # Utilisation de la matrice globale de la caméra
    cam_mg = camera.GetMg()
    cam_pos = cam_mg.off
    
    # Direction du rayon (de la caméra vers le point)
    direction = (point - cam_pos).GetNormalized()
    
    # Test de collision avec la distance exacte
    length = (point - cam_pos).GetLength()
    
    # Ajout d'un petit offset pour éviter les problèmes numériques
    ray = cam_pos + direction * 0.001
    length = length - 0.002
    
    # Test d'intersection
    if rayCollider.Intersect(ray, direction, length):
        poly_id = rayCollider.GetNearestIntersection()["face_id"]
        return poly_id == exclude_poly_id
    
    return True

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    # Vérification que l'objet sélectionné est un objet polygonal
    if not op or not op.CheckType(c4d.Opolygon):
        gui.MessageDialog('Veuillez sélectionner un objet polygonal.')
        return

    # Vérification qu'un objet null suit l'objet polygonal
    if not op.GetNext():
        gui.MessageDialog("Veuillez placer un objet null après l'objet polygonal.")
        return

    # Récupération des caméras
    cameras = [cam for cam in op.GetNext().GetChildren() if cam.CheckType(c4d.Ocamera) or cam.CheckType(OcamerasRS)]
    if not cameras:
        gui.MessageDialog("Aucune caméra trouvée dans l\'objet null.")
        return

    # Vérification des noms uniques des caméras
    camera_names = [cam.GetName() for cam in cameras]
    if len(camera_names) != len(set(camera_names)):
        gui.MessageDialog("Toutes les caméras doivent avoir des noms différents.")
        return

    cameras_pos = [cam.GetMg().off for cam in cameras]
    mg = op.GetMg()
    
    # Dictionnaire pour stocker les polygones par caméra
    camera_poly_dict = defaultdict(list)
    # Liste pour les polygones non visibles
    non_visible_polys = []
    
    # Début de l'action d'annulation
    doc.StartUndo()
    
    # Initialisation du rayCollider une seule fois
    rayCollider = c4d.utils.GeRayCollider()
    if not rayCollider.Init(op):
        gui.MessageDialog("Erreur lors de l'initialisation du RayCollider.")
        return
    
    # On parcourt tous les polygones de l'objet
    for poly_id, poly in enumerate(op.GetAllPolygons()):
        #on recupere les points du polygone
        p1 = op.GetPoint(poly.a)*mg
        p2 = op.GetPoint(poly.b)*mg
        p3 = op.GetPoint(poly.c)*mg
        if poly.c != poly.d:
            p4 = op.GetPoint(poly.d)*mg
            #on calcule le centre du polygone
            center = (p1 + p2 + p3 + p4) / 4
            #on calcule la normale du polygone
            normal = c4d.Vector.Cross(p2 - p1, p4 - p1).GetNormalized()
        else:
            #on calcule le centre du polygone
            center = (p1 + p2 + p3) / 3

            #on calcule la normale du polygone
            normal = c4d.Vector.Cross(p2 - p1, p3 - p1).GetNormalized()

        # On stocke l'angle minimal pour chaque caméra
        min_angle = float('inf')
        best_cam = None

        # On calcule et trie les angles pour toutes les caméras
        cam_angles = []
        for cam, cam_pos in zip(cameras, cameras_pos):
            to_cam = (cam_pos - center).GetNormalized()
            angle = c4d.utils.RadToDeg(c4d.utils.GetAngle(normal, to_cam))
            cam_angles.append((angle, cam))
            
        # Tri par angle croissant
        cam_angles.sort(key=lambda x: x[0])
        
        # Test de chaque caméra dans l'ordre
        polygon_assigned = False
        for angle, cam in cam_angles:
            in_view = is_point_in_camera_view(center, cam)
            if in_view:
                is_visible = is_point_visible(center, cam, rayCollider, poly_id)
                if is_visible:
                    camera_poly_dict[cam].append(poly_id)
                    polygon_assigned = True
                    break
    
    # Création des tags de sélection pour chaque caméra
    for cam, poly_list in camera_poly_dict.items():
        print(f"Camera {cam.GetName()}: {len(poly_list)} polygons")
        print(f"Polygon IDs: {poly_list}")

        # Création du tag de sélection
        tag = c4d.SelectionTag(c4d.Tpolygonselection)
        tag.SetName(cam.GetName())

        # Configuration de la sélection
        baseSelect = tag.GetBaseSelect()
        for poly_id in poly_list:
            baseSelect.Select(poly_id)

        # Ajout du tag à l'objet avec Undo
        doc.AddUndo(c4d.UNDOTYPE_NEW, tag)
        op.InsertTag(tag)

    # Création du tag pour les polygones non visibles
    if non_visible_polys:
        tag = c4d.SelectionTag(c4d.Tpolygonselection)
        tag.SetName(TAG_NON_VISIBLES)
        baseSelect = tag.GetBaseSelect()
        for poly_id in non_visible_polys:
            baseSelect.Select(poly_id)
        doc.AddUndo(c4d.UNDOTYPE_NEW, tag)
        op.InsertTag(tag)
        print(f"Polygones non visibles: {len(non_visible_polys)}")
        print(f"IDs: {non_visible_polys}")
    
    # Fin de l'action d'annulation
    doc.EndUndo()

    c4d.EventAdd()

if __name__ == '__main__':
    main()