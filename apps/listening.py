import streamlit as st
import pandas as pd

from collections import defaultdict


# リスニング
problem_file_path = "apps/problem/problems_listening.csv"


# CSVファイルから英検問題を読み込む
def load_data(file_path):
    return pd.read_csv(file_path)


def load_listening_files(row):

    audio_file_path = "apps/audio/"
    print(row["問題ID"])
    t = "audio" + str(row["問題ID"]) + ".mp3"
    audio_file_path += t

    try:
        # 音声ファイルを読み込む
        with open(audio_file_path, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        # 音声ファイルを再生
        st.audio(audio_bytes, format="audio/mpeg")
    except FileNotFoundError:
        st.error("音声ファイルが見つかりません。指定したパスを確認してください。")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")


def display_question(question_index, row):
    st.write(f"**問題 {question_index + 1}**")
    load_listening_files(row)

    # 選択肢は固定された順序で表示
    choice = st.radio(
        "選択肢を選んでください:",
        [f"A: {row['選択肢A']}", f"B: {row['選択肢B']}", f"C: {row['選択肢C']}", f"D: {row['選択肢D']}"],
        key=f"question_{question_index}",
        horizontal=True
    )

    return choice[:1]


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

    # if st.button("提出"):
    #     day, score = calc_score(id_to_choice, id_to_answer)
    #     record_score(day, score)