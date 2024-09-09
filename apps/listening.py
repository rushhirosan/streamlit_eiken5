import streamlit as st
import pandas as pd
from googleapiclient.http import MediaIoBaseDownload
import io
import sys
import os
sys.path.append(os.path.dirname(__file__))

from collections import defaultdict
from eiken_common import load_csv_file, select_num_questions, select_question_kind, \
    select_definite_questions, drive_service, RECORD_FILE_ID, submit_answer

# 定数
FOLDER_ID = "1g3QmKiqP3iCOa_GQcRwL-rZ3DCI3Mf-Z"
PROBLEM_FILE_ID = '1nHONtGQM2Msy9Wos8O0WaQ1oMnZkiflweqFIaaMOyMU'


def list_files_in_folder(folder_id=None):
    """フォルダ内のファイルをリストし、ファイル名とIDを返す"""
    query = f"'{folder_id}' in parents" if folder_id else ""
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return {item['name']: item['id'] for item in results.get('files', [])}


@st.cache_data
def download_listening_file(file_id):
    """Google Drive から音声ファイルをダウンロードする"""
    request = drive_service.files().get_media(fileId=file_id)
    file_data = io.BytesIO()
    downloader = MediaIoBaseDownload(file_data, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    file_data.seek(0)
    return file_data


def load_listening_file(file_id):
    """キャッシュから音声ファイルを取得して再生する"""
    file_data = download_listening_file(file_id)
    st.audio(file_data, format='audio/mpeg')


def display_listening_question(question_index, row, file_map, reflection_flag):
    """問題と選択肢を表示し、選択された回答を返す"""
    if not reflection_flag:
        st.write(f"**問題 {question_index + 1}**")
    else:
        st.write(f"**問題ID: {question_index + 1}**")
    st.write(row['問題文'])

    # 音声ファイルのロードと再生
    file_id = file_map[f"audio{row['問題ID']}.mp3"]
    load_listening_file(file_id)

    # 選択肢は固定された順序で表示
    choice = st.radio(
        label="選択肢を選んでください:",
        options=[
            "選んでください",
            f"A: {row['選択肢A']}",
            f"B: {row['選択肢B']}",
            f"C: {row['選択肢C']}",
            f"D: {row['選択肢D']}"
        ],
        key=f"question_{question_index}",
        horizontal=True
    )

    if choice == "選んでください":
        st.warning("選択肢を選んでください。")

    return choice[:1]


# def load_listening_file(file_id):
#     """Google Drive から音声ファイルをダウンロードし、再生する"""
#     request = drive_service.files().get_media(fileId=file_id)
#     file_data = io.BytesIO()
#     downloader = MediaIoBaseDownload(file_data, request)
#     done = False
#     while not done:
#         status, done = downloader.next_chunk()
#     file_data.seek(0)
#     st.audio(file_data, format='audio/mpeg')
#
#
# def display_listening_question(question_index, row, file_map, reflection_flag):
#     """問題と選択肢を表示し、選択された回答を返す"""
#     if not reflection_flag:
#         st.write(f"**問題 {question_index + 1}**")
#     else:
#         st.write(f"**問題ID: {question_index + 1}**")
#     st.write(row['問題文'])
#     load_listening_file(file_map[f"audio{row['問題ID']}.mp3"])
#
#     choice = st.radio(
#         "選択肢を選んでください:",
#         [f"A: {row['選択肢A']}", f"B: {row['選択肢B']}", f"C: {row['選択肢C']}", f"D: {row['選択肢D']}"],
#         key=f"question_{question_index}",
#         horizontal=True
#     )
#     return choice[:1]  # 選択肢の頭文字 (A, B, C, D) を返す

def count_valid_choices(id_to_choice, options):
    """Count the number of valid choices provided by the user."""
    return sum(1 for v in id_to_choice.values() if v in options)


def initialize_session(page):
    """Initialize session state if it's the first time the page is loaded."""
    if "page_initialized" not in st.session_state or st.session_state.page_initialized != page:
        st.session_state.clear()
        st.session_state.page_initialized = page


def app(page):
    st.title(f"英検{page}問題")
    st.write("▶ボタンを押して英語を聞いてから、選択肢から解答を選択してください📝")
    st.write("※ボタンが現れるまで少し時間がかかる場合があります。")

    choice = select_question_kind()[:1]
    reflection_flag = 0
    id_to_answer = defaultdict(int)
    id_to_choice = defaultdict(int)

    options = ["A", "B", "C", "D"]

    initialize_session(page)

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
                choice = display_listening_question(index, row, file_map, reflection_flag)
                id_to_choice[int(row["問題ID"]) - 1] = choice

        if count_valid_choices(id_to_choice, options) == len(id_to_choice) and nums:
            submit_answer(id_to_choice, id_to_answer, page)
    else:
        reflection_flag = 1
        if RECORD_FILE_ID:
            data = load_csv_file(PROBLEM_FILE_ID)
            data = pd.DataFrame(data)

        reflection_ids = select_definite_questions(page, PROBLEM_FILE_ID)

        for index, row in data.iterrows():
            if row["問題ID"] in reflection_ids:
                id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
                choice = display_listening_question(index, row, file_map, reflection_flag)
                id_to_choice[int(row["問題ID"]) - 1] = choice

        if count_valid_choices(id_to_choice, options) == len(id_to_choice) and reflection_ids:
            submit_answer(id_to_choice, id_to_answer, page)
