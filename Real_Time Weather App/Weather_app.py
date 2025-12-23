import streamlit as st
import requests
from datetime import datetime
import pandas as pd

st.header("Real-Time Weather App")

city = st.text_input("Enter the city name: ")

unit_choice = st.radio("Select unit:", ("Celsius", "Fahrenheit"))


def c_to_f(celsius):
    return (celsius * 9 / 5) + 32


if city:
    api_key = "16431f62cee897d4c4ccf0d7d5362645"
    # ---------------------
    # Current weather
    # ---------------------
    current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    current_response = requests.get(current_url)

    if current_response.status_code == 200:
        current_data = current_response.json()

        temp_c = current_data["main"]["temp"]
        humidity = current_data["main"]["humidity"]
        condition = current_data["weather"][0]["description"]
        sunrise = current_data["sys"]["sunrise"]
        sunset = current_data["sys"]["sunset"]
        icon_code = current_data["weather"][0]["icon"]

        sunrise_time = datetime.fromtimestamp(sunrise).strftime("%I:%M %p")
        sunset_time = datetime.fromtimestamp(sunset).strftime("%I:%M %p")

        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        if unit_choice == "Fahrenheit":
            temp_display = f"{c_to_f(temp_c):.1f} °F"
        else:
            temp_display = f"{temp_c:.1f} °C"

        st.subheader("Current Weather")
        st.image(icon_url)

        st.write(f"** Temperature: ** {temp_display}")
        st.write(f"** Humidity: ** {humidity}")
        st.write(f"** condition: ** {condition.capitalize()}")
        st.write(f"** sunrise: ** {sunrise_time}")
        st.write(f"** sunset: ** {sunset_time}")

    else:
        st.error("City Not found. Please try again.")

    # ---------------------
    # Forecastsection
    # --------------------

    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    forecast_response = requests.get(forecast_url)

    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        forecast_list = forecast_data["list"]

        daily_summary = {}

        for entry in forecast_list:
            date = pd.to_datetime(entry["dt_txt"]).date()
            temp_c = entry["main"]["temp"]
            icon_code = entry["weather"][0]["icon"]

            if date not in daily_summary:
                daily_summary[date] = {"temps": [], "icon": icon_code}
            daily_summary[date]["temps"].append(temp_c)

        # Display daily forecast with icons
        st.subheader("📅 5-Day Forecast")
        for date, info in daily_summary.items():
            avg_temp_c = sum(info["temps"]) / len(info["temps"])
            if unit_choice == "Fahrenheit":
                avg_temp_display = f"{c_to_f(avg_temp_c):.1f} °F"
            else:
                avg_temp_display = f"{avg_temp_c:.1f} °C"

            icon_url = f"http://openweathermap.org/img/wn/{info['icon']}@2x.png"

            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(icon_url, width=60)
            with col2:
                st.write(f"**{date}:** {avg_temp_display}")
