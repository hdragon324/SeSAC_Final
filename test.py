# test.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_links(hashcode, header):
    '''기업마당의 메인에 있는 공고 각각의 URL을 리스트로 반환'''
    BASE_URL = 'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/'
    idx = 1         # 페이지를 넘기기 위한 인덱스
    links = []      # 링크를 정리해둘 리스트 선언

    # 공고가 없는 페이지가 나올 때까지 반복문
    while True:
        URL = f'https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do?hashCode={hashcode}&cpage={idx}'
        response = requests.get(URL, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 공고가 없는 페이지가 나올 시 반복문 탈출
        if len(soup.select('div.sub_cont tr')) == 2:
            break
        
        # links에 URL 저장
        links += [BASE_URL + link.attrs['href'] for link in soup.select('td.txt_l a')]

        # 페이지 넘김
        idx += 1

    return links

def get_file_data(links, header):
    '''각 공고 링크에서 파일 관련 데이터 추출'''
    file_data = []
    for link in links:
        response = requests.get(link, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 제목 추출을 확인
        try:
            down_title = soup.select_one('h2.title').text
        except AttributeError:
            down_title = "제목 없음"  # 제목이 없을 경우 기본 값으로 설정

        # 다운로드 링크 추출을 확인
        try:
            down_link = soup.select('div.attached_file_list div.right_btn a')[-1].attrs['href']
        except (AttributeError, IndexError):
            down_link = None  # 다운로드 링크가 없을 경우 처리

        # 링크가 존재하면 URL로 변환
        if down_link:
            down_url = 'https://www.bizinfo.go.kr' + down_link
        else:
            down_url = None
        
        # 데이터가 있을 때만 추가
        if down_title and down_url:
            file_data.append({
                'title': down_title,
                'url': down_url
            })

    return file_data

# 크롤링 함수 실행 및 데이터 저장
def save_crawled_data(hashcode, header):
    links = fetch_links(hashcode, header)
    file_data = get_file_data(links, header)

    # 크롤링한 데이터를 DataFrame으로 저장
    df = pd.DataFrame(file_data)

    # 데이터 저장 (예: CSV 파일로 저장)
    df.to_csv('crawled_data.csv', index=False)
    return df

