import socket
from concurrent.futures import ThreadPoolExecutor
from scanner.config import TIMEOUT, MAX_THREADS

open_ports = []


def scan_single_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            open_ports.append(port)

        sock.close()

    except:
        pass


def scan_ports(target_ip, start_port, end_port):

    open_ports.clear()

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(
            lambda port: scan_single_port(target_ip, port),
            range(start_port, end_port + 1)
        )

    open_ports.sort()

    return open_ports
