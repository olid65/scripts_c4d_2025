from typing import Optional
import c4d
import redshift as rs
import os

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def main():
    pth = r"C:\Temp\BIBLIO_temp\Cordata_proxies"
    pth = c4d.storage.LoadDialog( title='', flags=c4d.FILESELECT_DIRECTORY)
    if not pth: return

    # pour le rs.Frsproxyexport -> j'ai trouvé dans
    #'C:\Program Files\Maxon Cinema 4D R26\Redshift\res\description\frsproxyexport.res
    plug = c4d.plugins.FindPlugin(rs.Frsproxyexport, c4d.PLUGINTYPE_SCENESAVER)
    if plug is None:
        raise RuntimeError("Failed to retrieve the alembic exporter.")

    data = dict()
    # Sends MSG_RETRIEVEPRIVATEDATA to Alembic export plugin
    if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
        raise RuntimeError("Failed to retrieve private data.")

    # BaseList2D object stored in "imexporter" key hold the settings
    rs_proxy_export = data.get("imexporter", None)
    if rs_proxy_export is None:
        raise RuntimeError("Failed to retrieve BaseContainer private data.")

    # Defines Alembic export settings
    rs_proxy_export[c4d.REDSHIFT_PROXYEXPORT_OBJECTS] = c4d.REDSHIFT_PROXYEXPORT_OBJECTS_SELECTION
    rs_proxy_export[c4d.REDSHIFT_PROXYEXPORT_EXPORT_COMPRESS] = True
    rs_proxy_export[c4d.REDSHIFT_PROXYEXPORT_EXPORT_LIGHTS] = False
    rs_proxy_export[c4d.REDSHIFT_PROXYEXPORT_SCALE] = doc[c4d.DOCUMENT_DOCUNIT]
    rs_proxy_export[c4d.REDSHIFT_PROXYEXPORT_ORIGIN] = c4d.REDSHIFT_PROXYEXPORT_ORIGIN_WORLD #or REDSHIFT_PROXYEXPORT_ORIGIN_OBJECTS
    rs_proxy_export[c4d.REDSHIFT_PROXYEXPORT_AUTOPROXY_CREATE] = True

    rs_proxy_export[c4d.REDSHIFT_PROXYEXPORT_AOV_DEFAULT_BEAUTY] = False
    rs_proxy_export[c4d.REDSHIFT_PROXYEXPORT_ANIMATION_RANGE] = c4d.REDSHIFT_PROXYEXPORT_ANIMATION_RANGE_CURRENT_FRAME

    #export par objet sélectionné
    for o in doc.GetActiveObjects(0):
        name = o.GetName()+'.rs'
        fn = os.path.join(pth,name)
        doc.SetActiveObject(o)
        # Finally export the document
        if not c4d.documents.SaveDocument(doc, fn, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, rs.Frsproxyexport):
            raise RuntimeError("Failed to save the document.")

        print("Document successfully exported to:", fn)


    return


def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED

if __name__ == '__main__':
    main()