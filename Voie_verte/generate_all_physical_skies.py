import c4d
from datetime import datetime

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

"""Sélectionner un ciel physique des base avec les bonnes coordonnées"""

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    mois = [6,7,8,9]
    heures = [10,13,17]
    
    res = c4d.BaseObject(c4d.Onull)
    for m in mois:
        for h in heures:
            clone = op.GetClone()
            clone.SetName(f"15/{m}_{h}h")
            
            dtd = clone[c4d.SKY_DATE_TIME]
            date_heure = f'15.{m}.2025 {h}:00:00'
            # Parse the time string
            dt = datetime.strptime(date_heure,"%d.%m.%Y %H:%M:%S")
        
            # Fills the Data object with the DateTime object
            dtd.SetDateTime(dt)
            clone[c4d.SKY_DATE_TIME] = dtd
            
            clone.InsertUnderLast(res)
    doc.InsertObject(res)        
    c4d.EventAdd()        



if __name__ == '__main__':
    main()