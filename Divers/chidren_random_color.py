import c4d
from random import random

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    nb = len(op.GetChildren())
    indent = 1/nb
    h = 0
    for o in op.GetChildren():
        o[c4d.ID_BASEOBJECT_USECOLOR] = c4d.ID_BASEOBJECT_USECOLOR_ALWAYS
        color = c4d.utils.HSVToRGB(c4d.Vector(random(),0.5,1))
        #color = c4d.utils.HSVToRGB(c4d.Vector(h,0.5,1))
        o[c4d.ID_BASEOBJECT_COLOR] = color
        h+= indent

    c4d.EventAdd()
if __name__ == '__main__':
    main()