import streamlit as st
import json
import os

# SeSAC_Final-test 폴더 경로
base_folder_path = './SeSAC_Final-test/'

# bizinfo.json 파일 경로
json_file_path = os.path.join(base_folder_path, 'bizinfo.json')

# JSON 파일을 로드하는 함수
def load_json_data(file_path):  # 인자 받도록 수정
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except Exception as e:
        st.error(f"파일 로드 오류: {str(e)}")
        return None

# Streamlit 앱 설정
def main():
    st.title("Bizinfo 검색")

    # 검색 입력창
    search_term = st.text_input("검색어를 입력하세요:")

    if search_term:
        # JSON 데이터를 로드
        data = load_json_data(json_file_path)

        if data is not None:
            # 검색어를 소문자로 변환하여 처리
            search_term_lower = search_term.lower()

            # '금융' 항목 아래 데이터를 검색
            results = []
            for category, items in data.items():  # '금융' 같은 키를 기준으로 반복
                for item in items:
                    # '지원사업 공고명'에서 검색어가 포함되어 있는지 확인
                    if isinstance(item, dict) and '지원사업 공고명' in item and search_term_lower in item['지원사업 공고명'].lower():
                        results.append(item)

            # 검색 결과 출력
            if results:
                st.write(f"총 {len(results)}개의 항목이 검색되었습니다.")
                for result in results:
                    st.json(result)  # 검색 결과 출력
            else:
                st.write("검색 결과가 없습니다.")
        else:
            st.write("데이터를 불러올 수 없습니다.")
    else:
        st.write("검색어를 입력해주세요.")

if __name__ == "__main__":
    main()

``

