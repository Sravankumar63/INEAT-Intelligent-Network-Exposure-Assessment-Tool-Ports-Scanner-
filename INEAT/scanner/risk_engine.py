from scanner.service_loader import get_service_information


RISK_SCORES = {

    "LOW": 5,

    "MEDIUM": 10,

    "HIGH": 20,

    "CRITICAL": 30,

    "UNKNOWN": 0

}


def get_port_risk(port, protocol="TCP"):

    info = get_service_information(port, protocol)

    risk = info["risk"].upper()

    score = RISK_SCORES.get(risk, 0)

    return risk, score


def calculate_exposure_score(open_ports):

    total_score = 0

    for port in open_ports:

        _, score = get_port_risk(port)

        total_score += score

    if total_score > 100:
        total_score = 100

    return total_score


def overall_risk(score):

    if score >= 80:
        return "CRITICAL"

    elif score >= 60:
        return "HIGH"

    elif score >= 30:
        return "MEDIUM"

    else:
        return "LOW"
