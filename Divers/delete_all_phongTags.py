import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


def suppr_PhongTags(obj,stop = None):
    while obj:
        for t in obj.GetTags():
            if t.CheckType(c4d.Tphong):
                t.Remove()
        suppr_PhongTags(obj.GetDown(),stop)
        obj = obj.GetNext()
        if obj == stop:
            break

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    suppr_PhongTags(op,stop = op.GetNext())
    
    c4d.EventAdd()


if __name__ == '__main__':
    main()