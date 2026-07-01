import sqlite3
from datetime import datetime

DATABASE_NAME = "scan_history.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            target TEXT,

            scan_date TEXT,

            scan_time TEXT,

            open_ports TEXT,

            total_ports INTEGER,

            open_count INTEGER,

            scan_duration REAL

        )
    """)

    connection.commit()
    connection.close()


def save_scan(target,
              open_ports,
              total_ports,
              scan_duration):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    now = datetime.now()

    cursor.execute("""

        INSERT INTO scan_history(

        target,
        scan_date,
        scan_time,
        open_ports,
        total_ports,
        open_count,
        scan_duration)

        VALUES(?,?,?,?,?,?,?)

    """,(target,
         now.strftime("%d-%m-%Y"),
         now.strftime("%H:%M:%S"),
         ",".join(map(str,open_ports)),
         total_ports,
         len(open_ports),
         scan_duration))

    connection.commit()
    connection.close()
