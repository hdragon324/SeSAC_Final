import streamlit as st
import json
import os
import csv

# ✅ session_state 변수 초기화 (KeyError 방지)
if "submissions" not in st.session_state:
    st.session_state["submissions"] = []  # 빈 리스트로 초기화

if "step" not in st.session_state:
    st.session_state["step"] = 1  # 기본값으로 1로 초기화

# 모든 항목을 session_state로 저장하기 위한 변수 초기화
if "business_type" not in st.session_state:
    st.session_state["business_type"] = None

if "business_field" not in st.session_state:
    st.session_state["business_field"] = None

if "region" not in st.session_state:
    st.session_state["region"] = None

if "representative" not in st.session_state:
    st.session_state["representative"] = None

if "sales" not in st.session_state:
    st.session_state["sales"] = None

if "employees" not in st.session_state:
    st.session_state["employees"] = None

if "support_type" not in st.session_state:
    st.session_state["support_type"] = []

if "announcement_type" not in st.session_state:
    st.session_state["announcement_type"] = []

# JSON 파일을 읽는 함수
def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"파일을 찾을 수 없습니다: {file_path}")
        return None
    except json.JSONDecodeError:
        st.error(f"JSON 파일을 읽을 수 없습니다: {file_path}")
        return None

# CSV 파일 저장 함수
def save_to_csv(submission_data):
    file_path = "submission_data.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # ✅ CSV 파일에 헤더 추가 (첫 실행 시)
        if not file_exists:
            writer.writerow(["business_type", "business_field", "region", "representative", "sales", "employees", 
                             "support_type", "announcement_type"])

        # ✅ 사용자 데이터 저장
        writer.writerow([submission_data["business_type"],
                         submission_data["business_field"],
                         submission_data["region"],
                         submission_data["representative"],
                         submission_data["sales"],
                         submission_data["employees"],
                         ", ".join(submission_data["support_type"]),
                         ", ".join(submission_data["announcement_type"])])

# main 함수
def main():
    st.title("🎯 맞춤형 지원사업 추천 시스템")

    # Step 1부터 Step 7까지 진행
    if "step" not in st.session_state:
        st.session_state["step"] = 1  # 초기화가 안 되어 있으면 1로 설정

    # Step 1: 사업 유형 입력
    if st.session_state["step"] == 1:
        business_type = st.radio("📌 사업 유형을 선택하세요.",
            ["개인사업자", "법인사업자", "창업(예비사업자 포함)", "재창업", "기존사업자"])

        if st.button("다음"):
            st.session_state["business_type"] = business_type
            st.session_state["step"] = 2
            st.rerun()

    # Step 2: 업종 입력
    elif st.session_state["step"] == 2:
        business_field = st.selectbox("📌 업종을 선택하세요.",
            ["자동차 및 부품 판매업", "도매 및 상품 중개업", "소매업(자동차 제외)", "숙박업", "음식점업", "제조업", 
             "교육 서비스업", "협회 및 단체", "수리 및 기타 개인 서비스업", "부동산업", "전문, 과학 및 기술 서비스업",
             "예술, 스포츠 및 여가관련 서비스업", "정보통신업", "농업, 임업 및 어업", "건설업", "운수 및 창고업", 
             "보건업 및 사회복지 서비스업", "사업시설 관리, 사업 지원 및 임대 서비스업", "금융 및 보험업", 
             "전기, 가스, 증기 및 공기 조절 공급업", "광업", "수도, 하수 및 폐기물 처리, 원료 재생업", 
             "가구 내 고용활동 및 달리 분류되지 않은 자가 소비 생산활동", "공공행정, 국방 및 사회보장 행정", 
             "국제 및 외국기관"])

        if st.button("다음"):
            st.session_state["business_field"] = business_field
            st.session_state["step"] = 3
            st.rerun()

    # Step 3: 지역 입력
    elif st.session_state["step"] == 3:
        region = st.selectbox("📌 지역을 선택하세요.",
            ["서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "울산광역시", "세종특별자치시",
             "경기도", "충청북도", "충청남도", "전라남도", "경상북도", "경상남도", "제주특별자치도", 
             "강원특별자치도", "전북특별자치도"])

        if st.button("다음"):
            st.session_state["region"] = region
            st.session_state["step"] = 4
            st.rerun()

    # Step 4: 대표자 정보 입력
    elif st.session_state["step"] == 4:
        representative = st.radio("📌 대표자 성별을 선택하세요.",
            ["남", "여"])

        if st.button("다음"):
            st.session_state["representative"] = representative
            st.session_state["step"] = 5
            st.rerun()

    # Step 5: 매출 및 종업원 수 입력
    elif st.session_state["step"] == 5:
        sales = st.number_input("📌 매출을 입력하세요.", min_value=0, step=1)
        employees = st.number_input("📌 종업원 수를 입력하세요.", min_value=0, step=1)

        if st.button("다음"):
            st.session_state["sales"] = sales
            st.session_state["employees"] = employees
            st.session_state["step"] = 6
            st.rerun()

    # Step 6: 지원사업유형 입력
    elif st.session_state["step"] == 6:
        support_type = st.multiselect("📌 지원사업 유형을 선택하세요.",
            ["금융", "기술", "인력", "수출", "내수", "창업", "경영", "기타"])

        if st.button("다음"):
            st.session_state["support_type"] = support_type
            st.session_state["step"] = 7
            st.rerun()

    # Step 7: 공고특성 입력
    elif st.session_state["step"] == 7:
        announcement_type = st.multiselect("📌 공고 특성을 선택하세요.",
            ["소상공인", "청년 대상", "여성 대상", "대출", "마케팅 홍보", "보조금", "폐업", "고용지원", 
             "시설 환경개선", "입주 임대 지원", "희망리턴패키지", "고용유지지원금", "희망대출플러스", 
             "두루누리지원금", "창업패키지", "노란우산공제", "이커머스 입점피해"])

        if st.button("제출"):
            # 입력값을 저장
            submission_data = {
                "business_type": st.session_state["business_type"],
                "business_field": st.session_state["business_field"],
                "region": st.session_state["region"],
                "representative": st.session_state["representative"],
                "sales": st.session_state["sales"],
                "employees": st.session_state["employees"],
                "support_type": st.session_state["support_type"],
                "announcement_type": st.session_state["announcement_type"],
            }
            st.session_state["submissions"].append(submission_data)

            # CSV에 저장
            save_to_csv(submission_data)

            st.success("🎉 제출 완료! 데이터가 저장되었습니다.")
            st.write(submission_data)

            # 처음부터 다시 시작
            st.session_state["step"] = 1
            st.rerun()

    # JSON 파일 불러오기
    st.subheader("지원사업 공고")
    file_path = "streamlit_test.json"  # JSON 파일 경로 설정
    data = load_json_data(file_path)

    if data:
        # 금융 관련 데이터 출력
        if "금융" in data and data["금융"]:
            # 첫 10개 항목만 가져오기
            test_data = data['금융'][:10]

            # 3번째 항목의 summary 출력
            if len(test_data) > 2:
                st.write("3번째 항목의 Summary:", test_data[2].get("summary", "데이터 없음"))
        else:
            st.write("금융 관련 데이터가 없습니다.")
