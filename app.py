import streamlit as st
from streamlit.components.v1 import html
from streamlit_folium import st_folium
import folium

# Настройки страницы
st.set_page_config(page_title="OpenStreetMap with User Location", layout="wide")

# Заголовок
st.title("OpenStreetMap with User Location")

# HTML/JS для получения координат пользователя через геолокацию
geolocation_html = """
<script>
function getLocation() {
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            document.getElementById("latitude").textContent = latitude;
            document.getElementById("longitude").textContent = longitude;
        }
    );
}
getLocation();
</script>
<p>Широта: <span id="latitude"></span></p>
<p>Долгота: <span id="longitude"></span></p>
"""

# Вставляем JavaScript код в Streamlit
html(geolocation_html)

# Получаем координаты из HTML-элементов
lat = st.session_state.get("latitude")
lon = st.session_state.get("longitude")

if lat and lon:
    st.write(f"Ваше местоположение: широта {lat}, долгота {lon}")

    # Создание карты с помощью folium
    m = folium.Map(location=[lat, lon], zoom_start=12)

    # Добавление маркера на карту
    folium.Marker([lat, lon], popup="Ваше местоположение").add_to(m)

    # Отображение карты в Streamlit
    st_folium(m, width=725)
else:
    st.write("Ожидание получения данных о геолокации...")
