import c4d
import math

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


#Il faudrait pour chaque caméra/beamer prendre la grille 1920x1080 et voir quel polygone
#est touché par le rayon pour créer le masque

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    cam = doc.GetFirstObject()
    cube = cam.GetNext()
    cube_inv_mat = ~ cube.GetMg()

    pt = cube.GetNext().GetMg().off * cube_inv_mat

    grc = c4d.utils.GeRayCollider()
    grc.Init( cube, force=False)

    pos_cam = cam.GetMg().off * cube_inv_mat

    ray_p = pos_cam
    ray_dir = pt-ray_p

    length = ray_dir.GetLength() *1000
    ray_dir.Normalize()

    if grc.Intersect(ray_p, ray_dir, length, only_test=False):
        res = grc.GetNearestIntersection()
        if res:
            print(res)
            f_normal = res['f_normal']
            angle = c4d.utils.GetAngle(ray_dir,f_normal)
            print(angle)
            #si l'angle est rasant -> 90°
            #si bien en face 180°
            print(c4d.utils.RadToDeg(angle))
            print(c4d.utils.RangeMap(angle, math.pi/2, math.pi, 0, 1, True   , None))


    else:
        print("Pas d'intersection")


if __name__ == '__main__':
    main()