import torch
import streamlit as st
import streamlit_antd_components as sac
from utils.pages import home_page, recommendation_page, login_page, register_page, search_file_page, businessplan_page, my_page

torch.classes.__path__ = [] # add this line to manually set it to empty.

st.set_page_config(page_title="떴다앱", page_icon='image_movie/ddapp.png',layout="wide")

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "홈"

# 세션 상태 초기화
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 만약 로그인을 하지 않은 상태라면
if st.session_state["authenticated"] == False:
    
    with st.sidebar:
        selected_menu = sac.menu([
            sac.MenuItem('홈', icon='house-fill'),
            sac.MenuItem('서비스', icon='box-fill', children=[
                sac.MenuItem('지원 사업 추천', icon='folder-fill'),
                sac.MenuItem('지원 사업 검색', icon='folder-fill'),
                sac.MenuItem('AI 사업계획서 초안', icon='folder-fill')
            ]),
            sac.MenuItem(type='divider'),
            sac.MenuItem('로그인', icon='person-fill'),
            sac.MenuItem('회원가입', icon='person-fill')
        ], color='blue', open_all=True)

elif st.session_state["authenticated"] == True:

    with st.sidebar:
        selected_menu = sac.menu([
            sac.MenuItem('홈', icon='house-fill'),
            sac.MenuItem('서비스', icon='box-fill', children=[
                sac.MenuItem('지원 사업 추천', icon='folder-fill'),
                sac.MenuItem('지원 사업 검색', icon='folder-fill'),
                sac.MenuItem('AI 사업계획서 초안', icon='folder-fill')
            ]),
            sac.MenuItem(type='divider'),
            sac.MenuItem('로그아웃', icon='person-fill'),
            sac.MenuItem('마이페이지', icon='person-fill'),
        ], color='blue', open_all=True)


# 선택한 메뉴를 세션 상태에 저장
if selected_menu:  # 사용자가 선택한 메뉴가 있으면
    st.session_state.page = selected_menu

# 페이지 렌더링
if st.session_state.page == "홈":
    home_page()

elif st.session_state.page == "지원 사업 추천":
    recommendation_page()

elif st.session_state.page == "지원 사업 검색":
    search_file_page()

elif st.session_state.page == "AI 사업계획서 초안":
    businessplan_page()

elif st.session_state.page == "로그인":
    login_page()

elif st.session_state.page == "로그아웃":
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.rerun()

elif st.session_state.page == "회원가입":
    register_page()

elif st.session_state.page == "마이페이지":
    my_page()

# ------------------------------------------------------------------------