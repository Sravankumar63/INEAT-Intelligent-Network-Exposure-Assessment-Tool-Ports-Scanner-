import sqlite3


DATABASE_NAME = "scan_history.db"


def get_scan_history(limit=10):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, target, open_ports, scan_duration
        FROM scan_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    return rows


def display_history():

    history = get_scan_history()

    print("\n")
    print("=" * 75)
    print("SCAN HISTORY")
    print("=" * 75)

    if not history:
        print("No Scan History Found.")
        print("=" * 75)
        return

    print(f"{'ID':<5}{'TARGET':<25}{'OPEN PORTS':<25}{'TIME(s)'}")
    print("-" * 75)

    for row in history:

        scan_id = row[0]
        target = row[1]
        ports = row[2]
        duration = row[3]

        print(f"{scan_id:<5}{target:<25}{ports:<25}{duration}")

    print("=" * 75)
