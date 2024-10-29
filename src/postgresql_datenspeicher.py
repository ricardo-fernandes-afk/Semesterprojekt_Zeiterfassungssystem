import psycopg2

try:
    connection = psycopg2.connect(
        user="postgres",
        password="Fcporto100%",
        host="127.0.0.1",
        port="5432",
        database="ARC-Zeiterfassung"
    )
    cursor = connection.cursor()
    print("Erfolgreich verbunden mit PostgreSQL")
except (Exception, psycopg2.Error) as error:
    print("Fehler bei der Verbindung:", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL-Verbindung geschlossen")