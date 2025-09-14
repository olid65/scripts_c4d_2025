import c4d
from pathlib import Path

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

"""Pour renommer une série d'images, par exemple si on a fait une sur deux, pour que la numérotation suive"""


def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    pth = Path(r"C:\Temp\RHONE_rendus_temp\Maquette_10k\Test_rain")
    
    for i,fn in enumerate(sorted(pth.glob('*.png'))):
        #print(fn.parent)
        new_name = fn.stem[:-4]+str(i).zfill(4)+fn.suffix
        new_fn = Path(fn.parent/new_name)
        fn.rename(new_fn)

if __name__ == '__main__':
    main()