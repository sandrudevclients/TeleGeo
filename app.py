import streamlit as st
from streamlit.components.v1 import html
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="OpenStreetMap with User Location", layout="wide")
st.title("OpenStreetMap с вашим местоположением")

# HTML/JS для получения координат пользователя
geolocation_html = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    document.getElementById("latitude").textContent = latitude;
    document.getElementById("longitude").textContent = longitude;
}

getLocation();
</script>
<p>Широта: <span id="latitude"></span></p>
<p>Долгота: <span id="longitude"></span></p>
"""

html(geolocation_html)

# Получаем координаты из HTML-элементов и сохраняем в состояние сессии
lat = st.session_state.get("latitude")
lon = st.session_state.get("longitude")

# Настройки карты
map_type = st.selectbox("Тип карты", ["OpenStreetMap", "Stamen Terrain", "Stamen Toner"])
zoom_level = st.slider("Уровень масштабирования", 1, 18, 12)

def create_map(latitude, longitude, map_type, zoom_level):
    m = folium.Map(location=[latitude, longitude], zoom_start=zoom_level)
    folium.TileLayer(tiles=map_type).add_to(m)
    folium.Marker([latitude, longitude], popup="Ваше местоположение").add_to(m)
    return m

if st.button("Обновить местоположение"):
    st.experimental_rerun()

if lat and lon:
    st.write(f"Ваше местоположение: широта {lat}, долгота {lon}")
    st.session_state.latitude = lat
    st.session_state.longitude = lon
    m = create_map(lat, lon, map_type, zoom_level)
    st_folium(m, width=725)
else:
    st.write("Ожидание получения данных о геолокации...")
