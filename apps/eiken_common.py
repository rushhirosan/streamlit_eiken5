import streamlit as st
import gspread
import pandas as pd
import numpy as np

from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from collections import defaultdict

# Google Drive API の設定
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive'
     ]
service_account_info = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

RECORD_FILE_ID = "1sVwChcnOnkh6Ypllndc-jV42xqGoaGAu0uKLdHkKEBg"


def load_csv_file(ID):

    # gspreadクライアントを作成
    client = gspread.authorize(credentials)

    # スプレッドシートの取得
    spreadsheet_id = ID
    spreadsheet = client.open_by_key(spreadsheet_id)

    # ワークシートの取得
    worksheet = spreadsheet.sheet1  # 最初のワークシートを取得
    data = worksheet.get_all_records()  # データを取得
    return data


def record_score(date, score, category, wrongs_input):

    # 入力文字列をリストに変換
    wrongs = wrongs_input.split()  # スペースで分割してリストにする
    wrongs = list(map(str, wrongs))  # リストの要素を文字列に変換

    # gspreadクライアントを作成
    client = gspread.authorize(credentials)

    spreadsheet_id = RECORD_FILE_ID
    spreadsheet = client.open_by_key(spreadsheet_id)

    # ワークシートの取得
    worksheet = spreadsheet.sheet1  # 最初のワークシートを取得

    try:
        # CSVファイルを読み込む
        data = load_csv_file(RECORD_FILE_ID)
        df = pd.DataFrame(data)
    except FileNotFoundError:
        # CSVファイルが存在しない場合、新しいDataFrameを作成
        df = pd.DataFrame(columns=["date", "category", "score", "wrongs"])

    # 新しいデータを追加
    new_entry = pd.DataFrame({
        "date": [date],
        "category": [category],
        "score": [score],
        "wrongs": [', '.join(wrongs)]  # `wrongs` 列をカンマ区切りの文字列に変換
    })
    df = pd.concat([df, new_entry], ignore_index=True)

    # DataFrameの最後の行をリストに変換してGoogle Sheetsに追加
    row_to_append = new_entry.iloc[0].tolist()

    # すべての要素をPythonの標準的な型に変換
    row_to_append = [int(item) if isinstance(item, np.int64) else item for item in row_to_append]

    worksheet.append_row(row_to_append)


# scoreを計算する関数
def calc_score(choices, answers):
    count = 0
    len_choices = len(choices)
    wrong_questions = []
    for k, v in choices.items():
        if choices[k] == answers[k]:
            count += 1
        else:
            wrong_questions.append(k + 1)
    score = int(100 * (count / len_choices))

    today = datetime.today().strftime("%Y-%m-%d")
    st.write(today + "のスコアは...")
    st.write(str(score) + "点")
    wrongs = ""
    if len(wrong_questions) >= 1:
        st.write("間違えた問題IDは...")
        wrongs = " ".join(f"{i}" for i in sorted(wrong_questions))
        st.text(wrongs)
    if count >= len_choices:
        st.write("🈴満点おめでとう！！💯")
        st.balloons()
    elif 70 <= score <= 90:
        st.write("🉑まあまあの出来だね、次は満点目指して頑張ろう！間違えた問題はパパかママに聞いてね。")
    elif 30 <= score < 70:
        st.write("💦もっと頑張れ！復習して、間違えた問題は👨か👩に聞いてね。")
    else:
        st.write("😱へばへぼー😱")
    return today, score, wrongs


# 問題を表示する関数
def display_question(question_index, row, reflection_flag):
    if not reflection_flag:
        st.write(f"**問題 {question_index + 1}**")
    else:
        st.write(f"**問題ID: {question_index + 1}**")
    st.write(row['問題文'])

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


def clear_selectbox_state():
    # ページ切り替え時にselectboxの値をリセット
    st.session_state['num_questions'] = " "  # 空の状態にリセット

# 解く問題数を選択させる
def select_num_questions():

    if 'num_questions' not in st.session_state:
        st.session_state['num_questions'] = " "

    num_questions = st.selectbox(
        "解く問題数を選んでください:（0から100の内、100の約数のみ選択できます）",
        options=[" "] + [x for x in range(1, 101) if 100 % x == 0],
        index=0,  # デフォルトで選択される値のインデックス（0=1問）
        key="num_questions"
    )
    if num_questions == " ":
        num_questions = 0
    st.write(f"あなたが選んだ問題数: {num_questions}問")
    return num_questions


def select_question_kind():
    kind_choice = st.radio(
        "ランダムに問題を解くか特定の問題IDを指定して復習するか選択してください",
        ["A: ランダム", "B: 復習"],
        horizontal=True
    )
    return kind_choice


def parse_wrongs(wrongs_str):
    # もしwrongs_strが空なら空のリストを返す
    if not wrongs_str:
        return ""

    # wrongs_strが数値の場合は、リストに変換して返す
    if isinstance(wrongs_str, (int, float)):
        return [int(wrongs_str)]

    # 文字列をカンマで分割し、リストに変換
    return [int(x.strip()) for x in wrongs_str.split(',') if x.strip().isdigit()]


def select_definite_questions(page, ID):

    st.write(f"間違えた{page}問題")

    df = load_csv_file(RECORD_FILE_ID)
    df = pd.DataFrame(df)
    df2 = load_csv_file(ID)
    df2 = pd.DataFrame(df2)
    wrong_ids = set()

    cnt_wrong_rows = 0
    for index, row in df.iterrows():
        category = row['category']
        wrongs_str = row['wrongs']
        if category != page:
            continue
        if len(str(wrongs_str)) == 1:
            wrong_ids.add(wrongs_str)
            cnt_wrong_rows += 1
        else:
            x = parse_wrongs(wrongs_str)
            for v in x:
                wrong_ids.add(v)
                cnt_wrong_rows += 1


    xs = sorted(list(wrong_ids))
    st.write(f"{', '.join(map(str, xs))}")

    # ユーザーが複数の問題IDを選択できるようにする
    selected_ids = st.multiselect(
        "選択する問題IDを選んでください:",
        #filtered_ids
        [x for x in range(1, len(df2) + 1)]
    )

    st.write(f"選択された問題ID: {selected_ids}")

    return set(selected_ids)


def load_problem(ID, page):

    choice = select_question_kind()[:1]
    reflection_flag = 0
    id_to_answer = defaultdict(int)
    id_to_choice = defaultdict(int)
    options = ["A", "B", "C", "D"]

    if choice == "A":
        nums = select_num_questions()
        if ID:
            data = load_csv_file(ID)
            data = pd.DataFrame(data)

            # 初回のみデータフレームの行をランダムにシャッフルして保存
            if "randomized_data" not in st.session_state:

                st.session_state.randomized_data = data.sample(frac=1).reset_index(drop=True)

            randomized_data = st.session_state.randomized_data
            randomized_data = randomized_data[:nums]

            for index, row in randomized_data.iterrows():
                id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
                choice = display_question(index, row, reflection_flag)
                id_to_choice[int(row["問題ID"]) - 1] = choice

        cnt = 0
        for k, v in id_to_choice.items():
            if v in options:
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

        reflection_ids = select_definite_questions(page, ID)

        for index, row in data.iterrows():
            if row["問題ID"] in reflection_ids:
                id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
                choice = display_question(index, row, reflection_flag)
                id_to_choice[int(row["問題ID"]) - 1] = choice

        cnt = 0
        for k, v in id_to_choice.items():
            if v in options:
                cnt += 1
        if cnt == len(id_to_choice) and reflection_ids:
            if st.button("提出"):
                calc_score(id_to_choice, id_to_answer)