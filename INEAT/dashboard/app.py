import streamlit as st

import pandas as pd

from scanner.risk_engine import get_port_risk, calculate_exposure_score, overall_risk

from scanner.security_grade import get_security_grade

from scanner.recommendation_engine import get_recommendations

from scanner.history_view import get_scan_history

from scanner.change_detection import detect_changes

import plotly.express as px

from scanner.pdf_report import generate_pdf

import os

st.set_page_config(
    page_title="INEAT",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Intelligent Network Exposure Assessment Tool (INEAT)")

st.markdown("---")

target = st.text_input("Target IP / Hostname")

scan_mode = st.selectbox(
    "Scan Mode",
    [
        "Quick Scan (1-1024)",
        "Standard Scan (1-10000)",
        "Full Scan (1-65535)",
        "Custom"
    ]
)

if scan_mode == "Quick Scan (1-1024)":

    start_port = 1
    end_port = 1024

elif scan_mode == "Standard Scan (1-10000)":

    start_port = 1
    end_port = 10000

elif scan_mode == "Full Scan (1-65535)":

    start_port = 1
    end_port = 65535

else:

    col1, col2 = st.columns(2)

    with col1:
        start_port = st.number_input(
            "Start Port",
            min_value=1,
            max_value=65535,
            value=1
        )

    with col2:
        end_port = st.number_input(
            "End Port",
            min_value=1,
            max_value=65535,
            value=1024
        )

scan = st.button("🚀 Start Scan")

if scan:

    from scanner.validator import validate_target
    from scanner.port_scanner import scan_ports
    from scanner.services import get_service

    target_ip = validate_target(target)

    if target_ip is None:
        st.error("Invalid Target")
    else:

        with st.spinner("Scanning ports... Please wait."):

            open_ports = scan_ports(
                target_ip,
                start_port,
                end_port
            )

        st.success("Scan Completed")

        search = st.text_input(
            "Search Port / Service",
            placeholder="Example: 80, HTTP, SMB"
        )
        st.subheader("Open Ports")

        if open_ports:

            results = []

            for port in open_ports:
                info = get_service(port)

                results.append({

                    "Port": port,

                    "Service": info["service"],

                    "Protocol": info["protocol"],

                    "Category": info["category"],

                    "Risk": info["risk"],

                    "Status": "OPEN",
        
                    "Description": info["description"]

                })

            df = pd.DataFrame(results)

            if search:

                search = search.lower()

                df = df[
                    df.astype(str)
                      .apply(lambda row: row.str.lower().str.contains(search))
                      .any(axis=1)
                ]
            st.dataframe(
                df,
                width="stretch", hide_index=True
                )

            st.subheader("Risk Assessment")

            exposure_score = calculate_exposure_score(open_ports)
            risk_level = overall_risk(exposure_score)
            grade = get_security_grade(exposure_score)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Open Ports", len(open_ports))

            with col2:
                st.metric("Exposure Score", f"{exposure_score}/100")

            with col3:
                st.metric("Overall Risk", risk_level)

            with col4:
                st.metric("Security Grade", grade)

            st.subheader("Scan Summary")

            col1, col2 = st.columns(2)

            with col1:
                st.info(f"Target : {target}")

            with col2:
                st.info(f"Scanned Ports : {end_port - start_port + 1}")
            
            risk_counts = {
                "LOW": 0,
                "MEDIUM": 0,
                "HIGH": 0,
                "CRITICAL": 0,
                "UNKNOWN": 0
            }
            for port in open_ports:
                risk, _ = get_port_risk(port)
                risk_counts[risk] += 1

            chart_data = {
                "Risk": list(risk_counts.keys()),
                "Count": list(risk_counts.values())
            }
            fig = px.pie(
                chart_data,
                names="Risk",
                values="Count",
                title="Risk Distribution"
            )
            st.plotly_chart(fig, width="stretch")

            st.subheader("Security Recommendations")
            
            for port in open_ports:
                st.markdown(f"### Port {port}")
                recommendations = get_recommendations(port)
                for recommendation in recommendations:
                    st.write("•", recommendation)

            st.subheader("Port Details")

            for port in open_ports:

                info = get_service(port)

                with st.expander(
                    f"Port {port} | {info['service']} | Risk : {info['risk']}",
                    expanded=False
                ):

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Service:**", info["service"])
                        st.write("**Protocol:**", info["protocol"])
                        st.write("**Category:**", info["category"])

                    with col2:
                        st.write("**Risk:**", info["risk"])
                        st.write("**Status:** OPEN")

                    st.write("**Description:**")
                    st.info(info["description"])

                    st.write("**Recommendations:**")

                    recommendations = get_recommendations(port)
    
                    for recommendation in recommendations:
                        st.write("•", recommendation)

            st.divider()

            # ==========================================
            # PDF DOWNLOAD
            # ==========================================

            pdf_file = f"{target}_Report.pdf"

            generate_pdf(
                target,
                open_ports,
                exposure_score,
                risk_level,
                grade
            )

            with open(pdf_file, "rb") as file:

                st.download_button(
                    label="📄 Download PDF Report",
                    data=file,
                    file_name=pdf_file,
                    mime="application/pdf"
                )

            st.subheader("Change Detection")
    
        else:

            st.warning("No Open Ports Found")


        st.subheader("Change Detection")

        new_ports, closed_ports = detect_changes(target, open_ports)

        col1, col2 = st.columns(2)
        with col1:
            st.write("### New Ports")

            if new_ports:
                st.success(", ".join(map(str, new_ports)))
            else:
                st.info("None")

        with col2:
            st.write("### Closed Ports")

            if closed_ports:
                st.error(", ".join(map(str, closed_ports)))
            else:
                st.info("None")
