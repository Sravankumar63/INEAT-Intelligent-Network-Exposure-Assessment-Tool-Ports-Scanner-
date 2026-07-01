import sqlite3

DATABASE_NAME = "scan_history.db"


def get_previous_open_port_count(target):

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
        return 0

    if row[0] == "":
        return 0

    return len(row[0].split(","))


def show_exposure_trend(previous_count, current_count):

    print("\nEXPOSURE TREND")
    print("-" * 30)

    print(f"Previous Scan : {previous_count} Open Ports")
    print(f"Current Scan  : {current_count} Open Ports")

    if current_count > previous_count:
        print(f"\nExposure Increased (+{current_count - previous_count})")

    elif current_count < previous_count:
        print(f"\nExposure Reduced (-{previous_count - current_count})")

    else:
        print("\nNo Change in Exposure")
