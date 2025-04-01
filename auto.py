import papermill as pm

# 실행할 Jupyter Notebook 파일 경로
notebook_input = r"{파일경로}\update_crawl.ipynb"
notebook_output = r"{파일경로}\update_crawl_output.ipynb"

# Papermill을 사용하여 Notebook 실행
try:
    pm.execute_notebook(
        notebook_input,   # 원본 노트북
        notebook_output,  # 실행 후 저장할 노트북
        log_output=True   # 실행 로그 출력
    )
    print("📌 Jupyter Notebook 실행 완료!")
except Exception as e:
    print(f"⚠️ 오류 발생: {e}")