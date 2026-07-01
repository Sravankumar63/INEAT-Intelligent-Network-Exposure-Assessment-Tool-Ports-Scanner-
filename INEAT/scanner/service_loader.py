import csv
import os

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IANA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "service-names-port-numbers.csv"
)

INEAT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "ineat_services.csv"
)

# ==========================================================
# Dictionaries
# ==========================================================

IANA_SERVICES = {}

INEAT_SERVICES = {}

# ==========================================================
# Load IANA Dataset
# ==========================================================

with open(IANA_FILE, encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        try:

            port = int(row["Port Number"])

            protocol = row["Transport Protocol"]

            service = row["Service Name"]

            description = row["Description"]

            IANA_SERVICES[(port, protocol.upper())] = {

                "service": service,
                "description": description

            }

        except:

            pass

# ==========================================================
# Load INEAT Dataset
# ==========================================================

with open(INEAT_FILE, encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        try:

            port = int(row["Port"])

            protocol = row["Protocol"]

            INEAT_SERVICES[(port, protocol.upper())] = {

                "risk": row["Risk"],

                "category": row["Category"],

                "recommendation": row["Recommendation"]

            }

        except:

            pass


# ==========================================================
# Combined Lookup
# ==========================================================

def get_service_information(port, protocol="TCP"):

    protocol = protocol.upper()

    iana = IANA_SERVICES.get((port, protocol), {})

    ineat = INEAT_SERVICES.get((port, protocol), {})

    return {

        "service": iana.get("service", "Unknown"),

        "description": iana.get("description", "No Description"),

        "risk": ineat.get("risk", "Unknown"),

        "category": ineat.get("category", "Unknown"),

        "recommendation": ineat.get(
            "recommendation",
            "No Recommendation"
        )

    }
