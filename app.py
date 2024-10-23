import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from streamlit_folium import st_folium
import folium

# Настройки страницы
st.set_page_config(page_title="OpenStreetMap with User Location", layout="wide")

# Заголовок
st.title("OpenStreetMap with User Location")

# Запрос координат пользователя через JavaScript
coords = streamlit_js_eval(js_expressions=["navigator.geolocation.getCurrentPosition((position) => {return position.coords;})"], key="geo_coords")

# Проверка, удалось ли получить координаты
if coords:
    lat = coords['latitude']
    lon = coords['longitude']
    st.write(f"Ваше местоположение: широта {lat}, долгота {lon}")

    # Создание карты с помощью folium
    m = folium.Map(location=[lat, lon], zoom_start=12)

    # Добавление маркера на карту
    folium.Marker([lat, lon], popup="Ваше местоположение").add_to(m)

    # Отображение карты в Streamlit
    st_folium(m, width=725)
else:
    st.write("Ожидание разрешения на доступ к геолокации...")
