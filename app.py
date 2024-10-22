import streamlit as st
import requests
import plotly.graph_objects as go
import time

# API details
API_KEY = '7fc48822b7a5336d09b725b685e01c9d'
WEATHER_API_KEY = 'ef9b13a44c000c096e28c7b84f91436d' 
GEOCODING_URL = 'http://api.openweathermap.org/geo/1.0/direct'
AIR_QUALITY_URL = 'http://api.openweathermap.org/data/2.5/air_pollution'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'

st.set_page_config(page_title="Air Quality Monitor", page_icon="🌍", layout="wide")

# Adding a header image and description
st.markdown(
    """
    <style>
    /* Background color for the body */
    .stApp {
        background-color: #f5f5f5; 
    }

    div.stButton > button {
        background-color: black; 
        color: white;
        padding: 10px 24px;
        font-size: 16px;
        border: none;
        border-radius: 20px;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.3s;
    }

    div.stButton > button:hover {
        background-color: gray;  
        transform: scale(1.05);
    }

    /* Custom color for the AQI title */
    .aqi-title {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 0.7; }
        50% { opacity: 1; }
        100% { opacity: 0.7; }
    }

    /* Make the image responsive */
    .responsive-image {
        width: 100%;
        height: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use HTML to render the image with the responsive class
st.markdown('<img src="https://t4.ftcdn.net/jpg/08/67/03/97/360_F_867039750_weThOJ30L07f0C6kYqJKyTjZB6hjyvP0.jpg" class="responsive-image"/>', unsafe_allow_html=True)

st.title("🌍 Air Quality Monitor")
st.markdown(
    """
    <style>
    /* Additional styling for the title or description can go here */
    </style>
    """,
    unsafe_allow_html=True
)

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

# Function to get real-time temperature
def get_weather_data(city):
    lat, lon = get_city_coordinates(city)
    if lat and lon:
        try:
            url = f"{WEATHER_URL}?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                return data
            else:
                st.error(f"Error fetching weather data. API responded with status: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching weather data: {e}")
            return None
    return None

# Sidebar with loading effect
with st.sidebar:
    st.header(" 🔎 Search your City")
    city = st.text_input("Enter Your city name", placeholder="e.g., Ludhiyana")
    fetch_btn = st.button("Check Air Quality")

    if fetch_btn:
        progress_bar = st.progress(0) 

        for i in range(100):
            time.sleep(0.02)  # Simulate delay
            progress_bar.progress(i + 1)

        air_quality_data = get_air_quality(city)
        weather_data = get_weather_data(city)
        progress_bar.empty()

if city and air_quality_data and weather_data:
    aqi = air_quality_data['list'][0]['main']['aqi']
    components = air_quality_data['list'][0]['components']
    temp = weather_data['main']['temp']

    # Mapping AQI values to air quality categories and colors
    aqi_level = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
    aqi_color = {1: "#00e400", 2: "#ffff00", 3: "#ff7e00", 4: "#ff0000", 5: "#7e0023"}

    # Display AQI Level
    st.markdown(f"<h2 class='aqi-title' style='color:{aqi_color[aqi]};'>{aqi_level[aqi]} Air Quality</h2>", unsafe_allow_html=True)

    st.metric("Temperature Of Your City(°C)", f"{temp}°C")
    
    # Using classes for metrics to apply transitions
    col1, col2, col3 = st.columns(3)
    col1.metric("CO (µg/m³)", round(components['co'], 2), delta=f"{round(components['co'] * 0.05, 2)}")
    col2.metric("NO (µg/m³)", round(components['no'], 2), delta=f"{round(components['no'] * 0.03, 2)}")
    col3.metric("NO2 (µg/m³)", round(components['no2'], 2), delta=f"{round(components['no2'] * 0.07, 2)}")

    col4, col5, col6 = st.columns(3)
    col4.metric("O3 (µg/m³)", round(components['o3'], 2), delta=f"{round(components['o3'] * 0.04, 2)}")
    col5.metric("SO2 (µg/m³)", round(components['so2'], 2), delta=f"{round(components['so2'] * 0.06, 2)}")
    col6.metric("PM2.5 (µg/m³)", round(components['pm2_5'], 2), delta=f"{round(components['pm2_5'] * 0.02, 2)}")

    col7, col8 = st.columns(2)
    col7.metric("PM10 (µg/m³)", round(components['pm10'], 2), delta=f"{round(components['pm10'] * 0.08, 2)}")
    col8.metric("NH3 (µg/m³)", round(components['nh3'], 2), delta=f"{round(components['nh3'] * 0.09, 2)}")

    fig = go.Figure(go.Scatterpolar(
        r=[components['co'], components['no'], components['no2'], components['o3'], components['so2'], components['pm2_5'], components['pm10'], components['nh3']],
        theta=['CO', 'NO', 'NO2', 'O3', 'SO2', 'PM2.5', 'PM10', 'NH3'],
        fill='toself',
        marker=dict(color=aqi_color[aqi]),
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(components.values()) + 50]),
        ),
        showlegend=False,
        title="Pollutant Levels Comparison",
        titlefont=dict(size=16),
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="closest"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Enter a city name in the sidebar and click 'Check Air Quality' to get the data.")


st.markdown("<hr><center><p>🌍 Thanks for using my App 🙏 </p></center>", unsafe_allow_html=True)
