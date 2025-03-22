import openai
import streamlit as st
import os

# OpenAI API 키 설정 (환경 변수 사용 권장)
from openai import OpenAI
client = OpenAI(api_key=os.getenv("api변경"))

def generate_business_plan(item_name, item_description):
    """
    OpenAI GPT-4 API를 사용하여 사업계획서 초안을 생성하는 함수.
    """
    prompt = f"사업계획서 초안을 작성해 주세요. 아이템명: {item_name}, 아이템 소개: {item_description}"

    # 최신 OpenAI API 사용
    response = client.chat.completions.create(
        model="gpt-4",  # 또는 "gpt-3.5-turbo" 사용 가능
        messages=[
            {"role": "system", "content": "당신은 사업계획서 작성 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7
    )
    
    # response에서 text 추출
    return response.choices[0].message.content.strip()

def business_plan_draft():
    st.title("🚀 사업계획서 초안 작성")

    st.markdown("""
    ### 📌 **사업계획서 작성 안내**
    1. 본 서비스는 체험판으로 제공됩니다.
    2. 작성 중 페이지를 종료하면 입력한 내용이 저장되지 않습니다.
    3. 제출 후, 작성 내용을 수정하거나 확인할 수 없습니다.
    """)

    st.markdown("### 📄 사업계획서 초안을 작성해 주세요.")

    # 지원 사업 선택
    option = st.selectbox(
        "어떤 사업계획서를 작성하시겠습니까?",
        ["청년 창업 사관학교", "예비 창업 패키지", "초기 창업 패키지"]
    )

    # 아이템명 및 설명 입력
    item_name = st.text_input("아이템명", "아이템명을 작성해주세요")
    item_description = st.text_area("아이템 소개", "아이템 소개글을 작성해주세요")

    # AI 사업계획서 생성
    if st.button("📌 AI로 사업계획서 작성하기", key="generate_button"):
        if item_name and item_description:
            with st.spinner("⏳ 사업계획서를 작성하는 중입니다..."):
                generated_plan = generate_business_plan(item_name, item_description)
                st.subheader("✅ 작성된 사업계획서 초안:")
                st.markdown(generated_plan)
        else:
            st.warning("⚠️ 아이템명과 아이템 소개를 모두 입력해 주세요.")

# business_plan_draft 함수 호출
business_plan_draft()
