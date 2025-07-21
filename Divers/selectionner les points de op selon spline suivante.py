import c4d
from c4d import Vector

def point_in_polygon(point, polygon):
    """Vérifie si un point est à l'intérieur d'un polygone en utilisant l'algorithme du ray-casting."""
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0].x, polygon[0].z
    for i in range(n + 1):
        p2x, p2y = polygon[i % n].x, polygon[i % n].z
        if point.z > min(p1y, p2y):
            if point.z <= max(p1y, p2y):
                if point.x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (point.z - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or point.x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def main():
    # Récupérer l'objet sélectionné et la spline
    obj = doc.GetActiveObject()
    spline = obj.GetNext()

    if not obj or not spline:
        c4d.gui.MessageDialog("Veuillez sélectionner un objet et avoir une spline nommée 'Spline' dans la scène.")
        return

    # Vérifier que l'objet sélectionné est un PolygonObject
    if not isinstance(obj, c4d.PolygonObject):
        c4d.gui.MessageDialog("L'objet sélectionné doit être un objet polygonal.")
        return

    # Récupérer les points de l'objet dans l'espace monde
    points = obj.GetAllPoints()
    obj_mg = obj.GetMg()

    # Récupérer les points de la spline dans l'espace monde
    spline_points = spline.GetAllPoints()
    spline_mg = spline.GetMg()
    spline_points_world = [spline_mg * p for p in spline_points]

    # Créer une sélection de points
    point_selection = obj.GetPointS()
    point_selection.DeselectAll()

    # Pour chaque point de l'objet
    for i, point in enumerate(points):
        # Convertir le point en coordonnées monde
        world_point = obj_mg * point

        # Projeter le point sur le plan XZ (y = 0)
        projected_point = Vector(world_point.x, 0, world_point.z)

        # Vérifier si le point projeté est à l'intérieur de la spline
        if not point_in_polygon(projected_point, spline_points_world):
            point_selection.Select(i)

    # Mettre à jour l'objet
    #obj.SetPointS(point_selection)

    # Rafraîchir la vue
    c4d.EventAdd()

if __name__ == '__main__':
    main()