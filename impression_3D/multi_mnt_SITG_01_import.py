import c4d
import urllib
from pathlib import Path

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


"""Sélectionner toutes les splines converties qui délimitent les zones à découper
   puis lancer le script
   Les MNT seront téléchargés dans un dossier MNT_Download à côté du fichier C4D
   Régler avant les constantes MAX_PX et URL_BASE
   MAX_PX est la taille maximale de l'image en pixel
   Ensuite il faut importer les MNT avec avec le script SIG/import MNT geotif dossier complet.py
   Puis découper les MNT avec le script multi_mnt_SITG_02_decoupe_selon_splines.py

   ATTENTION si on utilise le WorldElevation il faudra pour l'instant télécharger manuellement chaque url
   -> Lancer plutôt depuis Visual Studio Code parce qu'on peut cmd/cliquer sur les urls (se connecter avant)"""

CONTAINER_ORIGIN = 1026473

MAX_PX = 1024
URL_BASE = 'https://raster.sitg.ge.ch/arcgis/rest/services/MNA_SURFACE_COLLECTION/ImageServer'
URL_BASE = 'https://raster.sitg.ge.ch/arcgis/rest/services/MNA_TERRAIN_COLLECTION/ImageServer'

#
#URL_BASEC = 'https://elevation.arcgis.com/arcgis/rest/services/WorldElevation/Terrain/ImageServer'


def emprise_objet(obj, origin):
    """Calculates the bounding box of the given object.

    Args:
        obj: The object to calculate the bounding box for.
        origin: The origin of the bounding box.

    Returns:
        The bounding box of the object.
    """
    mg = obj.GetMg()
    pts = [p*mg for p in obj.GetAllPoints()]

    xmin = min([p.x for p in pts])+origin.x
    zmin = min([p.z for p in pts])+origin.z
    xmax = max([p.x for p in pts])+origin.x
    zmax = max([p.z for p in pts])+origin.z

    return xmin, zmin, xmax, zmax

def get_url(bbox,resol):
    xmin, ymin, xmax, ymax = bbox
    xmin,ymin,xmax,ymax = xmin - resol/2, ymin - resol/2, xmax + resol/2, ymax + resol/2
    bbox = f'{xmin},{ymin},{xmax},{ymax}'

    size_x = int(round((xmax-xmin)/resol))
    size_y = int(round((ymax-ymin)/resol))

    url = f'{URL_BASE}/exportImage?'
    params ={ 'bbox': bbox,
                'bboxSR': 2056,
                'size': f'{size_x},{size_y}',
                'imageSR': 2056,
                'format': 'tiff',
                'pixelType': 'F32',
                'f': 'image'}
    url += '&'.join([f'{k}={v}' for k,v in params.items()])
    return url

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    origin = doc[CONTAINER_ORIGIN]
    if not origin:
        c4d.gui.MessageDialog("No origin found.")
        return
    # Get the path of the current document.
    path = Path(doc.GetDocumentPath())
    if not path:
        c4d.gui.MessageDialog("Vous devez enregistrer le document avant.")
        return
    #create a folder for the TIFF files
    tiff_folder = path / 'MNT_Download'
    tiff_folder.mkdir(exist_ok=True)

    name_service = URL_BASE.split('/')[-2]

    for obj in doc.GetActiveObjects(0):
        bbox = None

        bbox = emprise_objet(obj, origin)

        if not bbox:
            print(f'No bounding box found for {obj.GetName()}.')
            continue
        xmin, zmin, xmax, zmax = bbox
        width = xmax - xmin
        height = zmax - zmin

        resol = max(width, height)/(MAX_PX-1) # j'enlève 1 pixel parce qu'on le rajoute après
        url = get_url(bbox, resol)
        print(url)

        name_img = f'{name_service}_{obj.GetName()}.tif'
        fn_tiff = tiff_folder / name_img
        # verify if the file already exists
        if fn_tiff.exists():
            print(f'{fn_tiff} already exists.')
            continue

        urllib.request.urlretrieve(url, fn_tiff)





if __name__ == '__main__':
    main()