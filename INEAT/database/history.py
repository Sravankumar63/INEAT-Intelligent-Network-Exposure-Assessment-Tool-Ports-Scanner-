import sqlite3


DATABASE_NAME = "scan_history.db"


def get_previous_ports(target):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""

        SELECT open_ports

        FROM scan_history

        WHERE target=?

        ORDER BY id DESC

        LIMIT 1 OFFSET 1

    """, (target,))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return []

    if row[0] == "":
        return []

    return list(map(int, row[0].split(",")))


def compare_scans(previous_ports, current_ports):

    previous = set(previous_ports)

    current = set(current_ports)

    new_ports = sorted(list(current - previous))

    closed_ports = sorted(list(previous - current))

    return new_ports, closed_ports
