from scanner.service_loader import get_service_information


def get_recommendations(port, protocol="TCP"):

    info = get_service_information(port, protocol)

    recommendation = info["recommendation"]

    if recommendation.strip() == "":
        return [
            "Review this service manually.",
            "Close the port if it is unnecessary."
        ]

    return [
        item.strip()
        for item in recommendation.split(";")
        if item.strip()
    ]
