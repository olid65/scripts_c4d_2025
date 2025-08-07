import c4d
from random import random as rdm

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


"""l'objet source doit faire 10m de haut"""
def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    dico = {'5 - 9 m': (5,9), 
            'inf 5 m' : (2,5), 
            '10 - 14 m': (10,14)
    }
    for o in op.GetChildren():
        class_height = o.GetName().split('_')[-1]
        if class_height:
            mini,maxi = dico[class_height]
            height = (mini + rdm()*(maxi-mini))/10
            scale = c4d.Vector(height)
            o.SetAbsScale(scale)
        else:
            print(o.GetName())
            
    c4d.EventAdd()
            


if __name__ == '__main__':
    main()