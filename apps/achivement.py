import streamlit as st
import pandas as pd
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import sys
import os
sys.path.append(os.path.dirname(__file__))

from eiken_common import load_csv_file


#record_file_path = "apps/score/scores.csv"
RECORD_FILE_ID = "1sVwChcnOnkh6Ypllndc-jV42xqGoaGAu0uKLdHkKEBg"


def show_score_graph(data):

    # dateをdatetime形式に変換
    data['date'] = pd.to_datetime(data['date'])

    t = {
        "単語/熟語": "Vocabulary",
        "文章": "Reading",
        "リスニング": "Listening"
    }

    # カテゴリごとにデータをフィルタリングしてグラフを描画
    categories = data['category'].unique()

    plt.figure(figsize=(10, 6))

    for category in categories:
        filtered_data = data[data['category'] == category]
        plt.plot(filtered_data['date'], filtered_data['score'], marker='o', label=t[category])

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

def delete_score():

    # 削除確認ボタン
    confirm_delete = st.button("成果を削除してリスタートする")

    # 削除確認後の操作
    if confirm_delete:
        st.warning(f"本当に成果を削除しますか？この操作は元に戻せません。")
        delete_now = st.button("はい、削除します")

        if delete_now:
            if os.path.exists(record_file_path):
                os.remove(record_file_path)
                st.success(f"ファイル '{record_file_path}' を削除しました。")
            else:
                st.error(f"ファイル '{record_file_path}' が見つかりません。")


def app(selection):
    # 保存されたscoreの一覧表示
    st.header("過去のscoreグラフ")
    try:
        data = load_csv_file(RECORD_FILE_ID)
        data = pd.DataFrame(data)
    except FileNotFoundError:
        st.write("まだscoreが保存されていません。")

    show_score_graph(data)
    st.write("\n")
    st.write("過去のscoreテーブル")
    data_transposed = data.transpose()
    # Streamlitで表示
    st.table(data_transposed)
    #delete_score()
