import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
from collections import defaultdict
from eiken_common import load_csv_file, select_num_questions, select_question_kind, select_definite_questions, \
    calc_score, record_score

# Google Drive API の設定
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
service_account_info = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# 定数
FOLDER_ID = "1g3QmKiqP3iCOa_GQcRwL-rZ3DCI3Mf-Z"
RECORD_FILE_ID = "1sVwChcnOnkh6Ypllndc-jV42xqGoaGAu0uKLdHkKEBg"
PROBLEM_FILE_ID = '1nHONtGQM2Msy9Wos8O0WaQ1oMnZkiflweqFIaaMOyMU'


def list_files_in_folder(folder_id=None):
    """フォルダ内のファイルをリストし、ファイル名とIDを返す"""
    query = f"'{folder_id}' in parents" if folder_id else ""
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return {item['name']: item['id'] for item in results.get('files', [])}


def load_listening_file(file_id):
    """Google Drive から音声ファイルをダウンロードし、再生する"""
    request = drive_service.files().get_media(fileId=file_id)
    file_data = io.BytesIO()
    downloader = MediaIoBaseDownload(file_data, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    file_data.seek(0)
    st.audio(file_data, format='audio/mpeg')


def display_listening_question(question_index, row, file_map):
    """問題と選択肢を表示し、選択された回答を返す"""
    st.write(f"**問題 {question_index + 1}**")
    load_listening_file(file_map[f"audio{row['問題ID']}.mp3"])

    choice = st.radio(
        "選択肢を選んでください:",
        [f"A: {row['選択肢A']}", f"B: {row['選択肢B']}", f"C: {row['選択肢C']}", f"D: {row['選択肢D']}"],
        key=f"question_{question_index}",
        horizontal=True
    )
    return choice[:1]  # 選択肢の頭文字 (A, B, C, D) を返す


def app(page):
    st.title(f"英検{page}問題")

    choice = select_question_kind()[:1]
    reflection_flag = 0
    id_to_answer = defaultdict(int)
    id_to_choice = defaultdict(int)

    options = ["A", "B", "C", "D"]

    # ページが初めて読み込まれたときのみセッションをクリアする
    if "page_initialized" not in st.session_state or st.session_state.page_initialized != page:
        st.session_state.clear()
        st.session_state.page_initialized = page

    file_map = list_files_in_folder(FOLDER_ID)

    if choice == "A":
        nums = select_num_questions()
        if PROBLEM_FILE_ID:
            data = pd.DataFrame(load_csv_file(PROBLEM_FILE_ID))

            # 初回のみデータフレームの行をランダムにシャッフルして保存
            if "randomized_data" not in st.session_state:
                st.session_state.randomized_data = data.sample(frac=1).reset_index(drop=True)

            randomized_data = st.session_state.randomized_data[:nums]
            randomized_data = randomized_data[:nums]

            for index, row in randomized_data.iterrows():
                id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
                choice = display_listening_question(index, row, file_map)
                id_to_choice[int(row["問題ID"]) - 1] = choice

        cnt = 0
        for k, v in id_to_choice.items():
            if v not in options:
                cnt += 1
        if cnt == len(id_to_choice) and nums:
            if st.button("提出"):
                day, score, wrongs = calc_score(id_to_choice, id_to_answer)
                #st.write(day, score, wrongs)
                record_score(day, score, page, wrongs)
    else:
        reflection_flag = 1
        if RECORD_FILE_ID:
            data = load_csv_file(ID)
            data = pd.DataFrame(data)

        reflection_ids = select_definite_questions(page)

        for index, row in data.iterrows():
            if row["問題ID"] in reflection_ids:
                id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
                choice = display_listening_question(index, row, reflection_flag)
                id_to_choice[int(row["問題ID"]) - 1] = choice

        cnt = 0
        for k, v in id_to_choice.items():
            if v not in options:
                cnt += 1
        if cnt == len(id_to_choice) and reflection_ids:
            if st.button("提出"):
                day, score, wrongs = calc_score(id_to_choice, id_to_answer)