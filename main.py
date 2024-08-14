import streamlit as st
import pandas as pd

file_path = "/Users/igusahiroyuki/PycharmProjects/pythonProject/eiken_quiz/problems1.csv"

# CSVファイルから英検問題を読み込む
def load_data(file_path):
    return pd.read_csv(file_path)


# 問題を表示する関数
def display_question(question_index, row):
    #st.write(f"**問題 {row['問題ID']}**")
    st.write(f"**問題 {question_index + 1}**")
    st.write(row['問題文'])
    choice = st.radio(
        "選択肢を選んでください:",
        ['A:' + row["選択肢A"], 'B:' + row["選択肢B"], 'C:' + row["選択肢C"], 'D:' + row["選択肢D"]],  # 選択肢をリストにまとめる
        key=f"question_{question_index}",  # 一意のキーを指定
        horizontal=True  # 選択肢を横並びに表示
    )

    return choice


def calc_score(choice, answers):
    score = 0
    for i in range(len(answers)):
        #print(choice[i][:1], answers[i])
        if choice[i][:1] == answers[i]:
            score += 1
    st.write(score)


# メインアプリケーション
def main():
    st.title("英検問題集")

    #file_path = st.text_input("英検問題集ファイルのパスを入力してください:")

    if file_path:
        data = load_data(file_path)

        choices = []
        answers = []

        for index, row in data.iterrows():
            answers.append(row["正解"])
            choice = display_question(index, row)
            choices.append(choice)

    if st.button("回答を確かめる"):
        calc_score(choices, answers)


if __name__ == "__main__":
    main()
