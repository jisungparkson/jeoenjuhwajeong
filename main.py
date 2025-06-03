import streamlit as st
import requests
import datetime

# 1. OpenWeatherMap API 키 설정 (여러분의 API 키로 바꿔주세요!)
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # 여기에 발급받은 API 키를 넣어주세요.
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# 2. 날씨 정보 가져오는 함수
def get_weather_data(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",  # 섭씨 온도를 원하면 'metric', 화씨를 원하면 'imperial'
        "lang": "kr" # 한국어 날씨 설명을 원할 경우
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"날씨 정보를 가져오는 중 오류가 발생했습니다: {e}")
        return None

# 3. Streamlit 웹앱 인터페이스
st.set_page_config(
    page_title="간단 날씨 앱",
    page_icon="☀️",
    layout="centered"
)

st.title("☀️ 날씨 정보 제공 웹앱")
st.markdown("---")

city = st.text_input("도시 이름을 입력하세요:", "Seoul")

if st.button("날씨 정보 가져오기"):
    if city:
        weather_data = get_weather_data(city)
        if weather_data:
            try:
                city_name = weather_data['name']
                country = weather_data['sys']['country']
                main_weather = weather_data['weather'][0]['description']
                icon_code = weather_data['weather'][0]['icon']
                temperature = weather_data['main']['temp']
                feels_like = weather_data['main']['feels_like']
                humidity = weather_data['main']['humidity']
                wind_speed = weather_data['wind']['speed']
                sunrise_timestamp = weather_data['sys']['sunrise']
                sunset_timestamp = weather_data['sys']['sunset']

                # 시간 변환
                sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp, datetime.timezone.utc) + datetime.timedelta(hours=9) # KST
                sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp, datetime.timezone.utc) + datetime.timedelta(hours=9) # KST


                st.subheader(f"{city_name}, {country}의 현재 날씨")
                st.write(f"날씨: {main_weather} {st.image(f'http://openweathermap.org/img/wn/{icon_code}@2x.png', width=50)}")
                st.write(f"온도: {temperature:.1f}°C")
                st.write(f"체감 온도: {feels_like:.1f}°C")
                st.write(f"습도: {humidity}%")
                st.write(f"바람 속도: {wind_speed} m/s")
                st.write(f"일출: {sunrise_time.strftime('%H:%M')} (KST)")
                st.write(f"일몰: {sunset_time.strftime('%H:%M')} (KST)")

            except KeyError as e:
                st.error(f"날씨 데이터를 처리하는 중 오류가 발생했습니다. 예상치 못한 데이터 형식: {e}")
                st.json(weather_data) # 디버깅을 위해 전체 데이터 출력
            except Exception as e:
                st.error(f"알 수 없는 오류가 발생했습니다: {e}")
    else:
        st.warning("도시 이름을 입력해주세요.")

st.markdown("---")
st.info("이 앱은 OpenWeatherMap API를 통해 날씨 정보를 제공합니다.")
