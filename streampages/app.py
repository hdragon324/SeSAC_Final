import streamlit as st
import mysql.connector  # MySQL 연결을 위한 라이브러리
from search import main as search_app  # 파일 검색 기능
from home import main as home_main  # 홈 화면 기능
from recommendation import main as recommendation_main  # 추천 시스템 기능
from signup import main as signup_main  # 회원가입 기능 추가

# MySQL 연결 설정
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sooseo6307!",
        database="FinalProject"
    )

# 로그인 인증 함수
def authenticate_user(userid, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE userid = %s AND password = %s"
    cursor.execute(query, (userid, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user  # 로그인 성공 시 사용자 정보 반환, 실패 시 None 반환

# Streamlit 페이지 설정
def main():
    st.set_page_config(page_title="맞춤 지원 공고 추천", layout="wide")

    # 세션 상태 (로그인 여부 저장)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_info = None

    menu = ["🏠 홈", "🎯 추천 시스템", "👤 로그인", "👋 회원가입", "📂 파일 검색"]
    choice = st.sidebar.selectbox("메뉴 선택", menu)

    if choice == "🏠 홈":
        home_main()  # 홈 화면 실행

    elif choice == "🎯 추천 시스템":
        if st.session_state.logged_in:
            recommendation_main()  # 로그인한 경우 추천 시스템 실행
        else:
            st.warning("추천 시스템을 이용하려면 로그인하세요.")

    elif choice == "📂 파일 검색":
        search_app()  # 파일 검색 기능 실행

    elif choice == "👤 로그인":
        st.subheader("로그인")

        userid = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")

        if st.button("로그인"):
            user = authenticate_user(userid, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.user_info = user  # 로그인된 사용자 정보 저장
                st.success(f"{user['userid']}님, 환영합니다!")
                st.rerun()  # 로그인 후 페이지 새로고침
            else:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

    elif choice == "👋 회원가입":
        signup_main()  # signup.py의 main() 실행

    # 로그인 상태일 때 상단에 표시
    if st.session_state.logged_in:
        st.sidebar.write(f"🔓 로그인됨: {st.session_state.user_info['userid']}")
        if st.sidebar.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.rerun()  # 로그아웃 후 새로고침

if __name__ == "__main__":
    main()

