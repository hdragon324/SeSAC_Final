import streamlit as st
import mysql.connector
from mysql.connector import Error
import datetime

# 각 페이지에서 필요한 함수들만 임포트
from signup import register_user, login_user  # signup.py에서 필요한 함수만 임포트
from home import home_page
from recommendation import main as recommendation_page  # recommendation.py의 main() 함수 호출
from search import main as file_search_page

# draft.py의 business_plan_draft 함수 임포트
from draft import business_plan_draft  # 절대 경로로 import

# MySQL 연결 설정
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sooseo6307!",
        database="FinalProject"
    )

# 로그인 기능 (이미 signup.py에서 가져오도록 설정됨)
def login_user(userid, password):
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE userid = %s", (userid,))
        user = cursor.fetchone()

        if user and user['password'] == password:
            st.session_state.logged_in = True
            st.session_state.user_info = user
            st.success(f"{user['name']}님, 환영합니다!")
            st.rerun()  # 로그인 후 페이지 새로고침
        else:
            st.warning("아이디 또는 비밀번호가 잘못되었습니다.")
    except Error as e:
        st.write(f"로그인 중 에러 발생: {e}")
    finally:
        cursor.close()
        connection.close()

def main():
    st.set_page_config(page_title="맞춤 지원 공고 추천", layout="wide")

    # 세션 상태 (로그인 여부 저장)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_info = None

    # 사이드바 메뉴
    menu = ["🏠 홈", "🎯 추천 시스템", "👤 로그인", "👋 회원가입", "📂 파일 검색", "📄 사업계획서 초안"]
    choice = st.sidebar.selectbox("메뉴 선택", menu)

    # 로그인 상태에 따른 사이드바 내용 변경
    if st.session_state.logged_in:
        st.sidebar.write(f"🔓 로그인됨: {st.session_state.user_info['userid']}")
        
        # 고유한 key를 추가하여 로그아웃 버튼 중복 문제 해결
        if st.sidebar.button("로그아웃", key="logout_button"):  # key 추가
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.rerun()  # 로그아웃 후 새로고침
    else:
        st.sidebar.write("🔐 로그인되지 않음")

    # 홈 화면
    if choice == "🏠 홈":
        home_page()

    # 추천 시스템
    elif choice == "🎯 추천 시스템":
        if st.session_state.logged_in:
            recommendation_page()  # recommendation.py의 main() 함수 호출
        else:
            st.warning("추천 시스템을 이용하려면 로그인하세요.")

    # 로그인 페이지
    elif choice == "👤 로그인":
        st.subheader("로그인")
        userid = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")

        if st.button("로그인"):
            login_user(userid, password)

    # 회원가입 페이지
    elif choice == "👋 회원가입":
        st.subheader("회원가입")
        userid = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        name = st.text_input("이름")
        email = st.text_input("이메일")
        phone_number = st.text_input("전화번호")
        address = st.text_area("주소")
        dob = st.date_input("생년월일", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
        gender = st.selectbox("성별", ["남", "여"])

        if st.button("회원가입"):
            register_user(userid, password, name, email, phone_number, address, dob, gender)  # signup.py의 register_user 함수 호출

    # 파일 검색 페이지
    elif choice == "📂 파일 검색":
        file_search_page()

    # 사업계획서 초안 페이지
    elif choice == "📄 사업계획서 초안":
        business_plan_draft()  # 사업계획서 초안 페이지로 연결

if __name__ == "__main__":
    main()

