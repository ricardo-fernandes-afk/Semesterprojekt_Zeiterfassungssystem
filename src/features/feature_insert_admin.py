def insert_admin(cursor): 
    start_admin = [("admin", 123, "admin")]
    
    try:
            
        for username, password, role in start_admin:
            cursor.execute('''
                INSERT INTO users (username, password, role)
                VALUES (%s, %s, %s)
                ON CONFLICT (username) DO NOTHING;
            ''', (username, password, role))
        print("Start Admin hinzugefügt")
        
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")