from langchain.document_loaders import PyPDFLoader

import re
import olefile
import zlib
import struct

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