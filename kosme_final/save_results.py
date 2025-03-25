import os
import json

def save_to_file(item_name, business_plans):
    """
    생성된 사업계획서를 JSON Lines 형식으로 자동 저장하는 함수
    """
    folder_path = "사용자 정보"  # 사용자 정보 폴더에 저장
    os.makedirs(folder_path, exist_ok=True)

    filename = os.path.join(folder_path, f"{item_name} 사업계획서.jsonl")

    with open(filename, 'a', encoding='utf-8') as f:
        json.dump({"사업계획서": business_plans}, f, ensure_ascii=False)
        f.write('\n')

    return filename  # 저장된 파일 경로 반환


