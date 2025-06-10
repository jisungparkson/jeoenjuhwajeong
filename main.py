import streamlit as st
import requests
import json
from datetime import datetime
import time

# 페이지 설정
st.set_page_config(
    page_title="🌟 오늘 운동장에서 놀 수 있을까?",
    page_icon="🌟",
    layout="wide"
)

# 제목
st.title("🌟 오늘 운동장에서 놀 수 있을까?")
st.subheader("미세먼지를 확인해보자! 🔍")

# API 키 입력
api_key = st.sidebar.text_input("9b0b8052f0c6eaead4c57ff48f0bd491
", type="password")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📍 위치 설정")

# 도시 선택
cities = {
    "서울": {"lat": 37.5665, "lon": 126.9780},
    "부산": {"lat": 35.1796, "lon": 129.0756},
    "대구": {"lat": 35.8714, "lon": 128.6014},
    "인천": {"lat": 37.4563, "lon": 126.7052},
    "광주": {"lat": 35.1595, "lon": 126.8526},
    "대전": {"lat": 36.3504, "lon": 127.3845},
    "울산": {"lat": 35.5384, "lon": 129.3114},
    "세종": {"lat": 36.4875, "lon": 127.2818}
}

selected_city = st.sidebar.selectbox("도시를 선택하세요:", list(cities.keys()))

def get_air_quality(api_key, lat, lon):
    """OpenWeatherMap API에서 대기질 데이터 가져오기"""
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 중 오류가 발생했습니다: {e}")
        return None

def get_pm_level_info(pm25, pm10):
    """미세먼지 수치에 따른 등급 및 정보 반환"""
    # PM2.5 기준 (WHO 기준 참고)
    if pm25 <= 15:
        pm25_level = "좋음"
        pm25_color = "🟢"
    elif pm25 <= 35:
        pm25_level = "보통"
        pm25_color = "🟡"
    elif pm25 <= 75:
        pm25_level = "나쁨"
        pm25_color = "🟠"
    else:
        pm25_level = "매우 나쁨"
        pm25_color = "🔴"
    
    # PM10 기준
    if pm10 <= 30:
        pm10_level = "좋음"
        pm10_color = "🟢"
    elif pm10 <= 80:
        pm10_level = "보통"
        pm10_color = "🟡"
    elif pm10 <= 150:
        pm10_level = "나쁨"
        pm10_color = "🟠"
    else:
        pm10_level = "매우 나쁨"
        pm10_color = "🔴"
    
    # 전체 등급 결정 (더 나쁜 등급으로)
    levels = ["좋음", "보통", "나쁨", "매우 나쁨"]
    overall_level = levels[max(levels.index(pm25_level), levels.index(pm10_level))]
    
    return {
        "pm25_level": pm25_level,
        "pm25_color": pm25_color,
        "pm10_level": pm10_level,
        "pm10_color": pm10_color,
        "overall_level": overall_level
    }

def get_recommendation(level):
    """등급에 따른 권장사항 반환"""
    recommendations = {
        "좋음": {
            "icon": "😄",
            "title": "야호! 밖에서 마음껏 놀아도 돼요!",
            "message": "미세먼지가 깨끗해요. 운동장에서 신나게 뛰어놀아도 괜찮아요!",
            "activities": ["축구", "농구", "달리기", "줄넘기", "놀이기구"],
            "color": "success"
        },
        "보통": {
            "icon": "🙂",
            "title": "괜찮아요! 밖에서 놀 수 있어요",
            "message": "미세먼지가 보통이에요. 평소처럼 밖에서 놀아도 됩니다.",
            "activities": ["가벼운 운동", "산책", "놀이기구", "공놀이"],
            "color": "info"
        },
        "나쁨": {
            "icon": "😷",
            "title": "조심해요! 짧게만 놀거나 실내에서 놀아요",
            "message": "미세먼지가 나빠요. 마스크를 끼고 짧게만 놀거나 실내 활동을 권해요.",
            "activities": ["실내 게임", "도서관", "짧은 산책 (마스크 착용)"],
            "color": "warning"
        },
        "매우 나쁨": {
            "icon": "😨",
            "title": "실내에서 놀아요!",
            "message": "미세먼지가 매우 나빠요. 오늘은 실내에서 놀아요!",
            "activities": ["실내 놀이", "독서", "그림그리기", "보드게임"],
            "color": "error"
        }
    }
    return recommendations.get(level, recommendations["보통"])

