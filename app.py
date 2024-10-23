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
            window.parent.postMessage({latitude: latitude, longitude: longitude}, "*");
        }
    );
}
getLocation();
</script>
"""

# Вставляем JavaScript код в Streamlit
html(geolocation_html)

# Получаем координаты через сообщения из JavaScript
latitude = st.session_state.get('latitude', None)
longitude = st.session_state.get('longitude', None)

# Если координаты переданы, отображаем карту
if latitude and longitude:
    st.write(f"Ваше местоположение: широта {latitude}, долгота {longitude}")
    
    # Создание карты с помощью folium
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    
    # Добавление маркера на карту
    folium.Marker([latitude, longitude], popup="Ваше местоположение").add_to(m)
    
    # Отображение карты в Streamlit
    st_folium(m, width=725)
else:
    st.write("Ожидание получения данных о геолокации...")
    
# Обработка событий для получения координат через postMessage
def set_coords(msg):
    if 'latitude' in msg.data and 'longitude' in msg.data:
        st.session_state['latitude'] = msg.data['latitude']
        st.session_state['longitude'] = msg.data['longitude']

# Вставка JavaScript для получения сообщений
html("""
<script>
window.addEventListener('message', (event) => {
    const data = event.data;
    const streamlitEvents = window.streamlitEvents || {};
    streamlitEvents.set_coords({data});
    window.streamlitEvents = streamlitEvents;
});
</script>
""", unsafe_allow_html=True)
