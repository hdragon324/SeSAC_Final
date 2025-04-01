import streamlit as st
import streamlit_antd_components as sac

import pandas as pd
import papermill as pm
import json
import os

from io import BytesIO

from utils.authenticator import hash_password, save_user, is_valid_password, authenticate_user
from utils.template import ccs_get_user_input, ccp_get_user_input, ycp_get_user_input # 초안 작성 (3가지 유형의 템플릿)
from utils.recommend import cosine_similarity_recommend, convert_table_to_dict, format_text_with_bullet_points # 공고 추천의 기능들


def home_page():
    # sac.alert(label='정기 점검 중', description='정기 점검 시간 03.27.18:00 ~ 04.02.12:00', banner=True, icon=True, closable=True)
    # 페이지 전체를 감싸는 컨테이너
    with st.container():
        # 스타일 커스텀
        st.header("🏠 맞춤형 지원 공고 추천 & AI 사업계획서 초안 작성")
        st.markdown("<p style='font-size:17px;'>본 페이지는 사용자의 사업 정보를 기반으로 정부 지원사업을 추천하고, AI를 활용하여 사업계획서 작성을 지원하는 맞춤형 비즈니스 지원 시스템입니다.</p>", unsafe_allow_html=True)
        st.markdown(
            """
            <style>
                .section { background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
                .card { height: 130px; padding: 15px; border-radius: 10px; color: white; text-align: left; font-weight: bold; }
                .blue { background-color: #6610f2; }
                .dark-blue { background-color: #3c007a; }
                .orange { background-color: #fd7e14; }
                body { overflow: hidden; }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # 카드 섹션을 감싸는 컨테이너
        with st.container():
        # 카드 섹션
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                <div class='card blue'>
                    <div style='font-size:18px; font-weight:bold;'>📄 맞춤형 지원 공고</div>
                    <p>사용자의 정보(사업 유형, 업종, 지역, 우대사항 등)를 분석하여 정부 지원 사업을 추천</p>
                </div>
            """, unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div class='card dark-blue'>
                    <div style='font-size:18px; font-weight:bold;'>📄 AI 사업계획서 초안</div>
                    <p>사용자의 정보 (사업 아이디어, 시장 분석, 재무 등)을 기반으로 사업계획서 초안을 작성</p>
                </div>
            """, unsafe_allow_html=True)

            with col3:
                st.markdown("""
                <div class='card orange'>
                    <div style='font-size:18px; font-weight:bold;'>📄 스마트 알림 서비스(예정)</div>
                    <p>사용자의 정보에 맞는 새로운 정부 지원 공고가 올라올 때 알림을 제공</p>
                </div>
            """, unsafe_allow_html=True)

        # 페이지 이용 방법 안내 (컨테이너 활용)
        with st.container():
            # 문서 사용법 섹션
            st.markdown("---")
            st.subheader("📌 페이지 이용 방법 안내")

            # 2등분된 레이아웃 생성 (2/3, 1/3 비율)
        left_column, right_column = st.columns([2, 1])

        # 왼쪽 컬럼에 내용 추가
        with left_column:

            st.markdown('''
                **:blue[✅ 로그인 및 회원가입]**   
                - 기존 회원은 **로그인** 버튼을 눌러 계정 정보를 입력 후 접속 할 수 있습니다.
                - 신규 사용자는  **회원가입**을 통해 계정을 생성한 후 서비스를 이용할 수 있습니다.''')
            st.markdown('''
                **:blue[✅ 사이드바 메뉴 선택]**  
                - 페이지 좌측에 위치한 **사이드바**를 통해 주요 기능을 선택할 수 있습니다.  
                - **지원 사업 추천** : 사업 정보를 입력하면 적합한 정부 지원사업의 요약을 확인할 수 있습니다.  
                - **AI 사업계획서 초안** : GPT-4o를 활용해 사업계획서 초안을 자동 생성할 수 있습니다.**(로그인 필수)**''')
            st.markdown(
                "**:orange[기타 문의 사항]** 이용 중 궁금한 사항이 있으면 고객 지원 센터를 이용해 주세요! 😊")
        
        with right_column:
            st.markdown('''
                **:blue[✅ 떴다앱 영상 설명서]**''')
            st.video('image_movie/ddapp_movie.mp4')
                
def recommendation_page():
    '''추천 시스템 페이지'''

    # 페이지 메인 제목 
    st.header("🎯 맞춤형 지원사업 공고 추천")

    # Step 1부터 Step 7까지 진행
    if "step" not in st.session_state:
        st.session_state["step"] = 1  # 초기화가 안 되어 있으면 1로 설정

    # Step 1: 사업 유형 입력
    if st.session_state["step"] == 1:
        
        st.write('📌 사업 유형을 선택하세요.')
        business_type = sac.chip(
            items=[
                sac.ChipItem(label=유형) for 유형 in ["개인사업자", "법인사업자", "창업(예비사업자 포함)", "재창업", "기존사업자"]],
                multiple=False) # 중복 선택 불가능
        

        if st.button("다음"):
            st.session_state["business_type"] = business_type
            st.session_state["step"] += 1
            st.rerun()

    # Step 2: 업종 입력
    elif st.session_state["step"] == 2:
        
        st.write('📌 업종을 선택하세요.')
        business_field = sac.chip(
        items=[
            sac.ChipItem(label=업종) for 업종 in [
                "자동차 및 부품 판매업", "도매 및 상품 중개업", "소매업(자동차 제외)", "숙박업", "음식점업", "제조업",
                "교육 서비스업", "협회 및 단체", "수리 및 기타 개인 서비스업", "부동산업", "전문, 과학 및 기술 서비스업",
                "예술, 스포츠 및 여가관련 서비스업", "정보통신업", "농업, 임업 및 어업", "건설업", "운수 및 창고업",
                "보건업 및 사회복지 서비스업", "사업시설 관리, 사업 지원 및 임대 서비스업", "금융 및 보험업",
                "전기, 가스, 증기 및 공기 조절 공급업", "광업", "수도, 하수 및 폐기물 처리, 원료 재생업",
                "가구 내 고용활동 및 달리 분류되지 않은 자가 소비 생산활동", "공공행정, 국방 및 사회보장 행정",
                "국제 및 외국기관"
            ]
        ],
        multiple=False)  # 하나만 선택 가능하도록 설정

        if st.button("다음"):
            st.session_state["business_field"] = business_field
            st.session_state["step"] += 1
            st.rerun()

    # Step 3: 지역 입력
    elif st.session_state["step"] == 3:

        st.write('📌 지역을 선택하세요.')
        region = sac.chip(
        items=[
            sac.ChipItem(label=지역) for 지역 in [
                "서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시", "울산광역시", "세종특별자치시",
                "경기도", "충청북도", "충청남도", "전라남도", "경상북도", "경상남도", "제주특별자치도",
                "강원특별자치도", "전북특별자치도"
            ]
        ],
        multiple=False  # 하나만 선택 가능하도록 설정
    )

        if st.button("다음"):
            st.session_state["region"] = region
            st.session_state["step"] += 1
            st.rerun()

    # Step 4: 대표자 정보 입력
    elif st.session_state["step"] == 4:
        representative = st.radio("📌 대표자 성별을 선택하세요.",
            ["남", "여"])

        if st.button("다음"):
            st.session_state["representative"] = representative
            st.session_state["step"] += 1
            st.rerun()

    # Step 5: 매출 및 종업원 수 입력
    elif st.session_state["step"] == 5:
        sales = st.number_input("📌 매출을 입력하세요.", min_value=0, step=1)
        employees = st.number_input("📌 종업원 수를 입력하세요.", min_value=0, step=1)

        if st.button("다음"):
            st.session_state["sales"] = sales
            st.session_state["employees"] = employees
            st.session_state["step"] += 1
            st.rerun()

    # Step 6: 지원사업유형 입력
    elif st.session_state["step"] == 6:

        st.write("📌 지원사업 유형을 선택하세요. **(복수 선택 가능)**")
        support_type = sac.chip(
            items=[
                sac.ChipItem(label=유형) for 유형 in [
                    "금융", "기술", "인력", "수출", "내수", "창업", "경영", "기타"
                ]
            ],
            multiple=True  # 다중 선택 가능하도록 설정
        )

        if st.button("다음"):
            st.session_state["support_type"] = support_type
            st.session_state["step"] += 1
            st.rerun()

    # Step 7
    elif st.session_state["step"] == 7:
        if "submitted" not in st.session_state:
            st.session_state["submitted"] = False
        if "submissions" not in st.session_state:
            st.session_state["submissions"] = []  # 초기화 추가

        if not st.session_state["submitted"]:

            st.write("📌 공고 특성을 선택하세요. **(복수 선택 가능)**")  # 라벨 출력
            announcement_type = sac.chip(
                items=[
                    sac.ChipItem(label=특성) for 특성 in [
                        "소상공인", "청년 대상", "여성 대상", "대출", "마케팅 홍보", "보조금", "폐업", "고용지원",
                        "시설 환경개선", "입주 임대 지원", "희망리턴패키지", "고용유지지원금", "희망대출플러스",
                        "두루누리지원금", "창업패키지", "노란우산공제", "이커머스 입점피해"
                    ]
                ],
                multiple=True  # 다중 선택 가능하도록 설정
            )

            if st.button("제출"):

                # 입력값을 저장
                st.session_state["announcement_type"] = announcement_type

                submission_data = {
                    "사업자 유형": st.session_state["business_type"],
                    "지원업종": st.session_state["business_field"],
                    "지역": st.session_state["region"],
                    "성별": st.session_state["representative"],
                    "신청기간" : "현재 진행중인 것",
                    "매출": st.session_state["sales"],
                    "종업원수": st.session_state["employees"],
                    "지원사업 유형": st.session_state["support_type"],
                    "공고 특성 / 우대 사항": st.session_state["announcement_type"],
                }

                # JSON 문자열로 변환 후 세션 상태에 저장
                st.session_state["user_input"] = json.dumps(submission_data, ensure_ascii=False, indent=4)

                st.session_state["submissions"].append(submission_data)

                # 만약에 로그인 되어 있으면
                if st.session_state["authenticated"] == True:
                    file_name = st.session_state["username"]
                    file_path = f"users/{file_name}data.json"

                    # 기존 JSON 파일을 읽어오기 (파일이 존재하면)
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding="utf-8") as file:
                            try:
                                existing_data = json.load(file)  # 기존 데이터 로드
                            except json.JSONDecodeError:
                                existing_data = []  # JSON 파일이 비어있거나 깨졌다면 빈 리스트로 초기화
                    else:
                        existing_data = []  # 파일이 없으면 빈 리스트로 초기화

                    # 새 데이터를 기존 데이터에 추가
                    existing_data.append(submission_data)

                    # 업데이트된 데이터를 JSON 파일로 저장
                    with open(file_path, "w", encoding="utf-8") as file:
                        json.dump(existing_data, file, ensure_ascii=False, indent=4)
                    

                # 제출 완료 상태 변경
                st.session_state["submitted"] = True
                st.rerun()

        else:
            st.success("🎉 제출 완료!")

            # 유사도 기반 추천 (이전 단계에서 저장한 user_input 사용)
            if "user_input" in st.session_state:
                with st.spinner("🔄 Loading...잠시만 기다려 주세요!"):
                    cosine_similarity_recommend(st.session_state["user_input"])

            if st.button("다시 제출"):
                st.session_state.clear()
                st.session_state["step"] = 1
                st.rerun()

def login_page():
    '''로그인 페이지'''
    st.header("👤 로그인")

    username = st.text_input("Username", placeholder='아이디(사용자 이름)를 입력하세요.')
    password = st.text_input("Password", type="password", placeholder='비밀번호를 입력하세요. (비밀번호는 6자이상, 영어 소문자, 숫자, 특수문자를 포함할 수 있습니다.)')

    if st.button("Sign in"):
        if not (username and password):
            st.error("아이디와 비밀번호를 모두 입력해 주세요.")
        else:
            success, message = authenticate_user(username, password)
            if success:
                st.success(message)
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error(message)

def register_page():
    '''회원가입 페이지'''

    st.header("👋 회원가입")

    username = st.text_input("Username", placeholder='아이디(사용자 이름)를 입력하세요')
    email = st.text_input("Email", placeholder='이메일(본인 확인용)을 입력하세요')
    password = st.text_input("Password", type="password", placeholder='비밀번호를 입력하세요')
    

    if st.button("Sign Up"):
        if not (username and email and password):
            st.error("모든 항목을 입력해 주세요.")
        elif not is_valid_password(password):
            st.warning("비밀번호는 6자 이상이며, 영어 소문자, 숫자, 특수문자를 포함해야 합니다.")
        else:
            hashed = hash_password(password)
            result = save_user(username, email, hashed)

            if result == "success":
                st.success(f"{username}님, 회원가입이 완료되었습니다!")
            else:
                st.error(result)
    
def search_file_page():
    '''파일 검색 및 페이지네이션 구현'''

    # **세션 상태에서 현재 페이지 저장**
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1  # 초기 페이지 설정
        
    with open('data/latest_biz.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    st.header("📂 지원 사업 검색")

    # 검색 입력창
    search_term = st.text_input("검색어를 입력하세요:", placeholder="키워드 검색")

    all_data = data.get("금융", [])  # 금융 항목 데이터 불러오기
    items_per_page = 10  # 한 페이지에 표시할 개수

    # 검색 결과 필터링
    results = []
    if search_term:
        search_term_lower = search_term.lower()
        for item in all_data:
            if isinstance(item, dict) and '지원사업 공고명' in item and search_term_lower in item['지원사업 공고명'].lower():
                results.append(item)

    # 검색 결과 존재 여부에 따라 표시할 데이터 결정
    display_items = results if search_term else all_data  

    if search_term and not results:
        st.write("검색 결과가 없습니다.")
        return

    total_items = len(display_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page  # 총 페이지 수 계산

    # **페이지네이션 UI**
    selected_page = sac.pagination(
        total=total_items,  # 🔥 **데이터 개수 기준으로 설정**
        page_size=items_per_page,  # 페이지당 항목 개수 지정
        align='center',
        color='indigo',
        jump=True,
        show_total=True
    )

    # **페이지 값이 바뀌었을 때 세션 상태 업데이트**
    if selected_page and selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page

    # **현재 페이지에 맞는 데이터 추출**
    page_number = st.session_state.current_page - 1  # 0부터 시작하도록 변환
    start_idx = page_number * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)  # 인덱스 초과 방지
    paged_data = display_items[start_idx:end_idx]

    # **페이지 정보 출력**
    st.write(f"📌 현재 페이지: {st.session_state.current_page} / 총 페이지: {total_pages}")

    # **지원 사업 목록 출력**
    for result in paged_data:
        with st.expander(f"**{result['지원사업 공고명']}**"):
            split_text = result['summary'].split('\n\n')
            for idx in split_text:
                info = idx.replace('```', '').strip()
                detail_info = info.split("\n", 1)
                st.markdown(f"**{detail_info[0].strip()}**")
                try:
                    if "|" in detail_info[1]:
                        result = convert_table_to_dict(detail_info[1])
                        df = pd.DataFrame(result)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        styled_text = f"""
                        <div style="
                            background-color: #fdfdfd; 
                            border-left: 5px solid #2C3E50; 
                            padding: 10px; 
                            border-radius: 5px;
                            font-size: 16px;
                            line-height: 1.6;
                        ">
                            {format_text_with_bullet_points(detail_info[1])}
                        </div>
                        """
                        st.markdown(styled_text, unsafe_allow_html=True)
                        st.markdown("\n")
                    st.write("\n")
                except:
                    pass

def businessplan_page():
    '''사업 계획서 초안 작성 페이지'''
    if st.session_state["authenticated"] == False:
        st.error('로그인 후 이용해주세요.')

    else:
        # 페이지 메인 제목
        st.header('📄 AI 사업 계획서 초안 작성')

        st.write('📌 사업 계획서 유형을 선택해주세요.')

        # 세션 상태를 이용한 선택값 저장
        if "selected_template" not in st.session_state:
            st.session_state.selected_template = None  # 초기값 설정
        
        selected_template =sac.segmented(
            items=[
                sac.SegmentedItem(label='사업 계획서 유형', disabled=True),
                sac.SegmentedItem(label='예비창업패키지', icon='file-earmark-text-fill'),
                sac.SegmentedItem(label='초기창업패키지', icon='file-earmark-text-fill'),
                sac.SegmentedItem(label='청년창업사관학교', icon='file-earmark-text-fill')
            ], label='', divider=False, use_container_width=True
        )

        # 선택된 값을 세션 상태에 저장
        st.session_state.selected_template = selected_template

        # template으로 예비창업패키지를 선택한 경우
        if st.session_state.selected_template == '예비창업패키지':
            
            # 사용자에게 사업 정보를 입력 받음
            item_info = ycp_get_user_input()
            if st.button("📄 사업계획서 작성하기"):
                with st.spinner("🔄 Loading...잠시만 기다려 주세요!"):
                    # papermill을 사용하여 노트북 실행
                    pm.execute_notebook(
                        'business_plan/예비창업패키지.ipynb',  # 실행할 Jupyter 노트북 경로
                        'business_plan/output.ipynb',  # 실행 결과를 저장할 출력 파일 경로
                        parameters={'loaded_data': item_info}  # item_info 파라미터 전달
                    )

                    # JSON 파일을 읽어와 딕셔너리로 변환
                    with open('business_plan/예비창업패키지_사업계획서.json', 'r', encoding='utf-8') as file:
                        plan = json.load(file)

                    # 사업계획서의 문항들을 전체 텍스트로 합체
                    result = "\n\n".join(plan.values())

                    with st.expander("⬇️ 사업계획서 파일 다운로드"):
                        # PDF 파일을 바이너리로 읽어서 BytesIO에 담기
                        with open("business_plan/예비창업패키지_초안.pdf", "rb") as f:
                            pdf_bytes = BytesIO(f.read())

                        # 다운로드 버튼 생성
                        st.download_button(
                            label="📜 사업계획서_초안.pdf",
                            data=pdf_bytes,
                            file_name="사업계획서_초안.pdf",
                            mime="application/pdf"
        )

                    with st.expander("🔍 사업계획서 내용 미리보기"):
                        st.code(result, language="plaintext")

        # template으로 초기창업패키지를 선택한 경우
        elif st.session_state.selected_template == '초기창업패키지':
            
            # 사용자에게 사업 정보를 입력 받음
            item_info = ccp_get_user_input()
            if st.button("📄 사업계획서 작성하기"):
                with st.spinner("🔄 Loading...잠시만 기다려 주세요!"):
                    # papermill을 사용하여 노트북 실행
                    pm.execute_notebook(
                        'business_plan/초기창업패키지.ipynb',  # 실행할 Jupyter 노트북 경로
                        'business_plan/output.ipynb',  # 실행 결과를 저장할 출력 파일 경로
                        parameters={'loaded_data': item_info}  # item_info 파라미터 전달
                    )

                    # JSON 파일을 읽어와 딕셔너리로 변환
                    with open('business_plan/초기창업패키지_사업계획서.json', 'r', encoding='utf-8') as file:
                        plan = json.load(file)

                    result = "\n\n".join(plan.values())

                    with st.expander("⬇️ 사업계획서 파일 다운로드"):
                        # PDF 파일을 바이너리로 읽어서 BytesIO에 담기
                        with open("business_plan/초기창업패키지_초안.pdf", "rb") as f:
                            pdf_bytes = BytesIO(f.read())

                        # 다운로드 버튼 생성
                        st.download_button(
                            label="📜 사업계획서_초안.pdf",
                            data=pdf_bytes,
                            file_name="사업계획서_초안.pdf",
                            mime="application/pdf"
        )

                    with st.expander("🔍 사업계획서 내용 미리보기"):
                        st.code(result, language="plaintext")


        # template으로 청년창업사관학교를 선택한 경우
        if st.session_state.selected_template == '청년창업사관학교':
            
            # 사용자에게 사업 정보를 입력 받음
            item_info = ccs_get_user_input()
            if st.button("📄 사업계획서 작성하기"):
                with st.spinner("🔄 Loading...잠시만 기다려 주세요!"):
                    # papermill을 사용하여 노트북 실행
                    pm.execute_notebook(
                        'business_plan/청년창업사관학교.ipynb',  # 실행할 Jupyter 노트북 경로
                        'business_plan/output.ipynb',  # 실행 결과를 저장할 출력 파일 경로
                        parameters={'item_info': item_info}  # item_info 파라미터 전달
                    )

                    # JSON 파일을 읽어와 딕셔너리로 변환
                    with open('business_plan/청년창업사관학교_사업계획서.json', 'r', encoding='utf-8') as file:
                        plan = json.load(file)

                    # 사업계획서의 문항들을 전체 텍스트로 합체
                    result = "\n\n".join(plan.values())

                    with st.expander("⬇️ 사업계획서 파일 다운로드"):
                        # PDF 파일을 바이너리로 읽어서 BytesIO에 담기
                        with open("business_plan/청년창업사관학교_초안.pdf", "rb") as f:
                            pdf_bytes = BytesIO(f.read())

                        # 다운로드 버튼 생성
                        st.download_button(
                            label="📜 사업계획서_초안.pdf",
                            data=pdf_bytes,
                            file_name="사업계획서_초안.pdf",
                            mime="application/pdf"
        )
                    

                    with st.expander("🔍 사업계획서 내용 미리보기"):
                        st.code(result, language="plaintext")

def my_page():
    '''마이페이지'''
    # 세션 상태를 이용한 선택값 저장
    if "my_tabs" not in st.session_state:
        st.session_state.my_tabs = None  # 초기값 설정

    my_tabs = sac.tabs([
    sac.TabsItem(label=f'{st.session_state["username"]}님의 페이지', disabled=True),
    sac.TabsItem(label='이전 지원사업 추천 내역'),
    sac.TabsItem(label='사용자 정보 변경', disabled=True),
    sac.TabsItem(label='공고 달력', disabled=True)
], align='center', use_container_width=True)
    
    st.session_state.my_tabs = my_tabs


    if st.session_state.my_tabs == "이전 지원사업 추천 내역":

        # 현재 접속해 있는 유저의 내역으로 접근
        with open(f'users/{st.session_state["username"]}data.json', 'r', encoding='utf-8') as f:
            content = json.load(f)

        st.write("📌 **최근 검색 기록 5개**만 보여드려요")
        st.dataframe(content[::-1][:5])