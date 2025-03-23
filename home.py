# home.py

import streamlit as st

def home_page():
    st.title("🏠 맞춤형 지원사업 추천 서비스")
    st.write("""
        본 서비스는 사용자의 사업 정보를 입력받아 **맞춤형 정부 지원사업**을 추천해주는 시스템입니다.
        
        좌측 사이드바에서 **"추천 시스템"**을 선택하여 지원사업 추천을 받아보세요!
    """)

    # 로그인 여부 확인
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        st.success(f"환영합니다, {st.session_state['user_info']['name']}님! 😊")
        st.write("👉 추천 시스템에서 맞춤 지원사업을 확인하세요.")
    else:
        st.warning("로그인이 필요합니다. 로그인 후 추천 서비스를 이용하세요!")

