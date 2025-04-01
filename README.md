# AI-for-Creating-Business-Plan-Drafts

## 초기세팅
'''plaintext
0. module_install.ipynb를  먼저 실행하세요

1.
business_plan/예비창업패키지.ipynb
business_plan/초기창업패키지.ipynb
business_plan/청년창업사관학교.ipynb
utils/summary.py fine_tune_summary(text, title)

client = OpenAI(api_key='YOUR_API_KEY')
에 본인의 api_key를 입력하세요 (OpenAI)

2.
utils/get_text.py def get_image_text(path)

api_url = 'YOUR_INVOKE_URL' 
secret_key = 'YOUR_API_KEY'
에 본인의 api_key, invoke_url을 입력하세요 (Naver Clova)

3.
data/fine_tune_test.ipynb에서 생생한 model을
utils/get_text.py def get_image_text(path)
의 model에 입력하세요

4. 
auto.py의 파일 경로를 입력하세요
'''

## 파일 구조

'''plaintext
AI-FOR-CREATING-BUSINESS-PLAN/
│── business_plan/                        # 사업계획서 초안 작성 서비스
│   │── output.ipynb                      # papermill의 결과가 출력되는 jupyter notebook 파일
│   │── 예비창업패키지_사업계획서.json      # 작성된 사업계획서를 json 파일로 저장
│   │── 예비창업패키지_초안.docx            # 작성된 사업계획서를 docx 파일로 저장
│   │── 예비창업패키지_초안.pdf             # docx 파일을 pdf 파일로 변환하여 저장
│   │── 예비창업패키지.ipynb                # papermill을 사용하여 실행할 jupyter notebook 파일
│   │── 청년창업사관학교_사업계획서.pdf
│   │── 청년창업사관학교_초안.docx
│   │── 청년창업사관학교_초안.json
│   │── 청년창업사관학교.ipynb
│   │── 초기창업패키지_사업계획서.json
│   │── 초기창업패키지_초안.docx
│   │── 초기창업패키지_초안.pdf
│   │── 초기창업패키지.ipynb
│
│── data/                                   # 공고 추천 서비스 데이터
│   │── fine_tune_test.ipynb                # fine-tune 모델을 만들기 위한 test 파일
│   │── latest_biz.json                     # 최신 공고 리스트 DB
│   │── previous_biz.json                   # 지난 공고 리스트 DB
│
│── image_movie/                            # streamlit 꾸미기용 파일
│   │── ddapp_movie.mp4                 
│   │── ddapp.png
│
│── users/                                  # 회원가입한 유저들의 이용내역, 회원 정보
│   │── config.yaml                         # 회원가입 정보
│
│── utils/                                  # 사용자 정의 함수 기능들 정리 파일
│   │── __pycache__/
│   │── __init__.py
│   │── authenticator.py                    # 회원가입 (비밀번호 확인, 아이디 중복, 이메일 중복) 확인
│   │── get_text.py                         # pdf, hwp, img 파일에서 텍스트 추출
│   │── pages.py                            # streamlit 페이지 구현
│   │── recommend.py                        # 지원 사업 추천 (코사인 유사도, 벡터 검색)
│   │── summary.py                          # 지원 사업 텍스트 요약 (RAG 모델 사용)
│   │── template.py                         # 요약된 텍스트 중 표 구현을 위한 템플릿
│   │── 경영/                               # 지원사업 분류 목록
│   │── 금융/
│   │── 기술/
│   │── 기타/
│   │── 내수/
│   │── 수출/
│   │── 인력/
│   │── 창업/
│
│── app.py                                  # **streamlit 실행 파일**
│── auto.bat                                # 스케줄러를 이용한 크롤링 자동화를 위한 batch 파일
│── auto.py                                 # 자동화를 실행할 파일 -> update_crawl.ipynb를 실행
│── module_install_list.ipynb               # 설치해야할 모듈             
│── README.md                               # 초기세팅 및 파일 구조 설명
│── update_crawl_output.json                # 크롤링 결과가 출력되는 파일
│── update_crawl.ipynb                      # 공고 업데이트 크롤링 (papermill로 실행)
'''
