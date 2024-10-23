import streamlit as st
from streamlit_folium import st_folium
import folium

# Настройки страницы
st.set_page_config(page_title="OpenStreetMap with User Location", layout="wide")

# Заголовок
st.title("OpenStreetMap with User Location")

# JavaScript для получения координат
st.markdown("""
<script>
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        // Отправляем данные в Streamlit
        const data = {latitude: latitude, longitude: longitude};
        window.parent.postMessage(data, "*");
    });
} else {
    alert("Геолокация не поддерживается вашим браузером.");
}
</script>
""", unsafe_allow_html=True)

# Функция для получения координат из JavaScript
def get_coords():
    coords = st.experimental_get_query_params()
    return coords.get("latitude", [None])[0], coords.get("longitude", [None])[0]

# Отображение координат на карте
latitude, longitude = get_coords()

if latitude and longitude:
    latitude = float(latitude)
    longitude = float(longitude)
    
    st.write(f"Ваше местоположение: широта {latitude}, долгота {longitude}")

    # Создание карты с помощью folium
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    folium.Marker([latitude, longitude], popup="Ваше местоположение").add_to(m)
    
    # Отображение карты в Streamlit
    st_folium(m, width=725)
else:
    st.write("Ожидание получения данных о геолокации...")
