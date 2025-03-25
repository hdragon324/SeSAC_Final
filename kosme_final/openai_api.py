import openai
import time

def generate_business_plan(prompt):
    """
    OpenAI API를 사용하여 사업계획서 초안을 생성하는 함수
    """
    client = openai.OpenAI()  # API 키 설정 필요
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{'role': 'system', 'content': prompt}],
        temperature=0.7,
        presence_penalty=0.8,
        frequency_penalty=0.5,
        max_tokens=4000
    )

    # 응답 결과 정리
    result = response.choices[0].message.content.replace("### ", "")

    # 각 문항 작성 후 대기
    sentences = result.split('\n')  # 문장 단위로 분리
    processed_result = ""
    for sentence in sentences:
        processed_result += sentence + '\n'
        time.sleep(2) 

    return processed_result
