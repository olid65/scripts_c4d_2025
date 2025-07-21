from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def test(cache, stop, indent = 0):
    while cache:
        print(indent*'--',cache.GetName(),cache.GetAbsRot())
        test(cache.GetDown(), stop, indent = indent+1)
        if cache == stop:
            break
        cache = cache.GetNext()

def getPhysicalSky(doc, obj = -1):
    if obj ==-1:
        obj = doc.GetFirstObject()

    while obj:
        if obj.CheckType(1011146): #physicalsky
            return obj
        sky = getPhysicalSky(doc, obj.GetDown())
        if sky : return sky

        obj = obj.GetNext()

    return None


def main() -> None:
    # Called when the plugin is selected by the user. Similar to CommandData.Execute.
    sky = getPhysicalSky(doc, obj = -1)
    if not sky:
        print('pas de ciel physique')
        return

    cache = sky.GetCache()
    sun = cache.GetDown().GetNext().GetDown()
    rot = sun.GetAbsRot()
    #test(cache, cache)

    c4d.CallCommand(1038653) # RS Sun & Sky Rig
    rs_sky = doc.GetFirstObject()

    if not rs_sky.CheckType(1036754) : # RS Sun & Sky Rig
        print('pas de rs_sky')
        return

    rs_sun = rs_sky.GetDown()

    if rs_sun:
        rs_sun.SetAbsRot(rot)
        
    #on desactive le ciel physique
    sky[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = False
    c4d.EventAdd()



"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()