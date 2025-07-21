from typing import Optional
import c4d
import os
from glob import glob

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def main() -> None:
    pth = c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY)
    #pth = r'C:\Users\olivier.donze\switchdrive\C4D\BIBLIOTHEQUE\Redshift_proxies'

    for fn in sorted(glob(os.path.join(pth,'*.rs')),reverse=True):
        c4d.documents.MergeDocument(doc, fn,
                                    c4d.SCENEFILTER_OBJECTS |
                                    c4d.SCENEFILTER_MATERIALS |
                                    c4d.SCENEFILTER_MERGESCENE, None)
    c4d.StatusClear()
    c4d.EventAdd()


"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()