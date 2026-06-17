import streamlit as st
import requests

st.set_page_config(page_title="전공 추천 앱", layout="centered")

st.title("🎓 내게 맞는 전공 과목 추천 시스템")
st.write("관심 분야와 학년을 입력하면 딱 맞는 과목을 추천해 드립니다.")
st.divider()

# 사용자 입력을 받기 위한 Form UI 구성
with st.form("recommend_form"):
    # 1. 관심 분야 선택 (Selectbox)
    major_focus = st.selectbox("관심 분야를 선택하세요", options=["AI/데이터", "웹/앱 개발", "보안/네트워크"])
    
    # 2. 학년 선택 (Slider)
    grade = st.slider("현재 학년을 선택하세요", min_value=1, max_value=4, value=2)
    
    # 3. 선호 난이도 선택 (Radio)
    difficulty = st.radio("선호하는 난이도는?", options=["하", "중", "상"], horizontal=True)
    
    # 4. 제출 버튼
    submit_button = st.form_submit_button(label="🎯 맞춤 과목 추천받기")

# 사용자가 버튼을 눌렀을 때 실행되는 로직
if submit_button:
    # 💡 [핵심] 내 컴퓨터(로컬)에서 테스트할 때는 주소를 localhost로 설정합니다!
    backend_url = "http://localhost:8000/recommend"
    
    # 백엔드가 요구한 형식(RecommendInput) 그대로 데이터를 상자에 담습니다.
    payload = {
        "major_focus": major_focus,
        "grade": grade,
        "difficulty": difficulty
    }
    
    # 빙글빙글 도는 로딩 표시 생성
    with st.spinner("백엔드 서버(FastAPI)에 추천을 요청하는 중..."):
        try:
            # 🚀 실제로 네트워크를 통해 FastAPI에 데이터를 쏘고 응답을 받습니다.
            response = requests.post(backend_url, json=payload)
            
            if response.status_code == 200:
                result = response.json() # 결과 JSON 파싱
                
                # 화면에 결과 예쁘게 출력하기
                st.balloons() # 축하 풍선 이펙트
                st.success("🎉 추천 결과가 도착했습니다!")
                st.info(f"**{result['recommendation']}** 과목을 추천합니다.")
                st.caption(result['message'])
            else:
                st.error(f"백엔드 응답 실패 (에러코드: {response.status_code})")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ 백엔드 서버(FastAPI)가 꺼져 있습니다! 터미널에서 서버를 켜주세요.")