import streamlit as st
import openai
import os
import kosme  # kosme.py 파일을 임포트

# ✅ ✅ ✅ set_page_config()를 가장 위에 위치시킵니다.
st.set_page_config(page_title="맞춤 지원 공고 추천", layout="wide")

# ✅ input.txt에서 OpenAI API 키 읽기
def load_api_key(file_path="input.txt"):
    with open(file_path, "r") as file:
        return file.read().strip()

api_key = load_api_key()  # API 키 불러오기

# OpenAI API 클라이언트 설정
client = openai.OpenAI(api_key=api_key)

def generate_business_plan(inputs):
    """
    OpenAI GPT-4 API를 사용하여 사업계획서 초안을 단계별로 생성하는 함수.
    kosme.py의 데이터를 활용하여 작성합니다.
    """
    kosme_data = kosme.get_business_plan_data(inputs)
    
    if not isinstance(kosme_data, dict):
        raise ValueError("kosme.get_business_plan_data() 함수는 딕셔너리를 반환해야 합니다.")
    
    prompts = {
        "제품 및 서비스 개발동기": inputs["제품 및 서비스 개발동기"],
        "제품 및 서비스의 목적(필요성)": inputs["제품 및 서비스의 목적_필요성"],
        "제품 및 서비스의 개발 방안": inputs["제품 및 서비스의 개발 방안"],
        "자금 조달 및 개발 방안": inputs["자금 조달 및 개발 방안"],
        "내수시장 확보 방안": inputs["내수시장 확보 방안 경쟁 및 판매가능성"],
        "해외시장 진출 방안": inputs["해외시장 진출 방안 경쟁 및 판매가능성"],
        "대표자 및 직원의 보유역량 및 기술보호 노력": inputs["대표자 및 직원의 보유역량 및 기술보호 노력"],
        "사회적 가치 실천계획": inputs["사회적 가치 실천계획"],
        "지역특화 아이디어 기반 사업추진계획": inputs["지역특화 아이디어 기반 사업추진계획"],
        "타겟 고객": inputs["타겟 고객"],
        "시장 규모": inputs["시장 규모"],
        "경쟁사 분석": inputs["경쟁사 분석"]
    }
    
    responses = {}
    for section, content in prompts.items():
        if content.strip():
            messages = [
                {"role": "system", "content": "당신은 사업계획서 작성 전문가입니다."},
                {"role": "user", "content": f"{section}: {content}"}
            ]
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
            )
            
            responses[section] = response.choices[0].message.content.strip()
    
    return responses

def business_plan_draft():
    st.title("🚀 사업계획서 초안 작성")

    st.markdown(""" 
    ### 📌 **사업계획서 작성 안내**
    1. 본 서비스는 체험판으로 제공됩니다.
    2. 작성 중 페이지를 종료하면 입력한 내용이 저장되지 않습니다.
    3. 제출 후, 작성 내용을 수정하거나 확인할 수 없습니다.
    """)

    st.markdown("### 📄 사업계획서 초안을 작성해 주세요.")

    # 입력 필드
    inputs = {
        '아이템 명': st.text_input("아이템 명", "아이템명을 작성해주세요"),
        '아이템 소개': st.text_area("아이템 소개", "아이템 소개글을 작성해주세요"),
        '제품 및 서비스 개발동기': st.text_area("제품 및 서비스 개발동기", "제품 및 서비스의 개발동기를 작성해주세요."),
        '제품 및 서비스의 목적_필요성': st.text_area("제품 및 서비스의 목적(필요성)", "제품 및 서비스의 목적과 필요성에 대해 작성해주세요."),
        '제품 및 서비스의 개발 방안': st.text_area("제품 및 서비스의 개발 방안", "제품 및 서비스의 개발 방안을 작성해주세요."),
        '자금 조달 및 개발 방안': st.text_area("자금 조달 및 개발 방안", "자금 조달 및 개발 방안을 작성해주세요."),
        '내수시장 확보 방안 경쟁 및 판매가능성': st.text_area("내수시장 확보 방안 (경쟁 및 판매가능성)", "내수시장 확보 방안과 경쟁 및 판매 가능성에 대해 작성해주세요."),
        '해외시장 진출 방안 경쟁 및 판매가능성': st.text_area("해외시장 진출 방안 (경쟁 및 판매가능성)", "해외시장 진출 방안과 경쟁 및 판매 가능성에 대해 작성해주세요."),
        '대표자 및 직원의 보유역량 및 기술보호 노력': st.text_area("대표자 및 직원의 보유역량 및 기술보호 노력", "대표자 및 직원의 역량과 기술 보호 노력에 대해 작성해주세요."),
        '사회적 가치 실천계획': st.text_area("사회적 가치 실천계획", "사회적 가치 실천 계획에 대해 작성해주세요."),
        '지역특화 아이디어 기반 사업추진계획': st.text_area("지역특화 아이디어 기반 사업추진계획", "지역특화 아이디어 기반 사업 추진 계획에 대해 작성해주세요."),
        '타겟 고객': st.text_area("타겟 고객", "타겟 고객에 대해 작성해주세요."),
        '시장 규모': st.text_area("시장 규모", "시장 규모에 대해 작성해주세요."),
        '경쟁사 분석': st.text_area("경쟁사 분석", "경쟁사 분석에 대해 작성해주세요.")
    }

    # AI 사업계획서 생성
    if st.button("📌 AI로 사업계획서 작성하기"):
        if inputs['아이템 명'] and inputs['아이템 소개']:
            with st.spinner("⏳ 사업계획서를 작성하는 중입니다..."):
                generated_plan = generate_business_plan(inputs)
                st.subheader("✅ 작성된 사업계획서 초안: ")
                for section, content in generated_plan.items():
                    st.subheader(section)
                    st.write(content)
        else:
            st.warning("⚠️ 아이템명과 아이템 소개를 모두 입력해 주세요.")

# 🚀 **메인 함수 실행**
business_plan_draft()
