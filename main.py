from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# 프론트엔드(Streamlit)에서 보내는 요청을 보안 문제없이 허용하기 위한 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 어디서 오든 다 받아줄게!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [데이터 규격] Streamlit이 보낼 데이터 상자의 모양을 정의합니다.
class RecommendInput(BaseModel):
    major_focus: str  # 관심분야
    grade: int        # 학년
    difficulty: str   # 선호 난이도

# [추천 엔드포인트] 진짜 추천을 수행하는 주소(/recommend)를 만듭니다.
@app.post("/recommend")
def get_recommend(data: RecommendInput):
    # 규칙 기반(if-else) 추천을 위한 데이터 데이터베이스 대용 딕셔너리
    courses = {
        "AI/데이터": ["머신러닝 기초", "데이터 마이닝", "딥러닝 응용"],
        "웹/앱 개발": ["웹 시스템 설계", "모바일 앱 프로그래밍", "데이터베이스"],
        "보안/네트워크": ["정보보호 개론", "컴퓨터 네트워크", "운영체제"]
    }
    
    # 1. 사용자가 고른 관심분야의 과목 목록을 가져옵니다.
    selected_pool = courses.get(data.major_focus, ["컴퓨터 공학 개론"])
    
    # 2. 난이도가 '상'이면 리스트의 마지막 과목(어려운 것), 그 외엔 첫 과목을 고르는 단순 규칙
    if data.difficulty == "상":
        recommended_course = selected_pool[-1]
    else:
        recommended_course = selected_pool[0]
        
    # 3. 텍스트 조립
    message = f"💡 {data.grade}학년 수준의 [{data.difficulty}] 난이도에 맞춘 추천 결과입니다."
    
    # 4. Streamlit에게 JSON 형태로 돌려주기
    return {
        "status": "success",
        "message": message,
        "recommendation": recommended_course
    }