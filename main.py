import streamlit as st
import pandas as pd
import random

from collections import defaultdict

file_path = "/Users/igusahiroyuki/PycharmProjects/pythonProject/eiken_quiz/problems1.csv"


# CSVファイルから英検問題を読み込む
def load_data(file_path):
    return pd.read_csv(file_path)


# 問題を表示する関数
def display_question(question_index, row):
    st.write(f"**問題 {question_index + 1}**")
    st.write(row['問題文'])

    # 選択肢は固定された順序で表示
    choice = st.radio(
        "選択肢を選んでください:",
        [f"A: {row['選択肢A']}", f"B: {row['選択肢B']}", f"C: {row['選択肢C']}", f"D: {row['選択肢D']}"],
        key=f"question_{question_index}",
        horizontal=True
    )

    return choice[:1]


def calc_score(choices, answers):
    score = 0
    for i in range(len(choices)):
        if choices[i] == answers[i]:
            score += 1
    st.write(score)

# メインアプリケーション
def main():
    st.title("英検問題集")

    if file_path:
        data = load_data(file_path)

        # 初回のみデータフレームの行をランダムにシャッフルして保存
        if "randomized_data" not in st.session_state:
            st.session_state.randomized_data = data.sample(frac=1).reset_index(drop=True)

        randomized_data = st.session_state.randomized_data

        id_to_answer = defaultdict(int)
        id_to_choice = defaultdict(int)

        for index, row in randomized_data.iterrows():
            id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
            choice = display_question(index, row)
            id_to_choice[int(row["問題ID"]) - 1] = choice
    if st.button("回答を確かめる"):
        calc_score(id_to_choice, id_to_answer)


if __name__ == "__main__":
    main()
