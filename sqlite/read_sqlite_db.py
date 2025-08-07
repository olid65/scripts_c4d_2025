import c4d
from pathlib import Path
import sqlite3


doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    fn_db = Path(r"C:\Users\olivi\switchdrive\Mandats\Voie_verte\DOC\CFF200-61-AFS-T301-P01 Etats editions Voie Verte_OD_for_db.db")
    if not fn_db.exists():
        c4d.gui.MessageDialog(f"Database file not found: {fn_db}")
        return  
    
    try:
        conn = sqlite3.connect(fn_db)
        cursor = conn.cursor()

        # print all the tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(table[0])
        
        # Example: Fetching data from a specific table
        cursor.execute("SELECT * FROM editions LIMIT 10;")  # Adjust the table name
        rows = cursor.fetchall()
        print("Sample data from 'editions' table:")
        for row in rows:
            print(row)
        print('-' * 40 + "\n")
        # Print all columns in the 'editions' table
        cursor.execute("PRAGMA table_info(editions);")
        columns = cursor.fetchall()
        print("Columns in 'editions' table:")
        for column in columns:
            print(f"   {column[1]}, Type: {column[2]}")
    
    except sqlite3.Error as e:
        c4d.gui.MessageDialog(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")



if __name__ == '__main__':
    main()
