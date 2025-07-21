import c4d

def sweep_plat(spline, epaisseur):
    sweep = c4d.BaseObject(c4d.Osweep)
    sweep[c4d.SWEEPOBJECT_BANKING] = False

    rect_epaisseur = c4d.BaseObject(c4d.Osplinerectangle)
    rect_epaisseur[c4d.PRIM_PLANE] = c4d.PRIM_PLANE_XY
    #res.SetRelPos(pos)
    rect_epaisseur[c4d.PRIM_RECTANGLE_WIDTH] = epaisseur
    rect_epaisseur[c4d.PRIM_RECTANGLE_HEIGHT] = 0
    rect_epaisseur.InsertUnder(sweep)
    spline.InsertUnder(sweep)
    rect_epaisseur.InsertUnder(sweep)
    return sweep


def subdivise_rect(rect,nb_pces_h,nb_pces_v, epaisseur_contour =2, epaisseur_separations = 1):
    larg = rect[c4d.PRIM_RECTANGLE_WIDTH]
    haut = rect[c4d.PRIM_RECTANGLE_HEIGHT]

    res = c4d.BaseObject(c4d.Onull)
    res.SetName(rect.GetName()+"_contour_et_separations")
    
    rect_clone = rect.GetClone()
    rect_clone.SetMl(c4d.Matrix())
    sweep_contour = sweep_plat(rect_clone, epaisseur_contour)
    sweep_contour.InsertUnder(res)

    sweep_separations = c4d.BaseObject(c4d.Osweep)
    sweep_separations[c4d.SWEEPOBJECT_BANKING] = False

    rect_epaisseur = c4d.BaseObject(c4d.Osplinerectangle)
    rect_epaisseur[c4d.PRIM_PLANE] = c4d.PRIM_PLANE_XY
    #res.SetRelPos(pos)
    rect_epaisseur[c4d.PRIM_RECTANGLE_WIDTH] = epaisseur_separations
    rect_epaisseur[c4d.PRIM_RECTANGLE_HEIGHT] = 0
    rect_epaisseur.InsertUnder(sweep_separations)

    connect = c4d.BaseObject(c4d.Oconnector)
    connect.InsertUnderLast(sweep_separations)


    # Création des subdivisions verticales
    for i in range(1, nb_pces_h):
        x_pos = (i * larg / nb_pces_h) -larg/2
        spline_v = c4d.SplineObject(2, c4d.SPLINETYPE_LINEAR)
        spline_v.SetName(f"v_{i}")
        spline_v.SetPoint(0, c4d.Vector(x_pos, 0, haut/2))
        spline_v.SetPoint(1, c4d.Vector(x_pos, 0, -haut/2))
        spline_v.InsertUnderLast(connect)

    # Création des subdivisions horizontales
    for j in range(1, nb_pces_v):
        z_pos = (j * haut / nb_pces_v) - haut/2
        spline_h = c4d.SplineObject(2, c4d.SPLINETYPE_LINEAR)
        spline_h.SetName(f"Subdivision_H_{j}")
        spline_h.SetPoint(0, c4d.Vector(-larg/2, 0, -z_pos))
        spline_h.SetPoint(1, c4d.Vector(larg/2, 0, -z_pos))
        spline_h.InsertUnderLast(connect)
    
    sweep_separations.InsertUnderLast(res)

    return res

def main():
    # Paramètres de configuration
    #larg = 120     # Largeur du rectangle
    #haut = 80      # Hauteur du rectangle
    nb_pces_h = 8  # Nombre de divisions horizontales
    nb_pces_v = 3  # Nombre de divisions verticales
    epaisseur_trait = 1
    
    rect = op

    sweep = subdivise_rect(rect,nb_pces_h,nb_pces_v, epaisseur_trait)
    sweep.InsertUnder(rect)
    # Mise à jour de la scène
    c4d.EventAdd()
    return

    # Création du rectangle principal
    rect = c4d.BaseObject(c4d.Osplinerectangle)
    rect[c4d.PRIM_PLANE] = c4d.PRIM_PLANE_XZ
    #res.SetRelPos(pos)
    rect[c4d.PRIM_RECTANGLE_WIDTH] = larg
    rect[c4d.PRIM_RECTANGLE_HEIGHT] = haut

    # Insertion dans le document
    doc.InsertObject(rect)

    # Création des subdivisions verticales
    for i in range(1, nb_pces_h):
        x_pos = i * larg / nb_pces_h
        spline_v = c4d.SplineObject(2, c4d.SPLINETYPE_LINEAR)
        spline_v.SetName(f"Subdivision_V_{i}")
        spline_v.SetPoint(0, c4d.Vector(x_pos, 0, 0))
        spline_v.SetPoint(1, c4d.Vector(x_pos, 0, -haut))
        spline_v.InsertUnder(rectangle)

    # Création des subdivisions horizontales
    for j in range(1, nb_pces_v):
        z_pos = j * haut / nb_pces_v
        spline_h = c4d.SplineObject(2, c4d.SPLINETYPE_LINEAR)
        spline_h.SetName(f"Subdivision_H_{j}")
        spline_h.SetPoint(0, c4d.Vector(0, 0, -z_pos))
        spline_h.SetPoint(1, c4d.Vector(larg, 0, -z_pos))
        spline_h.InsertUnder(rectangle)



if __name__ == '__main__':
    main()