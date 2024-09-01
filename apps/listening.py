import streamlit as st
import pandas as pd
import gspread

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io


from collections import defaultdict

import sys
import os
sys.path.append(os.path.dirname(__file__))

from eiken_common import load_csv_file, calc_score, record_score


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
service_account_info = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# リスニング
FOLDER_ID = "1g3QmKiqP3iCOa_GQcRwL-rZ3DCI3Mf-Z"
PROBLEM_FILE_ID = '1nHONtGQM2Msy9Wos8O0WaQ1oMnZkiflweqFIaaMOyMU'


def list_files_in_folder(folder_id=None):
    query = f"'{folder_id}' in parents" if folder_id else ""
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    return {item['name']: item['id'] for item in items}


def load_listening_files(row, file_map):
    t = "audio" + str(row["問題ID"]) + ".mp3"
    file_id = file_map[t]
    request = drive_service.files().get_media(fileId=file_id)
    file_data = io.BytesIO()
    downloader = MediaIoBaseDownload(file_data, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    file_data.seek(0)

    # ファイルをダウンロードして再生
    st.audio(file_data, format='audio/mpeg')

    # audio_file_path = "apps/audio/"
    # print(row["問題ID"])
    # t = "audio" + str(row["問題ID"]) + ".mp3"
    # audio_file_path += t
    #
    # try:
    #     # 音声ファイルを読み込む
    #     with open(audio_file_path, 'rb') as audio_file:
    #         audio_bytes = audio_file.read()
    #     # 音声ファイルを再生
    #     st.audio(audio_bytes, format="audio/mpeg")
    # except FileNotFoundError:
    #     st.error("音声ファイルが見つかりません。指定したパスを確認してください。")
    # except Exception as e:
    #     st.error(f"エラーが発生しました: {e}")


def display_question(question_index, row, file_map):
    st.write(f"**問題 {question_index + 1}**")
    load_listening_files(row, file_map)

    # 選択肢は固定された順序で表示
    choice = st.radio(
        "選択肢を選んでください:",
        [f"A: {row['選択肢A']}", f"B: {row['選択肢B']}", f"C: {row['選択肢C']}", f"D: {row['選択肢D']}"],
        key=f"question_{question_index}",
        horizontal=True
    )

    return choice[:1]


# 解く問題数を選択させる
def select_num_questions():
    num_questions = st.selectbox(
        "解く問題数を選んでください:",
        options=[" ", 1, 3, 5],
        index=0  # デフォルトで選択される値のインデックス（0=1問）
    )
    if num_questions == " ":
        num_questions = 0
    st.write(f"あなたが選んだ問題数: {num_questions}問")
    return num_questions


def app(page):

    st.title(f"英検{page}問題")

    # ルートフォルダ、または特定のフォルダのIDを指定してマッピングを作成
    folder_id = FOLDER_ID  # 特定のフォルダ内のファイルをリストする場合にフォルダIDを指定
    file_map = list_files_in_folder(folder_id)

    nums = select_num_questions()

    if PROBLEM_FILE_ID:
        data = load_csv_file(PROBLEM_FILE_ID)
        data = pd.DataFrame(data)

        # 初回のみデータフレームの行をランダムにシャッフルして保存
        if "randomized_data" not in st.session_state:
            st.session_state.randomized_data = data.sample(frac=1).reset_index(drop=True)

        randomized_data = st.session_state.randomized_data
        randomized_data = randomized_data[:nums]

        id_to_answer = defaultdict(int)
        id_to_choice = defaultdict(int)

        for index, row in randomized_data.iterrows():
            id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
            choice = display_question(index, row, file_map)
            id_to_choice[int(row["問題ID"]) - 1] = choice

    # if st.button("提出"):
    #     day, score = calc_score(id_to_choice, id_to_answer)
    #     record_score(day, score)