# 메인 앱
if api_key:
    lat = cities[selected_city]["lat"]
    lon = cities[selected_city]["lon"]
    
    # 새로고침 버튼
    if st.button("🔄 최신 데이터 가져오기", type="primary"):
        st.rerun()
    
    # 데이터 가져오기
    with st.spinner(f"{selected_city}의 미세먼지 데이터를 가져오는 중..."):
        air_data = get_air_quality(api_key, lat, lon)
    
    if air_data and 'list' in air_data:
        # 현재 시간
        current_time = datetime.now().strftime("%Y년 %m월 %d일 %H:%M")
        st.markdown(f"**📅 업데이트 시간:** {current_time}")
        st.markdown("---")
        
        # 미세먼지 데이터 추출
        pm25 = air_data['list'][0]['components']['pm2_5']
        pm10 = air_data['list'][0]['components']['pm10']
        
        # 등급 정보 가져오기
        level_info = get_pm_level_info(pm25, pm10)
        recommendation = get_recommendation(level_info["overall_level"])
        
        # 메인 추천 카드
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        ">
            <h1 style="font-size: 3rem; margin: 0;">{recommendation['icon']}</h1>
            <h2 style="margin: 0.5rem 0;">{recommendation['title']}</h2>
            <p style="font-size: 1.2rem; margin: 0;">{recommendation['message']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 상세 정보
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="🌫️ PM2.5 (초미세먼지)",
                value=f"{pm25} ㎍/㎥",
                delta=f"{level_info['pm25_level']} {level_info['pm25_color']}"
            )
        
        with col2:
            st.metric(
                label="💨 PM10 (미세먼지)",
                value=f"{pm10} ㎍/㎥",
                delta=f"{level_info['pm10_level']} {level_info['pm10_color']}"
            )
        
        with col3:
            st.metric(
                label="📊 종합 등급",
                value=level_info["overall_level"],
                delta=f"{selected_city}"
            )
        
        st.markdown("---")
        
        # 추천 활동
        st.subheader("🎮 오늘 추천하는 활동들")
        cols = st.columns(len(recommendation['activities']))
        for i, activity in enumerate(recommendation['activities']):
            with cols[i]:
                st.info(f"✨ {activity}")
        
        # 미세먼지 등급 안내
        st.markdown("---")
        st.subheader("📚 미세먼지 등급 알아보기")
        
        grade_info = """
        | 등급 | PM2.5 | PM10 | 설명 |
        |------|-------|------|------|
        | 🟢 좋음 | 0-15 | 0-30 | 마음껏 놀아도 괜찮아요! |
        | 🟡 보통 | 16-35 | 31-80 | 평소처럼 놀 수 있어요 |
        | 🟠 나쁨 | 36-75 | 81-150 | 마스크를 끼고 조심해서 놀아요 |
        | 🔴 매우나쁨 | 76+ | 151+ | 실내에서 놀아요! |
        """
        st.markdown(grade_info)
        
        # 건강 팁
        st.markdown("---")
        st.subheader("💡 건강 지키는 팁")
        
        tips = [
            "🚰 물을 많이 마셔요",
            "🧼 손을 자주 씻어요",
            "😷 미세먼지가 나쁠 때는 마스크를 써요",
            "🪟 창문을 열기 전에 미세먼지를 확인해요",
            "🥕 과일과 채소를 많이 먹어요"
        ]
        
        for tip in tips:
            st.write(tip)
    
    else:
        st.error("미세먼지 데이터를 가져올 수 없습니다. API 키를 확인해주세요.")

else:
    st.warning("⚠️ OpenWeatherMap API 키를 입력해주세요!")
    st.markdown("""
    ### API 키 받는 방법:
    1. [OpenWeatherMap](https://openweathermap.org/api) 사이트에 가입
    2. API Keys 메뉴에서 무료 API 키 생성
    3. 왼쪽 사이드바에 API 키 입력
    """)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; padding: 1rem;">
    만든이: AI 도우미 | 데이터 제공: OpenWeatherMap<br>
    🌱 깨끗한 공기로 건강하게 놀아요!
</div>
""", unsafe_allow_html=True)
