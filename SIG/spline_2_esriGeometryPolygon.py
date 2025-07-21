import c4d
from c4d import gui
from pprint import pprint


doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

CONTAINER_ORIGIN =1026473

def main() -> None:
    """Converts a spline object to an ESRI Geometry Polygon."""
    # Get the selected object.
    if op is None or not op.CheckType(c4d.Ospline):
        raise ValueError('Please select a spline object.')

    # Get the spline object.
    spline = op.GetRealSpline()
    if spline is None:
        raise ValueError('The spline object is empty.')

    origin = doc[CONTAINER_ORIGIN]
    if origin is None:
        raise ValueError('No origin found.')

    # Get the number of segments.
    nb_seg = spline.GetSegmentCount()
    mg = spline.GetMg()
    points = [p * mg + origin for p in spline.GetAllPoints()]

    # UN SEUL SEGMENT
    if not nb_seg:
        polygon = [[[p.x, p.z] for p in points]]

    # MULTISEGMENT (attention ne foncntionne pas avec segments interne à un autre)
    else:
        polygon = []
        id_pt = 0
        for i in range(nb_seg):
            cnt = spline.GetSegment(i)['cnt']
            polygon.append([[p.x, p.z] for p in points[id_pt:id_pt + cnt]])
            id_pt += cnt

    """exemple structure esriGeometryPolygon :
        {
          "rings": [
            [
              [-97.06138,32.837],
              [-97.06133,32.836],
              [-97.06124,32.834],
              [-97.06127,32.832],
              [-97.06138,32.837]
            ],
            [
              [-97.06326,32.759],
              [-97.06298,32.755],
              [-97.06153,32.749],
              [-97.06326,32.759]
            ]
          ],
          "spatialReference": {
            "wkid": 4326
          }
        }
        """
    esri_geometry_polygon = {
        "rings": polygon,
        "spatialReference": {
            "wkid": 2056
        }
    }

    pprint(esri_geometry_polygon)





if __name__ == '__main__':
    main()