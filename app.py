import streamlit as st
from streamlit.components.v1 import html
from streamlit_folium import st_folium
import folium

# Настройки страницы
st.set_page_config(page_title="OpenStreetMap with User Location", layout="wide")

# Заголовок
st.title("OpenStreetMap with User Location")

# HTML/JS для получения координат пользователя через геолокацию и их сохранения в Streamlit
geolocation_html = """
<script>
function getLocation() {
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            // Отправляем координаты в Streamlit
            document.getElementById("latitude").value = latitude;
            document.getElementById("longitude").value = longitude;
            document.getElementById("sendCoords").click();
        }
    );
}
getLocation();
</script>
<input type="hidden" id="latitude" name="latitude" value="">
<input type="hidden" id="longitude" name="longitude" value="">
<button id="sendCoords" onclick="sendCoords()" style="display:none;">Send</button>
"""

# Вставляем JavaScript код в Streamlit
html(geolocation_html, unsafe_allow_html=True)

# Получаем координаты из скрытых полей через Streamlit
lat = st.text_input("Широта", key="latitude")
lon = st.text_input("Долгота", key="longitude")

# Проверка наличия координат
if lat and lon:
    st.write(f"Ваше местоположение: широта {lat}, долгота {lon}")
    
    # Создание карты с помощью folium
    m = folium.Map(location=[float(lat), float(lon)], zoom_start=12)
    
    # Добавление маркера на карту
    folium.Marker([float(lat), float(lon)], popup="Ваше местоположение").add_to(m)
    
    # Отображение карты в Streamlit
    st_folium(m, width=725)
else:
    st.write("Ожидание получения данных о геолокации...")
