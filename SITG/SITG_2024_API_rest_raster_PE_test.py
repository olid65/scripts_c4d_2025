import c4d
import requests
import json
from pathlib import Path


doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

"""MARCHE PAS !!!!"""
def main():
    # Paramètres
    service_url = "https://raster.sitg.ge.ch/arcgis/rest/services/CARTES_HISTORIQUES_PLAN_BASE_ARCHIVE_1936_2002/ImageServer"
    bbox = (2496057.25, 1111912.75, 2500057.25, 1114912.75)  # BBox en projet 2056

    xmin,ymin,xmax,ymax = bbox
    largeur  = int(round((xmax-xmin)*0.25))
    hauteur = int(round((ymax-ymin)*0.25))

    geometry = {
        "xmin": bbox[0],
        "ymin": bbox[1],
        "xmax": bbox[2],
        "ymax": bbox[3],
        "spatialReference": {"wkid": 2056}
    }

    params = {
        "f": "json",
        "where": "1=1",
        "geometry": str(geometry),
        "geometryType": "esriGeometryEnvelope",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "DATE",
        "returnGeometry": False,
        "returnDistinctValues": True
    }

    response = requests.get(service_url + "/query", params=params)
    response.raise_for_status()
    data = response.json()

    # Conversion des timestamps en dates lisibles
    from datetime import datetime

    dates = []
    if "features" in data:
        for feature in data["features"]:
            ts = feature["attributes"].get("DATE")
            # Les valeurs DATE d’ESRI sont en millisecondes depuis 1970-01-01
            if ts > 0:
                date = datetime.utcfromtimestamp(ts / 1000)
                dates.append((date.strftime("%Y"),ts))
                print(date.strftime("%Y"))
    dates = sorted(set(dates))

    # Assurez-vous que le dossier existe
    pth = Path(r"C:\Temp\test_SITG_raster")
    pth.mkdir(parents=True, exist_ok=True)

    for an, ts in dates:
        mosaic_rule = {
            "mosaicMethod": "esriMosaicAttribute",  # Changed from esriMosaicNone
            "sortField": "DATE",
            "sortValue": ts,  # Ajout du sortValue
            "ascending": True,
            "where": f"DATE = {ts}"
        }

        export_params = {
            "f": "image",
            "bbox": ",".join(map(str, bbox)),  # Utilisation de map() pour la conversion
            "bboxSR": 2056,
            "imageSR": 2056,
            "size": f"{largeur},{hauteur}",
            "format": "tiff",  # Changed from tif to tiff
            "pixelType": "U8",  # Spécifier le type de pixel
            "noDataInterpretation": "esriNoDataMatchAny",
            "interpolation": "RSP_BilinearInterpolation",
            "compression": "LZW",
            "mosaicRule": json.dumps(mosaic_rule)
        }

        resp = requests.get(service_url + "/exportImage", params=export_params, stream=True)
        
        # Debug information
        print(f"URL: {resp.url}")
        print(f"Status: {resp.status_code}")
        print(f"Headers: {resp.headers}")
        
        fn = pth/f"{an}.tiff"  # Changed extension to tiff
        
        if resp.status_code == 200 and resp.headers.get('content-type', '').startswith('image/'):
            with open(fn, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Image sauvegardée : {fn}")
        else:
            print(f"Erreur lors du téléchargement : {resp.status_code}")
            print(f"Message d'erreur : {resp.text}")
        



if __name__ == '__main__':
    main()