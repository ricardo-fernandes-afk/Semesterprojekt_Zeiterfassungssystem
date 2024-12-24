def insert_sia_phases(cursor): 
    sia_phases = [
        (2, "Vorstudien"),
        (3, "Projektierung"),
        (4, "Ausschreibung"),
        (5, "Realisierung")
    ]
    
    try:
            
        for phase_number, phase_name in sia_phases:
            cursor.execute('''
                INSERT INTO sia_phases (phase_number, phase_name)
                VALUES (%s, %s)
                ON CONFLICT (phase_number) DO NOTHING;
            ''', (phase_number, phase_name))
        print("SIA phases erfolgreich hinzugefügt!")
        
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")