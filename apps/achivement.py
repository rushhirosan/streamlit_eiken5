import streamlit as st
import pandas as pd
import gspread
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from eiken_common import load_csv_file, RECORD_FILE_ID, credentials


CATEGORY_TRANSLATION = {
    "単語/熟語": "Vocabulary",
    "文章": "Reading",
    "リスニング": "Listening",
    "並び替え": "Ordering"
}


def show_score_graph(data):
    """Scoreデータを基にカテゴリごとのスコアをグラフに表示する"""
    data['date'] = pd.to_datetime(data['date'])

    plt.figure(figsize=(10, 6))

    for category in data['category'].unique():
        filtered_data = data[data['category'] == category]
        plt.plot(filtered_data['date'], filtered_data['score'], marker='o',
                 label=CATEGORY_TRANSLATION.get(category, category))

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    # グラフの装飾
    plt.xlabel("Date")
    plt.ylabel("Score")
    plt.title("Score by Category over Time")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)


def delete_rows():
    # gspreadクライアントを作成
    client = gspread.authorize(credentials)

    # スプレッドシートID
    spreadsheet_id = RECORD_FILE_ID

    # スプレッドシートを開く
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.sheet1  # 最初のシートを取得

    # ヘッダーを残し、2行目以降を削除
    worksheet.delete_rows(2, worksheet.row_count)


def delete_confirm():
    """スコアの保存されたファイルを削除する"""
    confirm_delete = st.button("成果を削除してリスタートする")

    if confirm_delete:
        delete_rows()


def app(page):
    st.header(f"過去の{page}グラフ")
    st.write("今までの成果を確認してみよう👀")

    try:
        df = pd.DataFrame(load_csv_file(RECORD_FILE_ID))

        if not df.empty:
            show_score_graph(df)
            st.write("\n")
            st.write("過去のスコアテーブル")
            st.write("※日付、カテゴリ、スコア、間違った問題ID")
            df_transposed = df.transpose().astype(str)
            st.table(df_transposed)
        else:
            st.write("まだスコアが保存されていません。")
    except FileNotFoundError:
        st.write("まだスコアが保存されていません。")

    delete_confirm()