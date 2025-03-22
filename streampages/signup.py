import streamlit as st
import mysql.connector
from mysql.connector import Error
import re
import datetime
import bcrypt  # 비밀번호 해싱을 위한 라이브러리
 
# MySQL 연결 함수
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1:3306',  # MySQL 서버 주소
            database='FinalProject',  # 사용할 데이터베이스
            user='root',  # MySQL 사용자명
            password='sooseo6307!'  # MySQL 비밀번호
        )       
        if connection.is_connected():
            return connection
    except Error as e:
        st.write(f"연결 실패: {e}")
        return None

# 이메일 형식 검증 함수
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# 비밀번호 해싱 함수
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# 비밀번호 검증 함수
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# 사용자 등록 함수
def register_user(userid, password, name, email, phone_number, address, dob, gender):
    if not email or email == '':
        st.write("이메일을 입력해야 합니다.")
        return
    
    if not is_valid_email(email):
        st.write("올바른 이메일 형식을 입력하세요.")
        return

    connection = connect_to_mysql()
    if connection is not None:
        try:
            cursor = connection.cursor()

            # 이메일 중복 체크
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()

            if result:
                st.write("이미 존재하는 이메일입니다.")
                return

            # 비밀번호 해싱 적용
            hashed_password = hash_password(password)

            # 사용자 정보를 'users' 테이블에 삽입
            query = """INSERT INTO users (userid, password, name, email, phone_number, address, dob, gender) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (userid, hashed_password, name, email, phone_number, address, dob, gender))
            connection.commit()
            st.write("사용자 등록이 성공적으로 완료되었습니다.")
        except Error as e:
            st.write(f"사용자 등록 중 에러 발생: {e}")
        finally:
            cursor.close()
            connection.close()

# 로그인 함수
def login_user(userid, password):
    connection = connect_to_mysql()
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)

            # 입력받은 사용자 ID의 정보를 가져옴
            cursor.execute("SELECT * FROM users WHERE userid = %s", (userid,))
            user = cursor.fetchone()

            if user and check_password(password, user['password']):  # 해싱된 비밀번호 비교
                st.session_state["logged_in"] = True
                st.session_state["user_info"] = user
                st.success(f"{user['name']}님, 환영합니다!")
                st.rerun()  # 로그인 후 새로고침
            else:
                st.write("아이디 또는 비밀번호가 잘못되었습니다.")
        except Error as e:
            st.write(f"로그인 중 에러 발생: {e}")
        finally:
            cursor.close()
            connection.close()

# 로그아웃 함수
def logout():
    st.session_state["logged_in"] = False
    st.session_state["user_info"] = None
    st.rerun()

# Streamlit 인터페이스 구현
def main():
    st.title("MySQL Streamlit 연동 예시")

    # 로그인 상태 유지
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user_info"] = None

    menu = ["🏠 홈", "👤 로그인", "👋 회원가입"]
    choice = st.sidebar.selectbox("메뉴 선택", menu)

    if st.session_state["logged_in"]:
        st.sidebar.write(f"🔓 로그인됨: {st.session_state['user_info']['name']} 님")
        if st.sidebar.button("로그아웃"):
            logout()

    elif choice == "👤 로그인":
        st.subheader("로그인")
        userid = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")

        if st.button("로그인"):
            login_user(userid, password)

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
            register_user(userid, password, name, email, phone_number, address, dob, gender)

if __name__ == "__main__":
    main()


