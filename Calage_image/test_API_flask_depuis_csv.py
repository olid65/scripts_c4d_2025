import c4d
import requests
from typing import List, Tuple, Dict, Any
import math
import csv

class CameraMatchCinema4D:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url.rstrip('/')

    def solve_camera(self,
                    points_2d: List[Tuple[float, float]],
                    points_3d: List[Tuple[float, float, float]],
                    image_size: Tuple[int, int],
                    distortion: List[float] = None) -> Dict[str, Any]:
        """
        Résout les paramètres de caméra et crée une caméra dans Cinema 4D

        Args:
            points_2d: Liste des points 2D dans l'image
            points_3d: Liste des points 3D correspondants
            image_size: Dimensions de l'image (largeur, hauteur)
            distortion: Paramètres de distorsion (optionnel)
        """
        payload = {
            "image_size": {
                "width": image_size[0],
                "height": image_size[1]
            },
            "points_2d": points_2d,
            "points_3d": points_3d
        }

        if distortion:
            payload["distortion"] = distortion

        try:
            response = requests.post(f"{self.api_url}/solve-camera", json=payload)
            response.raise_for_status()
            data = response.json()

            # Création de la caméra dans Cinema 4D
            self._create_camera_in_c4d(data)

            return data

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la communication avec l'API: {str(e)}")
            raise

    def _create_camera_in_c4d(self, camera_data: Dict[str, Any]):
        """Crée une caméra dans Cinema 4D avec les paramètres calculés"""
        # Création de la caméra
        camera = c4d.BaseObject(c4d.Ocamera)

        # Configuration de la focale
        camera[c4d.CAMERAOBJECT_FOV] = self._focal_length_to_fov(camera_data['focal_length'])


        # Configuration de la position
        pos = c4d.Vector(
            camera_data['position'][0],
            camera_data['position'][1],
            camera_data['position'][2]
        )
        camera.SetAbsPos(pos)

        # Configuration de la rotation
        # Conversion des angles d'Euler en radians
        rot = c4d.Vector(
            math.radians(camera_data['rotation'][0]),
            math.radians(camera_data['rotation'][1]),
            math.radians(camera_data['rotation'][2])
        )
        camera.SetAbsRot(rot)

        # Ajout de la caméra à la scène
        doc = c4d.documents.GetActiveDocument()
        doc.InsertObject(camera)

        # Mise à jour de la scène
        c4d.EventAdd()

        print(f"Caméra créée avec succès:")
        print(f"- Focale: {camera_data['focal_length']}mm")
        print(f"- Position: {camera_data['position']}")
        print(f"- Rotation: {camera_data['rotation']}")
        print(f"- Erreur de reprojection: {camera_data['reprojection_error']}")

    def _focal_length_to_fov(self, focal_length: float) -> float:
        """
        Convertit la focale en angle de champ de vision (FOV)
        pour Cinema 4D
        """
        # Formule simplifiée pour la conversion focale -> FOV
        # Pour une image de 36mm de large (format 35mm)
        fov = 2 * math.atan(18 / focal_length)
        return math.degrees(fov)


def main():
    fn = r"C:\Temp\pic2map_points.csv"

    points_2d = []
    points_3d = []

    # Ouvrir le fichier CSV
    with open(fn, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Utilisation de DictReader pour accéder aux colonnes par nom

        # Vérifier que les colonnes nécessaires sont présentes
        required_columns = {'x2d', 'y2d', 'X3d', 'Y3d', 'Z3d'}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"Le fichier CSV doit contenir les colonnes : {required_columns}")

        # Parcourir chaque ligne du fichier
        for row in reader:
            # Ajouter les tuples pour points_2d et points_3d
            points_2d.append((int(row['x2d']), int(row['y2d'])))
            points_3d.append((float(row['X3d']), float(row['Y3d']), float(row['Z3d'])))

    image_size = (1920, 1080)
    print(points_2d)
    print(points_3d)
    # Création de l'instance et résolution
    camera_match = CameraMatchCinema4D()
    result = camera_match.solve_camera(points_2d, points_3d, image_size)

    return

# Exemple d'utilisation
if __name__ == "__main__":
    main()