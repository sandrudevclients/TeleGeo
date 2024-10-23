import streamlit as st
from streamlit.components.v1 import html
from streamlit_folium import st_folium
import folium

# Настройки страницы
st.set_page_config(page_title="OpenStreetMap с местоположением пользователя", layout="wide")

# Заголовок
st.title("OpenStreetMap с местоположением пользователя")

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
            // Отправляем координаты в Streamlit с помощью пользовательского события
            const streamlitEvent = new CustomEvent("streamlit:message", {
                detail: { latitude: latitude, longitude: longitude }
            });
            window.dispatchEvent(streamlitEvent);
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

# Получаем координаты из сообщения Streamlit
if 'latitude' not in st.session_state:
    st.session_state.latitude = None
if 'longitude' not in st.session_state:
    st.session_state.longitude = None

# Обработка события от JavaScript
def update_location(latitude, longitude):
    st.session_state.latitude = latitude
    st.session_state.longitude = longitude

# Слушаем событие геолокации
st.experimental_get_query_params()  # Запускает повторный запуск при событии геолокации

# Проверяем, доступны ли координаты
if st.session_state.latitude is not None and st.session_state.longitude is not None:
    lat = st.session_state.latitude
    lon = st.session_state.longitude
    st.write(f"Ваше местоположение: широта {lat}, долгота {lon}")

    # Создание карты с помощью folium
    m = folium.Map(location=[lat, lon], zoom_start=12)

    # Добавление маркера на карту
    folium.Marker([lat, lon], popup="Ваше местоположение").add_to(m)

    # Отображение карты в Streamlit
    st_folium(m, width=725)
else:
    st.write("Ожидание получения данных о геолокации...")
