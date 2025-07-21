import c4d
import sys
from math import floor

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


#Sélectionner le neutre contenant les pièces terrain à extruder
#Régler l'échelle et l'épaisseur minimale de la maquette'
ech = 2500
epaisseur_min = 3 #épaisseur minmale en mm


def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    ymin = sys.float_info.max
    ymax = sys.float_info.min
    for o in op.GetChildren():
        mg = o.GetMg()
        f = lambda v : (v*mg).y
        ys = [f(p) for p in o.GetAllPoints()]
        ymin_temp = min(ys)
        if ymin> ymin_temp:
            ymin = ymin_temp
        ymax_temp =  max(ys)
        if ymax < ymax_temp:
            ymax = ymax_temp
    print(ymin,ymax)
    alt_base = floor(ymin - (epaisseur_min/1000*ech))
    print(alt_base)

    print(f"Epaiseur min : {round((ymin-alt_base)/ech*1000,1)} mm")
    print(f"Epaiseur max : {round((ymax-alt_base)/ech*1000,1)} mm")



if __name__ == '__main__':
    main()