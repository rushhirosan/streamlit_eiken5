import streamlit as st
import pandas as pd
from datetime import datetime

from collections import defaultdict


problem_file_path = "apps/problem/problems1.csv"
record_file_path = "apps/score/scores.csv"


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


# scoreを計算する関数
def calc_score(choices, answers):
    score = 0
    len_choices = len(choices)
    for k, v in choices.items():
        if choices[k] == answers[k]:
            score += 1
    #today = datetime.today().strftime("%Y年%m月%d日")
    today = datetime.today().strftime("%Y-%m-%d")
    st.write(today + "のscoreは...")
    st.write(score)
    ratio = score / len_choices
    if score >= len_choices:
        st.write("すごい")
    elif 0.7 <= ratio <= 0.9:
        st.write("まあまあ")
    elif 0.3 <= ratio < 0.7:
        st.write("頑張れ")
    else:
        st.write("へぼー")
    return today, score


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


# 記録する
def record_score(date, score):

    try:
        df = pd.read_csv(record_file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["date", "score"])

    # 新しいデータを追加
    new_entry = pd.DataFrame({"date": [date], "score": [score]})
    df = pd.concat([df, new_entry], ignore_index=True)

    # CSVに保存
    df.to_csv(record_file_path, index=False)


def app(page):


    st.title(f"英検{page}問題")

    nums = select_num_questions()

    if problem_file_path:
        data = load_data(problem_file_path)

        # 初回のみデータフレームの行をランダムにシャッフルして保存
        if "randomized_data" not in st.session_state:
            st.session_state.randomized_data = data.sample(frac=1).reset_index(drop=True)

        randomized_data = st.session_state.randomized_data
        randomized_data = randomized_data[:nums]

        id_to_answer = defaultdict(int)
        id_to_choice = defaultdict(int)

        for index, row in randomized_data.iterrows():
            id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
            choice = display_question(index, row)
            id_to_choice[int(row["問題ID"]) - 1] = choice
    if st.button("提出"):
        day, score = calc_score(id_to_choice, id_to_answer)
        record_score(day, score)