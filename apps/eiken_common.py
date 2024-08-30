import streamlit as st
import gspread
import pandas as pd

from datetime import datetime
from google.oauth2.service_account import Credentials

PROBLEM_FILE_ID = "14PmuhBLAv54cUmYeQfo2BqwJHe8FQWUIaZAoJry78So"
RECORD_FILE_ID = ""


def load_csv_file(ID):
    print("TEST")

    # スコープを指定
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    st.write(st.secrets)

    # サービスアカウントのJSONファイルを使用して認証情報を作成
    service_account_info = st.secrets["gcp_service_account"]

    # 認証情報を作成
    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)

    # gspreadクライアントを作成
    client = gspread.authorize(creds)

    # スプレッドシートの取得
    spreadsheet_id = ID
    spreadsheet = client.open_by_key(spreadsheet_id)

    # ワークシートの取得
    worksheet = spreadsheet.sheet1  # 最初のワークシートを取得
    data = worksheet.get_all_records()  # データを取得
    #st.write(data)
    return data


def record_score(date, score, category, wrongs_input):
    # `wrongs_input` は文字列として受け取ります。例: "2 3 5"

    # 入力文字列をリストに変換
    wrongs = wrongs_input.split()  # スペースで分割してリストにする
    wrongs = list(map(str, wrongs))  # リストの要素を文字列に変換

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # サービスアカウントのJSONファイルを使用して認証情報を作成
    service_account_info = st.secrets["gcp_service_account"]

    # 認証情報を作成
    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)

    # gspreadクライアントを作成
    client = gspread.authorize(creds)

    spreadsheet_id = '1sVwChcnOnkh6Ypllndc-jV42xqGoaGAu0uKLdHkKEBg'
    spreadsheet = client.open_by_key(spreadsheet_id)

    # ワークシートの取得
    worksheet = spreadsheet.sheet1  # 最初のワークシートを取得

    try:
        # CSVファイルを読み込む
        data = load_csv_file(RECORD_FILE_ID)
        df = pd.read_csv(data)
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

    # CSVに保存
    #df.to_csv(RECORD_FILE_ID, index=False)
    worksheet.append_row(df)


# scoreを計算する関数
def calc_score(choices, answers):
    score = 0
    len_choices = len(choices)
    wrong_questions = []
    for k, v in choices.items():
        if choices[k] == answers[k]:
            score += 1
        else:
            wrong_questions.append(k + 1)

    #today = datetime.today().strftime("%Y年%m月%d日")
    today = datetime.today().strftime("%Y-%m-%d")
    st.write(today + "のscoreは...")
    st.write(score)
    st.write("間違えた問題IDは")
    wrongs = " ".join(f"{i}" for i in sorted(wrong_questions))
    st.text(wrongs)
    ratio = score / len_choices
    if score >= len_choices:
        st.write("すごい")
    elif 0.7 <= ratio <= 0.9:
        st.write("まあまあ")
    elif 0.3 <= ratio < 0.7:
        st.write("頑張れ")
    else:
        st.write("へぼー")
    return today, score, wrongs