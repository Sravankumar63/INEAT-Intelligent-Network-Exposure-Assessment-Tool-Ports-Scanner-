import time

from scanner.validator import validate_target, validate_ports
from scanner.port_scanner import scan_ports
from scanner.services import get_service

from database.database import create_database, save_scan

from database.history import get_previous_ports, compare_scans

from scanner.risk_engine import *

from scanner.recommendation_engine import get_recommendations

from scanner.history_view import display_history

from scanner.security_grade import get_security_grade

from scanner.exposure_trend import get_previous_open_port_count, show_exposure_trend

from scanner.pdf_report import generate_pdf

print("=" * 75)
print("        Intelligent Network Exposure Assessment Tool")
print("=" * 75)

target = input("Enter Target IP or Hostname : ")

target_ip = validate_target(target)

if target_ip is None:
    print("\nInvalid Hostname or IP Address.")
    exit()

try:
    start_port_input = input("Enter Start Port (Default: 1) : ").strip()
    end_port_input = input("Enter End Port   (Default: 65535) : ").strip()

    start_port = int(start_port_input) if start_port_input else 1
    end_port = int(end_port_input) if end_port_input else 65535
except ValueError:
    print("\nPort numbers must be integers.")
    exit()

if not validate_ports(start_port, end_port):
    print("\nInvalid Port Range.")
    exit()

print("\nScanning Started...")
print("-" * 75)

# Start Timer
start_time = time.time()

# Perform Scan
open_ports = scan_ports(target_ip, start_port, end_port)

# End Timer
end_time = time.time()

# Calculate Scan Duration
scan_duration = round(end_time - start_time, 2)


previous_ports = get_previous_ports(target)

new_ports, closed_ports = compare_scans(previous_ports, open_ports)

print(f"\nTarget Host : {target}")
print(f"Target IP   : {target_ip}")

print("\n" + "=" * 110)
print(f"{'PORT':<8}{'SERVICE':<25}{'PROTOCOL':<12}{'CATEGORY':<25}{'STATUS'}")
print("=" * 110)

if open_ports:

    for port in open_ports:

        info = get_service(port)

        print(
            f"{port:<8}"
            f"{info['service']:<25}"
            f"{info['protocol']:<12}"
            f"{info['category']:<25}"
            f"OPEN"
        )

        print(f"{'':8}Description : {info['description']}")
        print("-" * 110)

else:

    print("No Open Ports Found.")

print("=" * 110)

print("\nCHANGE DETECTION")
print("-" * 30)

if new_ports:
    print("New Ports:")
    for port in new_ports:
        print(port)
else:
    print("New Ports : None")

print()

if closed_ports:
    print("Closed Ports:")
    for port in closed_ports:
        print(port)
else:
    print("Closed Ports : None")

print("=" * 75)

print("\nRISK ASSESSMENT")
print("-" * 30)

for port in open_ports:

    risk, score = get_port_risk(port)

    print(f"Port {port:<6} Risk : {risk}")

exposure_score = calculate_exposure_score(open_ports)

overall = overall_risk(exposure_score)

grade = get_security_grade(exposure_score)

previous_count = get_previous_open_port_count(target)
current_count = len(open_ports)

print("\nOverall Exposure Score :", exposure_score, "/100")
print("Overall Risk Level     :", overall)
print("Security Grade         :", grade)
show_exposure_trend(previous_count, current_count)

print("=" * 75)

print("\nSECURITY RECOMMENDATIONS")
print("-" * 30)

for port in open_ports:

    print(f"\nPort {port}")

    recommendations = get_recommendations(port)

    for recommendation in recommendations:

        print(f"  • {recommendation}")

print("=" * 75)

print(f"Total Ports Scanned : {end_port - start_port + 1}")
print(f"Open Ports Found    : {len(open_ports)}")
print(f"Scan Time           : {scan_duration} Seconds")

print("=" * 75)


# Create Database (if not exists)
create_database()

# Save Scan History
save_scan(
    target,
    open_ports,
    end_port - start_port + 1,
    scan_duration
)

display_history()

generate_pdf(
    target,
    open_ports,
    exposure_score,
    overall,
    grade
)
