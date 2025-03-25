from user_input import get_user_input
from prompt_generator import generate_prompt
from openai_api import generate_business_plan
from save_results import save_to_file

# 1️⃣ 사용자 입력 받기
item_info = get_user_input()

# 2️⃣ 섹션별 사업계획서 생성
sections = [
    "제품 및 서비스 개발동기 및 필요성",
    "개발 방안",
    "시장진입 및 자금조달",
    "팀 구성 및 사회적 가치"
]

business_plans = {}

for section in sections:
    prompt = generate_prompt(section, item_info)
    business_plans[section] = generate_business_plan(prompt)

# 3️⃣ 생성된 사업계획서 출력
for section, content in business_plans.items():
    print(f"\n[{section}]\n{content}\n")

# 4️⃣ 결과 저장
save_to_file(item_info['아이템 명'], business_plans)
