import socket


def validate_target(target):
    """
    Validate target hostname or IP.
    Returns resolved IP if valid.
    """

    try:
        target_ip = socket.gethostbyname(target)
        return target_ip
    except socket.gaierror:
        return None


def validate_ports(start_port, end_port):
    """
    Validate port range.
    """

    if start_port < 1:
        return False

    if end_port > 65535:
        return False

    if start_port > end_port:
        return False

    return True
