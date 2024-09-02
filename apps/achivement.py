import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from eiken_common import load_csv_file

# 定数
RECORD_FILE_ID = "1sVwChcnOnkh6Ypllndc-jV42xqGoaGAu0uKLdHkKEBg"

CATEGORY_TRANSLATION = {
    "単語/熟語": "Vocabulary",
    "文章": "Reading",
    "リスニング": "Listening"
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


def delete_score(record_file_path):
    """スコアの保存されたファイルを削除する"""
    confirm_delete = st.button("成果を削除してリスタートする")

    if confirm_delete:
        st.warning("本当に成果を削除しますか？この操作は元に戻せません。")
        if st.button("はい、削除します"):
            if os.path.exists(record_file_path):
                os.remove(record_file_path)
                st.success(f"ファイル '{record_file_path}' を削除しました。")
            else:
                st.error(f"ファイル '{record_file_path}' が見つかりません。")


def app(page):
    st.header("過去のスコアグラフ")

    try:
        data = pd.DataFrame(load_csv_file(RECORD_FILE_ID))
        if not data.empty:
            show_score_graph(data)
            st.write("\n")
            st.write("過去のスコアテーブル")
            st.table(data.transpose())
        else:
            st.write("まだスコアが保存されていません。")
    except FileNotFoundError:
        st.write("まだスコアが保存されていません。")