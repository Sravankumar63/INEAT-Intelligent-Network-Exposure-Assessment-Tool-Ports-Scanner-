from scanner.service_loader import get_service_information


def get_service(port, protocol="TCP"):

    info = get_service_information(port, protocol)

    return {
        "service": info["service"],
        "protocol": protocol,
        "description": info["description"],
        "category": info["category"],
        "risk": info["risk"],
        "recommendation": info["recommendation"]
    }
