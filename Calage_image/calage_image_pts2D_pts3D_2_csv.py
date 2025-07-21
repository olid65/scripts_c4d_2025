import c4d

import csv
from pathlib import Path

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

""" Il faut un plan image à plat sur le sol (importer l'image avec "Importer une image"
    dans ext. swisstopo
    ATTENTION mettre l'axe de l'image en haut à gauche !!!!!!'
    en enfant de ce plan on doit trouver au moins 6 points 2D sous forme de onull
    placé sur l'image

    Les points 3D correspondants doivent être placés en enfant de l'objet sivant le plsn
    et placés dans le même ordre que les points 2D
    et il doit en avoir le même nombre """


def export_to_pic2map(pts_2d, pts_3d, output_file):
    """
    Exporte les points 2D et 3D de Cinema 4D vers un fichier CSV pour pic2map_app.

    Args:
        pts_2d: Liste de tuples (x, y) représentant les points 2D en pixels
        pts_3d: Liste de tuples (x, y, z) représentant les points 3D en unités réelles
        output_file: Chemin du fichier CSV de sortie (par défaut: "pic2map_points.csv")

    Returns:
        bool: True si l'export a réussi, False sinon
    """
    # Vérification des données
    if len(pts_2d) != len(pts_3d):
        print(f"Erreur: Le nombre de points 2D ({len(pts_2d)}) ne correspond pas au nombre de points 3D ({len(pts_3d)})")
        return False

    if len(pts_2d) < 6:
        print("Attention: Il faut au moins 6 points pour calculer la position de la caméra")

    try:
        # Conversion du chemin en objet Path
        output_path = Path(output_file)

        # Création du fichier CSV
        with output_path.open('w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # En-tête du fichier
            writer.writerow(['x2d', 'y2d', 'X3d', 'Y3d', 'Z3d'])

            # Écriture des points
            for i in range(len(pts_2d)):
                x2d, y2d = pts_2d[i]
                x3d, y3d, z3d = pts_3d[i]

                # Vérification que les coordonnées 2D sont positives
                if x2d < 0 or y2d < 0:
                    print(f"Attention: Point 2D {i} ({x2d}, {y2d}) a des coordonnées négatives")

                writer.writerow([x2d, y2d, x3d, y3d, z3d])

        print(f"Fichier CSV créé avec succès: {output_path.absolute()}")
        print(f"Nombre de points exportés: {len(pts_2d)}")
        return True

    except Exception as e:
        print(f"Erreur lors de l'export: {str(e)}")
        return False


def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    print(op)
    if not op:
        print("sélectionner lle plan avec l'image")
        return
    tag = op.GetTag(c4d.Ttexture)
    if not tag:
        print('Pas de tag texture')
        return
    mat = tag[c4d.TEXTURETAG_MATERIAL]
    if not mat:
        print('Pas de materiau associé au tag')
        return
    fn_img = None
    shd = mat.GetFirstShader()
    
    while shd:
        if shd.CheckType(c4d.Xbitmap):
            print(shd[c4d.BITMAPSHADER_FILENAME])
            fn_img = shd[c4d.BITMAPSHADER_FILENAME]
            break

        shd = shd.GetNext()
    print(fn_img)
    if fn_img:
        # Chargement de l'image
        bmp = c4d.bitmaps.BaseBitmap()
        if bmp.InitWith(fn_img)[0] != c4d.IMAGERESULT_OK:
            print("Image_pas_ok")
            #TODO : gerer les chemins relatifs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            w,h = 1920,1080

        else:
            w,h = bmp.GetSize()
    
    size_plane = op.GetRad()*2
    w_plane = size_plane.x
    h_plane = size_plane.z
    print()
    #print(op.GetMp())
    pts_2D = []
    for p in op.GetChildren():
        pos = p.GetRelPos()
        p2D_x = int(round(pos.x*w/w_plane))
        p2D_y = int(round(-pos.z*h/h_plane))
        pts_2D.append((p2D_x, p2D_y))
    print(pts_2D)

    f = lambda v : (v.x,v.y,v.z)
    pts_3D = [f(p.GetMg().off) for p in op.GetNext().GetChildren()]
    print(pts_3D)

    #export csv
    fn_csv = Path(doc.GetDocumentPath())/"pic2map_points.csv"
    print(fn_csv)
    export_to_pic2map(pts_2D, pts_3D, fn_csv)



if __name__ == '__main__':
    main()