import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt

record_file_path = "apps/score/scores.csv"

def show_score_graph():
    data = pd.read_csv(record_file_path)

    # dateをdatetime形式に変換
    data['date'] = pd.to_datetime(data['date'])

    # グラフの描画
    plt.figure(figsize=(10, 6))
    plt.plot(data['date'], data['score'], marker='o')

    # グラフのタイトルとラベル
    plt.title('date and score')
    plt.xlabel('date')
    plt.ylabel('score')

    # dateのフォーマットを調整
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()  # dateラベルを傾ける

    # グラフを表示
    plt.grid(True)
    st.pyplot(plt)


def app(selection):
    # 保存されたscoreの一覧表示
    st.header("過去のscore")
    try:
        data = pd.read_csv(record_file_path)
        st.table(data)
    except FileNotFoundError:
        st.write("まだscoreが保存されていません。")

    if st.button("グラフを見る"):
        show_score_graph()