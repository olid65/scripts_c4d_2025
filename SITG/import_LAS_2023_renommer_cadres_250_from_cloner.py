import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

CONTAINER_ORIGIN = 1026473

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    origin = doc[CONTAINER_ORIGIN]
    lst_to_remove = []

    for o in op.GetChildren():
        #Lorsqu'on utilise un cloner avec effecteur simple avec une scale de -1
        #les clones arrivent avec une scale de 0
        #on les supprime
        if o.GetRelScale() == c4d.Vector(0):
            o.Remove()
            continue
        pos = o.GetMg().off + origin
        o.SetName(f'{round(pos.x)}_{round(pos.z)}.las')
    c4d.EventAdd()


if __name__ == '__main__':
    main()