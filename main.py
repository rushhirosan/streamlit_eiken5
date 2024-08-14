import streamlit as st
import pandas as pd
import random

file_path = "/Users/igusahiroyuki/PycharmProjects/pythonProject/eiken_quiz/problems1.csv"


# CSVファイルから英検問題を読み込む
def load_data(file_path):
    return pd.read_csv(file_path)


# 問題を表示する関数
def display_question(question_index, row):
    st.write(f"**問題 {question_index + 1}**")
    st.write(row['問題文'])

    # 初回のみ選択肢のテキストをランダムに並び替える
    if f"randomized_choices_{question_index}" not in st.session_state:
        original_choices = ['A', 'B', 'C', 'D']
        choices_text = [row["選択肢A"], row["選択肢B"], row["選択肢C"], row["選択肢D"]]
        randomized_text = random.sample(choices_text, len(choices_text))  # テキストをランダム化
        st.session_state[f"randomized_choices_{question_index}"] = randomized_text
    else:
        randomized_text = st.session_state[f"randomized_choices_{question_index}"]

    # 元のラベル順序でランダム化された選択肢テキストを表示
    choice = st.radio(
        "選択肢を選んでください:",
        [f"{label}: {text}" for label, text in zip(['A', 'B', 'C', 'D'], randomized_text)],
        key=f"question_{question_index}",
        horizontal=True
    )

    return choice, randomized_text


def calc_score(choices, answers):
    score = 0
    for i, (selected_choice, randomized_text) in enumerate(choices):
        selected_label = selected_choice[:1]  # ユーザーが選んだ選択肢のラベル
        correct_answer = answers[i]  # 正解のラベル
        correct_text = randomized_text[original_choices.index(correct_answer)]  # 正しいテキスト
        correct_label = original_choices[randomized_text.index(correct_text)]  # テキストに対応する正しいラベル

        if selected_label == correct_label:
            score += 1
    st.write(f"スコア: {score}")


# メインアプリケーション
def main():
    st.title("英検問題集")

    if file_path:
        data = load_data(file_path)

        # 初回のみデータフレームの行をランダムにシャッフルして保存
        if "randomized_data" not in st.session_state:
            st.session_state.randomized_data = data.sample(frac=1).reset_index(drop=True)

        randomized_data = st.session_state.randomized_data

        choices = []
        answers = []

        for index, row in randomized_data.iterrows():
            answers.append(row["正解"])
            choice, randomized_text = display_question(index, row)
            choices.append((choice, randomized_text))

    if st.button("回答を確かめる"):
        calc_score(choices, answers)


if __name__ == "__main__":
    main()
