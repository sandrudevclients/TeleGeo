import streamlit as st
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from streamlit_folium import st_folium
import folium

def get_location():
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode("Your IP Address")
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        return None

# Настройки страницы
st.set_page_config(page_title="OpenStreetMap with Location", layout="wide")

# Заголовок
st.title("OpenStreetMap with User Location")

# Определение местоположения пользователя
location = get_location()

if location:
    lat, lon = location
    st.write(f"Ваше местоположение: широта {lat}, долгота {lon}")
else:
    lat, lon = 51.5074, -0.1278  # Лондон как пример по умолчанию
    st.write("Не удалось определить местоположение, показано местоположение по умолчанию (Лондон)")

# Создание карты с помощью folium
m = folium.Map(location=[lat, lon], zoom_start=12)

# Добавление маркера на карту
folium.Marker([lat, lon], popup="Ваше местоположение").add_to(m)

# Отображение карты в Streamlit
st_folium(m, width=725)
