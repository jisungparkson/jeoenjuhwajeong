import streamlit as st
import requests
import datetime

# 1. OpenWeatherMap API 키 설정 (★★★ 중요: 본인의 유효한 API 키로 변경하세요! ★★★)
API_KEY = "9c08027329504879b2a152706251601"  # 여기에 발급받은 API 키를 정확하게 넣어주세요.
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# 2. 날씨 정보 가져오는 함수
def get_weather_data(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",  # 섭씨 온도를 원하면 'metric', 화씨를 원하면 'imperial'
        "lang": "kr"  # 한국어 날씨 설명을 원할 경우
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        # HTTP 오류 (4xx, 5xx)의 경우, 더 구체적인 오류 메시지를 보여줍니다.
        st.error(f"날씨 정보를 가져오는 중 HTTP 오류가 발생했습니다: {http_err}")
        st.error(f"응답 내용: {response.text}") # 서버로부터 받은 응답 내용을 보여줍니다.
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"날씨 정보를 가져오는 중 요청 오류가 발생했습니다: {e}")
        return None
    except Exception as e:
        st.error(f"알 수 없는 오류 발생: {e}")
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
            # API 응답에 'cod' 필드가 있고, 그 값이 200 (성공)이 아닌 경우 오류로 처리
            if 'cod' in weather_data and weather_data['cod'] != 200:
                st.error(f"API 오류: {weather_data.get('message', '알 수 없는 오류')}")
                st.json(weather_data) # 디버깅을 위해 전체 데이터 출력
            elif 'name' not in weather_data: # 성공 응답이지만 예상치 못한 구조일 경우
                st.error("날씨 데이터를 가져왔으나, 예상치 못한 형식입니다.")
                st.json(weather_data)
            else:
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

                    # 시간 변환 (UTC 기준으로 KST 변환)
                    # datetime.timezone.utc를 명시하여 UTC 시간임을 알리고, timedelta를 사용하여 KST로 변환
                    sunrise_time_utc = datetime.datetime.fromtimestamp(sunrise_timestamp, datetime.timezone.utc)
                    sunset_time_utc = datetime.datetime.fromtimestamp(sunset_timestamp, datetime.timezone.utc)
                    
                    # 한국 시간대(KST, UTC+9)로 변환
                    kst = datetime.timezone(datetime.timedelta(hours=9))
                    sunrise_time_kst = sunrise_time_utc.astimezone(kst)
                    sunset_time_kst = sunset_time_utc.astimezone(kst)

                    st.subheader(f"{city_name}, {country}의 현재 날씨")
                    # st.image는 URL을 직접 사용합니다.
                    st.write(f"날씨: {main_weather}")
                    st.image(f"http://openweathermap.org/img/wn/{icon_code}@2x.png", width=70)
                    st.write(f"온도: {temperature:.1f}°C")
                    st.write(f"체감 온도: {feels_like:.1f}°C")
                    st.write(f"습도: {humidity}%")
                    st.write(f"바람 속도: {wind_speed} m/s")
                    st.write(f"일출: {sunrise_time_kst.strftime('%H:%M')} (KST)")
                    st.write(f"일몰: {sunset_time_kst.strftime('%H:%M')} (KST)")

                except KeyError as e:
                    st.error(f"날씨 데이터를 처리하는 중 오류가 발생했습니다. 데이터 키를 찾을 수 없습니다: {e}")
                    st.json(weather_data) # 디버깅을 위해 전체 데이터 출력
                except Exception as e:
                    st.error(f"데이터 처리 중 알 수 없는 오류가 발생했습니다: {e}")
                    st.json(weather_data) # 디버깅을 위해 전체 데이터 출력
    else:
        st.warning("도시 이름을 입력해주세요.")

st.markdown("---")
st.info("이 앱은 OpenWeatherMap API를 통해 날씨 정보를 제공합니다.")
