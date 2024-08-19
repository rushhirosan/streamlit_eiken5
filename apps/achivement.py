import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

record_file_path = "apps/score/scores.csv"

def show_score_graph(data):

    # dateをdatetime形式に変換
    data['date'] = pd.to_datetime(data['date'])

    # カテゴリごとにデータをフィルタリングしてグラフを描画
    categories = data['category'].unique()

    plt.figure(figsize=(10, 6))

    for category in categories:
        filtered_data = data[data['category'] == category]
        plt.plot(filtered_data['date'], filtered_data['score'], marker='o', label=category)

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


def app(selection):
    # 保存されたscoreの一覧表示
    st.header("過去のscore")
    try:
        data = pd.read_csv(record_file_path)
    except FileNotFoundError:
        st.write("まだscoreが保存されていません。")

    # TODO: selectbox, default graph
    if st.button("グラフを見る"):
        show_score_graph(data)
    st.write("\n")
    if st.button("間違えた問題を見る"):
        pass
    st.write("\n")
    if st.button("表を見る"):
        st.table(data)