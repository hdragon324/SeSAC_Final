from langchain.document_loaders import PyPDFLoader

import cv2
import re
import zlib
import struct
import olefile
import pytesseract

import numpy as np
import platform
from PIL import ImageFont, ImageDraw, Image
from matplotlib import pyplot as plt
 
import uuid
import json
import time
import cv2
import requests

def get_pdf_text(filename):

    # PyPDFLoader를 사용하여 PDF 파일 로드
    loader = PyPDFLoader(filename)
    documents = loader.load()

    # 전체 텍스트를 하나의 문자열로 저장
    text = "\n".join([doc.page_content for doc in documents])

    return text

def get_hwp_text(filename):
    # HWP 파일을 읽기 위한 olefile 객체 생성
    f = olefile.OleFileIO(filename)
    
    # HWP 파일 내의 디렉터리 목록을 가져옴
    dirs = f.listdir()

    # HWP 파일이 올바른 형식인지 확인 (FileHeader와 HwpSummaryInformation이 존재해야 함)
    if ["FileHeader"] not in dirs or \
            ["\x05HwpSummaryInformation"] not in dirs:
        raise Exception("Not Valid HWP.")

    # FileHeader 스트림을 열고 해당 데이터를 읽음
    header = f.openstream("FileHeader")
    header_data = header.read()

    # 파일이 압축되어 있는지 여부를 확인 (헤더의 36번째 바이트에 정보 있음)
    is_compressed = (header_data[36] & 1) == 1

    # BodyText 섹션의 번호를 찾기 위해 디렉토리에서 "Section"을 포함하는 항목 찾음
    nums = []
    for d in dirs:
        if d[0] == "BodyText":
            nums.append(int(d[1][len("Section"):]))

    # 섹션을 번호순으로 정렬하고 "BodyText/Section" 형식으로 리스트 생성
    sections = ["BodyText/Section" + str(x) for x in sorted(nums)]

    text = ""  # 최종적으로 추출될 텍스트 초기화

    # 각 섹션을 순차적으로 처리
    for section in sections:
        # 해당 섹션을 열고 데이터 읽기
        bodytext = f.openstream(section)
        data = bodytext.read()

        # 파일이 압축된 경우 압축을 해제
        if is_compressed:
            unpacked_data = zlib.decompress(data, -15)
        else:
            unpacked_data = data

        section_text = ""  # 각 섹션의 텍스트를 담을 변수
        i = 0
        size = len(unpacked_data)

        # 섹션 데이터에서 텍스트를 추출
        while i < size:
            # 각 레코드의 헤더를 읽고, 레코드 타입과 길이를 추출
            header = struct.unpack_from("<I", unpacked_data, i)[0]
            rec_type = header & 0x3ff  # 레코드 타입 추출
            rec_len = (header >> 20) & 0xfff  # 레코드 길이 추출

            # 레코드 타입이 67일 때 텍스트를 추출 (67은 텍스트 레코드 타입)
            if rec_type in [67]:
                rec_data = unpacked_data[i + 4:i + 4 + rec_len]
                section_text += rec_data.decode('utf-16')  # 텍스트를 UTF-16으로 디코딩
                section_text += "\n"  # 줄 바꿈 추가

            # 다음 레코드로 이동
            i += 4 + rec_len

        # 섹션의 텍스트를 전체 텍스트에 추가
        text += section_text
        text += "\n"  # 섹션 간에 줄 바꿈 추가

        text = re.sub(r'[^\x00-\x7F\uAC00-\uD7AF]', '', text)
        
    return text  # 최종적으로 추출된 텍스트 반환

# def get_image_text(filename):
#     # Tesseract-OCR 경로 설정
#     pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\every\\Desktop\\Project\\team_project\\SeSAC_Final\\AI-for-Creating-Business-Plan-Drafts\\OCR\\tesseract.exe"


#     # 이미지 로드
#     img = cv2.imread(filename)
#     dst = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # tesseract에서는 RGB로 넣어야 하기 때문에 변환

#     # 이미지에서 텍스트 추출
#     text = pytesseract.image_to_string(dst, lang='kor+eng')
    
#     return text

def put_text(image, text, x, y, color=(0, 255, 0), font_size=22):
    '''한글 깨짐을 방지하기 위한 함수'''
    if type(image) == np.ndarray:
        color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(color_coverted)
 
    if platform.system() == 'Darwin':
        font = 'AppleGothic.ttf'
    elif platform.system() == 'Windows':
        font = 'malgun.ttf'
        
    image_font = ImageFont.truetype(font, font_size)
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)
 
    draw.text((x, y), text, font=image_font, fill=color)
    
    numpy_image = np.array(image)
    opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
 
    return opencv_image

def get_image_text(path):
    api_url = 'https://dqfp3rdhcw.apigw.ntruss.com/custom/v1/39549/6ec703e8b494511fd50f11c0df474b47bdc8717eb906e3b6c5bab61e56621fba/general' # NAVER CLOVA invoke url 입력
    secret_key = 'U290ZXdjRFpBWVhPcFFGVWplRVRJT0RBQk9FS1VBb0k=' # NAVER CLOVA key 입력

    files = [('file', open(path,'rb'))]

    request_json = {'images': [{'format': 'jpg',
                                'name': 'demo'
                               }],
                    'requestId': str(uuid.uuid4()),
                    'version': 'V2',
                    'timestamp': int(round(time.time() * 1000))
                   }
 
    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    
    headers = {
    'X-OCR-SECRET': secret_key,
    }
    
    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    result = response.json()

    img = cv2.imread(path)
    roi_img = img.copy()

    # 추출된 텍스트를 저장할 리스트
    extracted_texts = []

    for field in result['images'][0]['fields']:
        text = field['inferText']
        extracted_texts.append(text)  # 리스트에 저장

        vertices_list = field['boundingPoly']['vertices']
        pts = [tuple(vertice.values()) for vertice in vertices_list]
        topLeft = [int(_) for _ in pts[0]]
        topRight = [int(_) for _ in pts[1]]
        bottomRight = [int(_) for _ in pts[2]]
        bottomLeft = [int(_) for _ in pts[3]]

        cv2.line(roi_img, topLeft, topRight, (0,255,0), 2)
        cv2.line(roi_img, topRight, bottomRight, (0,255,0), 2)
        cv2.line(roi_img, bottomRight, bottomLeft, (0,255,0), 2)
        cv2.line(roi_img, bottomLeft, topLeft, (0,255,0), 2)

        roi_img = put_text(roi_img, text, topLeft[0], topLeft[1] - 10, font_size=30)
  
    # 각 단어를 공백 구분자로 구분
    result = " ".join(extracted_texts)

    return result