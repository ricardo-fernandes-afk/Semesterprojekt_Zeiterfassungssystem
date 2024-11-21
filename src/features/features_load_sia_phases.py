from db.db_connection import create_connection

def load_sia_phases():
    connection = create_connection()
    phases = []
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT phase_name FROM sia_phases")
        phases = cursor.fetchall()
        cursor.close()
        connection.close()
    return [phase[0] for phase in phases]  # Rückgabe einer Liste von Phasen