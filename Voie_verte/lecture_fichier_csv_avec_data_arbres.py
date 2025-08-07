import c4d
import csv

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

CONTAINER_ORIGIN = 1026473


def main() -> None:
    origin = doc[CONTAINER_ORIGIN]
    res = c4d.BaseObject(c4d.Onull)
    fn = r"C:\Users\olivi\switchdrive\Mandats\Voie_verte\DOC\CFF200-61-AFS-T301-P01 Etats editions Voie Verte_OD.csv"
    # Remplace "fichier.csv" par le nom de ton fichier
    with open(fn, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            x = float(row['X'])
            y = float(row['Y'])
            pos = c4d.Vector(x,0,y)-origin
            obj = c4d.BaseObject(c4d.Oinstance)
            obj.SetAbsPos(pos)
            obj.SetName(f"{row['Numero']}_{row['Nom']}_{row['Class_height']}")
            obj.InsertUnderLast(res)
    doc.InsertObject(res)
    c4d.EventAdd()    


if __name__ == '__main__':
    main()