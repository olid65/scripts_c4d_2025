import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def sel_pts_inside_circle(circle,pts_2D, bs):
    center = circle.GetMp()+circle.GetMg().off
    center.y = 0
    rayon = circle.GetRad().x
    #print(center, rayon)
    
    for i,pt in enumerate(pts_2D):
        dist = c4d.Vector.GetDistance(center, pt)
        if dist <= rayon:
            bs.Select(i)

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    #circle = op
    obj_pts = op.GetNext()
    bs = obj_pts.GetPointS()
    bs.DeselectAll()
    mg = obj_pts.GetMg()
    v2d = lambda v : c4d.Vector(v.x,0,v.z)
    pts_2D = [v2d(p*mg) for p in obj_pts.GetAllPoints()]
    for circle in op.GetChildren():
        #print(circle)
        sel_pts_inside_circle(circle,pts_2D,bs)
    c4d.EventAdd()


if __name__ == '__main__':
    main()