import streamlit as st
import hashlib
import yaml
import re
import os

# 비밀번호 해시화 함수
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# 비밀번호 유효성 검사 함수
def is_valid_password(password):
    if len(password) < 6:
        return False
    has_lower = re.search(r'[a-z]', password)
    has_digit = re.search(r'[0-9]', password)
    has_special = re.search(r'[\W_]', password)  # 특수문자
    return all([has_lower, has_digit, has_special])

# 사용자 정보 중복 확인 및 저장 함수
def save_user(username, email, hashed_password):
    config_path = 'users/config.yaml'

    # config.yaml 불러오기
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            if config is None:
                config = {'credentials': {'usernames': {}}}
    else:
        config = {'credentials': {'usernames': {}}}

    # 기존 사용자 목록
    existing_users = config['credentials']['usernames']

    # 중복 검사
    for user, details in existing_users.items():
        if user == username:
            return "이미 존재하는 사용자 이름입니다."
        if details['email'] == email:
            return "이미 등록된 이메일입니다."
    
    # 사용자 추가
    config['credentials']['usernames'][username] = {
        'email': email,
        'name': username,
        'password': hashed_password
    }

    # 저장
    with open(config_path, 'w') as file:
        yaml.dump(config, file)

    return "success"

# 사용자 인증
def authenticate_user(username, password):
    config_path = 'users/config.yaml'

    if not os.path.exists(config_path):
        return False, "사용자 데이터 파일이 존재하지 않습니다."

    with open(config_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    if config is None or 'credentials' not in config or 'usernames' not in config['credentials']:
        return False, "사용자 정보가 등록되어 있지 않습니다."

    users = config['credentials']['usernames']

    if username not in users:
        return False, "존재하지 않는 사용자 이름입니다."

    hashed_input_password = hash_password(password)
    stored_password = users[username]['password']

    if hashed_input_password != stored_password:
        return False, "비밀번호가 일치하지 않습니다."

    return True, f"{username}님, 환영합니다!"