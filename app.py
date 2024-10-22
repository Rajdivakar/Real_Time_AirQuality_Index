import streamlit as st
import requests

# API details (keep your actual API key here)
API_KEY = '7fc48822b7a5336d09b725b685e01c9d'  # Replace with your API key
GEOCODING_URL = 'http://api.openweathermap.org/geo/1.0/direct'
AIR_QUALITY_URL = 'http://api.openweathermap.org/data/2.5/air_pollution'

# Function to get city coordinates
def get_city_coordinates(city):
    try:
        url = f"{GEOCODING_URL}?q={city}&limit=1&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            st.error("Error retrieving city coordinates. Please check the city name or API response.")
            return None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching city coordinates: {e}")
        return None, None

# Function to get air quality
def get_air_quality(city):
    lat, lon = get_city_coordinates(city)
    if lat and lon:
        try:
            url = f"{AIR_QUALITY_URL}?lat={lat}&lon={lon}&appid={API_KEY}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                return data
            else:
                st.error("Error fetching air quality data. Please check the API response.")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching air quality data: {e}")
            return None
    return None

# Streamlit app
st.title("Air Quality Monitor")

# City input from user
city = st.text_input("Enter city name")

if st.button("Check Air Quality"):
    if city:
        air_quality_data = get_air_quality(city)
        
        if air_quality_data:
            aqi = air_quality_data['list'][0]['main']['aqi']
            components = air_quality_data['list'][0]['components']
            
            st.subheader(f"Air Quality in {city.capitalize()}")
            st.write(f"Air Quality Index (AQI): {aqi}")
            
            st.write("Pollutant Levels (µg/m³):")
            st.write(f"CO: {components['co']}")
            st.write(f"NO: {components['no']}")
            st.write(f"NO2: {components['no2']}")
            st.write(f"O3: {components['o3']}")
            st.write(f"SO2: {components['so2']}")
            st.write(f"PM2.5: {components['pm2_5']}")
            st.write(f"PM10: {components['pm10']}")
            st.write(f"NH3: {components['nh3']}")
    else:
        st.warning("Please enter a valid city name.")
