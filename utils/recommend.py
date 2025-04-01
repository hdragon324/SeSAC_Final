from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import json
import faiss
import numpy as np
import streamlit as st
import pandas as pd

def convert_table_to_dict(table_text):
    '''텍스트에서 df 테이블로 데이터를 바꾸기 위한 함수'''
    lines = table_text.strip().split("\n")  # 줄바꿈을 기준으로 분할
    headers = lines[0].split("|")[1:-1]  # 첫 번째 줄(헤더)에서 양 끝 "|" 제거 후 분할
    headers = [header.strip() for header in headers]  # 공백 제거

    data = {header: [] for header in headers}  # 빈 딕셔너리 생성

    for line in lines[2:]:  # 데이터 부분만 순회 (구분선 제외)
        values = line.split("|")[1:-1]  # 양 끝 "|" 제거 후 분할
        values = [value.strip() for value in values]  # 공백 제거

        for i, header in enumerate(headers):
            data[header].append(values[i])  # 해당 키에 데이터 추가

    return data

def format_text_with_bullet_points(text):
    '''텍스트를 하이픈을 기준으로 줄바꿈하기 위한 함수'''
    # 여러 줄을 포함한 경우 "\n"으로 분리
    lines = text.split("\n")

    has_hyphen = any("- " in line for line in lines)  # 하이픈이 포함된 줄이 있는지 확인

    if has_hyphen:
        formatted_text = "<ul>"
        for line in lines:
            # 하이픈(`– `)을 기준으로 추가 분리 (줄바꿈이 없는 경우 포함)
            items = line.split("- ")
            for item in items:
                if item.strip():  # 빈 문자열 방지
                    formatted_text += f"<li>{item.strip()}</li>"
        formatted_text += "</ul>"
    else:
        # 하이픈이 없는 경우, 원래 텍스트를 그대로 출력 (줄바꿈도 유지)
        formatted_text = text.replace("\n", "<br>")

    return formatted_text


def cosine_similarity_recommend(user_input):
    # Sentence-Transformers 라이브러리에서 모델 로드
    # "intfloat/multilingual-e5-large" 모델은 다양한 언어에서 문장 임베딩을 생성할 수 있는 모델
    model = SentenceTransformer("intfloat/multilingual-e5-large")

    biz_embeddings = [] # 벡터를 저장할 리스트
    biz_names = [] # 공고명을 저장할 리스트
    biz_summaries = [] # 공고 요약을 저장할 리스트

    # 추천 지원사업의 데이터가 있는 파일을 읽음
    with open('data/latest_biz.json', 'r', encoding='utf-8') as f: # 파일 저장되어 있는 위치 수정할것
        data = json.load(f)

    for category, items in data.items():
        for item in items:
            if "vector" in item:  # 벡터 정보가 있는 경우만 추가
                vector = np.array(item["vector"])
                vector = vector / np.linalg.norm(vector)  # 벡터 정규화
                biz_embeddings.append(vector)
                biz_names.append(item["지원사업 공고명"])
                biz_summaries.append(item["summary"])

    # numpy 배열 변환
    biz_embeddings = np.array(biz_embeddings)

    # FAISS 인덱스 생성 (내적 기반 검색을 위해 IndexFlatIP 사용)
    biz_dimension = biz_embeddings.shape[1]  # 벡터 차원 수
    biz_index = faiss.IndexFlatIP(biz_dimension)
    biz_index.add(biz_embeddings)

    query = user_input

    query_vector = model.encode(query).reshape(1, -1)
    query_vector = query_vector / np.linalg.norm(query_vector)  # 정규화

    # ✅ 코사인 유사도 직접 계산하여 비교
    top_k = 1  # 검색할 개수
    similarities = cosine_similarity(query_vector, biz_embeddings)
    top_k_indices = np.argsort(similarities[0])[::-1][:top_k]

    # 펼치기 박스 추가
    st.write("🔎 추천 사업 결과 펼쳐보기")
    for i, idx in enumerate(top_k_indices):

        
        with st.expander(f"**{biz_names[idx]}**"):

            # 각 항목을 띄어쓰기 기준으로 나눔
            split_text = biz_summaries[idx].split('\n\n')

            for idx in split_text:
                info = idx.replace('```','').strip()
                detail_info = info.split("\n", 1) # 각 항목을 첫번째 띄어쓰기 한해서 나눔 (항목명, 세부사항)
                # 항목명 출력 (볼드 적용)
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

                        st.markdown(styled_text, unsafe_allow_html=True)  # 텍스트 내용 출력
                        st.markdown("\n")
                    st.write("\n")
                except:
                    pass

