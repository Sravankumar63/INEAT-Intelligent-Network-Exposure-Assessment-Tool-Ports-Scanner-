import sqlite3

DATABASE_NAME = "scan_history.db"


def detect_changes(target, current_ports):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT open_ports
        FROM scan_history
        WHERE target=?
        ORDER BY id DESC
        LIMIT 1
    """, (target,))

    row = cursor.fetchone()

    connection.close()

    if row is None or row[0] == "":
        previous_ports = []

    else:
        previous_ports = list(map(int, row[0].split(",")))

    new_ports = list(set(current_ports) - set(previous_ports))

    closed_ports = list(set(previous_ports) - set(current_ports))

    return sorted(new_ports), sorted(closed_ports)
