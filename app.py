import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Firewall Location Detector",
    page_icon="🔥",
    layout="centered"
)

st.title("🔥 Mini Firewall Location Detector")
st.write("Detect suspicious IP addresses and view their approximate location.")

ip = st.text_input(
    "Enter suspicious IP address",
    placeholder="Example: 8.8.8.8"
)

if st.button("🔍 Detect IP"):

    if ip == "":
        st.warning("Please enter an IP address.")

    else:
        try:
            url = f"https://ipapi.co/{ip}/json/"
            response = requests.get(url, timeout=5)
            data = response.json()

            if data.get("error"):
                st.error("Invalid IP address.")
            else:

                city = data.get("city", "Unknown")
                country = data.get("country_name", "Unknown")
                org = data.get("org", "Unknown")
                latitude = data.get("latitude")
                longitude = data.get("longitude")

                st.success("IP detected successfully!")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("IP Address", ip)
                    st.metric("Country", country)

                with col2:
                    st.metric("City", city)
                    st.metric("Network", org)

                st.subheader("📍 Approximate Location")

                if latitude and longitude:
                    location = pd.DataFrame({
                        "latitude": [latitude],
                        "longitude": [longitude]
                    })

                    st.map(location)

                st.subheader("🚨 Firewall Status")

                st.error("Suspicious IP detected")

                st.write(
                    "This IP should be investigated or blocked "
                    "if repeated malicious activity is observed."
                )

        except Exception as e:
            st.error("Unable to retrieve IP information.")
