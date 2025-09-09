from typing import Optional
import c4d
from c4d.utils import GeRayCollider
import math

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected


def get_visble_points_in_renderview(doc, op, bd, cam):

    if bd.GetFrame()!= bd.GetSafeFrame():
        rep = c4d.gui.MessageDialog("Attention la fenêtre de rendu n'est pas ajustée à la fenêtre visible, voulez vous continuer ?")
        if not rep : return
    res = []    
    for i,p in enumerate(op.GetAllPoints()):
        pt = bd.WS(p)
        if bd.TestPoint(pt.x,pt.y): 
            #bs.Select(i)
            res.append(i)
    return res


def find_visible_polys(op, pts_visible):
    polys = op.GetAllPolygons()
    visible_polys_ids = []
    for i, poly in enumerate(polys):
        # poly = c4d.CPolygon(a, b, c, d)
        indices = [poly.a, poly.b, poly.c]
        if hasattr(poly, 'd'):  # si quad
            indices.append(poly.d)
        if any(pt in pts_visible for pt in indices):
            visible_polys_ids.append(i)
    return visible_polys_ids

def get_poly_visibility_and_angle(op, poly_id, cam, rc):
    poly = op.GetPolygon(poly_id)

    p1 = op.GetPoint(poly.a)
    p2 = op.GetPoint(poly.b)
    p3 = op.GetPoint(poly.c)
    if poly.c == poly.d:
        center = (p1 + p2 + p3) / 3.0
    else:
        p4 = op.GetPoint(poly.d)
        center = (p1 + p2 + p3 + p4) / 4.0
    #center = center * op.GetMg()
    cam_pos = cam.GetMg().off
    direction = (center-cam_pos).GetNormalized()
    length = (center - cam_pos).GetLength()
    print(direction,length)
    if rc.Intersect(cam_pos, direction, length*1000):
        intersection = rc.GetIntersection(0)
        print(poly_id, intersection)
        if intersection["face_id"] == poly_id:
            return True
    return False


def main() -> None:
    
    bd = doc.GetRenderBaseDraw()
    cam = bd.GetSceneCamera(doc)
    print(cam.GetName())
    
    pts_visible = get_visble_points_in_renderview(doc, op, bd, cam)
    #bs = op.GetPointS()
    #bs.DeselectAll()
    #
    #for i in pts_visible:
        #bs.Select(i)
    # Initialisation unique du GeRayCollider
    
    rc = GeRayCollider()
    rc.Init(op, True)
            
    poly_ids = find_visible_polys(op, pts_visible)
    #sel_tag = c4d.SelectionTag(c4d.Tpolygonselection)
    #bc = sel_tag.GetBaseSelect()
    bs = op.GetPolygonS()
    bs.DeselectAll()

    for poly_id in poly_ids:
        if get_poly_visibility_and_angle(op, poly_id, cam, rc):
            #bc.Select(poly_id)
            bs.Select(poly_id)

    #op.InsertTag(sel_tag)
    c4d.EventAdd()

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()