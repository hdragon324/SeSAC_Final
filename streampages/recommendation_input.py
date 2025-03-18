import streamlit as st
import csv
import os

# ✅ session_state 변수 초기화 (KeyError 방지)
if "submissions" not in st.session_state:
    st.session_state["submissions"] = []  # 빈 리스트로 초기화

if "step" not in st.session_state:
    st.session_state["step"] = 1  # 기본값으로 1로 초기화

if "business_type" not in st.session_state:
    st.session_state["business_type"] = None

if "business_field" not in st.session_state:
    st.session_state["business_field"] = None

if "region" not in st.session_state:
    st.session_state["region"] = None

if "business_name" not in st.session_state:
    st.session_state["business_name"] = None

def main():
    st.title("🎯 맞춤형 지원사업 추천 시스템")

    # ✅ Step 1: 사업 유형 입력
    if st.session_state["step"] == 1:
        business_type = st.radio("📌 사업 유형을 선택하세요.", 
            ["제조업", "도소매업", "IT 서비스", "프리랜서", "기타"])

        if st.button("다음"):
            st.session_state["business_type"] = business_type
            st.session_state["step"] = 2
            st.rerun()

    # ✅ Step 2: 업종 입력
    elif st.session_state["step"] == 2:
        business_field = st.selectbox("📌 업종을 선택하세요.", 
            ["기술 개발", "콘텐츠 제작", "교육 서비스", "헬스케어", "기타"])

        if st.button("다음"):
            st.session_state["business_field"] = business_field
            st.session_state["step"] = 3
            st.rerun()

    # ✅ Step 3: 지역 입력
    elif st.session_state["step"] == 3:
        region = st.selectbox("📌 지역을 선택하세요.", 
            ["서울", "경기", "부산", "대전", "기타"])

        if st.button("다음"):
            st.session_state["region"] = region
            st.session_state["step"] = 4
            st.rerun()

    # ✅ Step 4: 사업명 입력 + 제출 버튼
    elif st.session_state["step"] == 4:
        business_name = st.text_input("📌 사업명을 입력하세요.")

        if st.button("제출"):
            # ✅ 입력값을 저장
            submission_data = {
                "business_type": st.session_state["business_type"],
                "business_field": st.session_state["business_field"],
                "region": st.session_state["region"],
                "business_name": business_name,
            } 
            st.session_state["submissions"].append(submission_data)

            # ✅ CSV에 저장
            save_to_csv(submission_data)

            st.success("🎉 제출 완료! 데이터가 저장되었습니다.")
            st.write(submission_data)

            # ✅ 처음부터 다시 시작
            st.session_state["step"] = 1
            st.rerun()

# ✅ CSV 파일 저장 함수
def save_to_csv(submission_data):
    file_path = "submission_data.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # ✅ CSV 파일에 헤더 추가 (첫 실행 시)
        if not file_exists:
            writer.writerow(["business_type", "business_field", "region", "business_name"])

        # ✅ 사용자 데이터 저장
        writer.writerow([submission_data["business_type"],
                         submission_data["business_field"],
                         submission_data["region"],
                         submission_data["business_name"]])

if __name__ == "__main__":
    main()

