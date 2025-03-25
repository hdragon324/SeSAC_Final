import streamlit as st
import time
from user_input import get_user_input
from prompt_generator import generate_prompt
from openai_api import generate_business_plan
from save_results import save_to_file

# 템플릿 및 가이드라인
kosme_template = "..."  # 제공된 템플릿
kosme_pass = "..."  # 제공된 가이드라인

st.title("🚀 AI 기반 사업계획서 자동 생성")

# 사용자 입력 받기
item_info = get_user_input()

# 사업계획서 생성 버튼 추가
if st.button("📄 사업계획서 작성하기"):
    sections = [
        "1. 문제 인식",
        "2. 실현 가능성",
        "3. 성장 전략",
        "4. 팀 구성"
    ]

    business_plans = {}
    progress_bar = st.progress(0)  # 진행률 바 초기화
    total_sections = len(sections)

    with st.spinner("⏳ AI가 사업계획서를 작성 중입니다..."):
        for idx, section in enumerate(sections):
            prompt = generate_prompt(section, item_info, kosme_template, kosme_pass)
            business_plans[section] = generate_business_plan(prompt)

            progress = int(((idx + 1) / total_sections) * 100)  # 진행률 계산
            progress_bar.progress(progress)  # 진행률 업데이트
            time.sleep(1)  # 가시성을 위해 1초 대기 (실제 AI 응답 시간 고려)

    st.success("✅ 사업계획서가 성공적으로 생성되었습니다!")

    # 생성된 결과 자동 저장
    json_filename = save_to_file(item_info['아이템 명'], business_plans)


    # 결과를 Streamlit 화면에 출력
    st.subheader("📌 생성된 사업계획서")
    for section, content in business_plans.items():
        with st.expander(f"📑 {section}"):
            st.text_area("출력 결과", content, height=200)
