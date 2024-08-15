import streamlit as st
import pandas as pd

from collections import defaultdict


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

# スコアを計算する関数
def calc_score(choices, answers):
    score = 0
    for i in range(len(choices)):
        if choices[i] == answers[i]:
            score += 1
    st.write(score)


def page_listening():
    pass


def page_vocabulary():
    pass

def page_achievement():
    pass


def page_reading(page):

    file_path = "/Users/igusahiroyuki/PycharmProjects/pythonProject/eiken_quiz/problems1.csv"

    st.title(f"英検{page}問題")

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
    page = st.sidebar.radio("問題/成果を選択してください", ["単語", "文章", "リスニング", "成果"])
    if page == "単語":
        page_vocabulary()
    elif page == "文章":
        page_reading(page)
    elif page == "リスニング":
        page_listening()
    else:
        page_achievement()
