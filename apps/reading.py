import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(__file__))

from eiken_common import load_csv_file, calc_score, record_score
from collections import defaultdict




# PROBLEM_FILE_ID = "apps/problem/problems_reading.csv"
RECORD_FILE_ID = "apps/score/scores.csv"
PROBLEM_FILE_ID = "14PmuhBLAv54cUmYeQfo2BqwJHe8FQWUIaZAoJry78So"


# CSVファイルから英検問題を読み込む
def load_data(file_path):
    return pd.read_csv(file_path)


# 問題を表示する関数
def display_question(question_index, row, reflection_flag):
    if not reflection_flag:
        st.write(f"**問題 {question_index + 1}**")
    else:
        st.write(f"**問題ID: {question_index + 1}**")
    st.write(row['問題文'])

    # 選択肢は固定された順序で表示
    choice = st.radio(
        label="選択肢を選んでください:",
        options=[
            "選んでください",
            f"A: {row['選択肢A']}",
            f"B: {row['選択肢B']}",
            f"C: {row['選択肢C']}",
            f"D: {row['選択肢D']}"
        ],
        key=f"question_{question_index}",
        horizontal=True
    )

    if choice == "選んでください":
        st.warning("選択肢を選んでください。")

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


def select_question_kind():
    kind_choice = st.radio(
        "特定の問題IDを指定して復習するかランダム問題を解くか選択してください",
        ["A: ランダム", "B: 復習"],
        horizontal=True
    )
    return kind_choice


def parse_wrongs(wrongs_str):
    # 文字列をカンマで分割し、リストに変換
    return [int(x.strip()) for x in wrongs_str.split(',') if x.strip().isdigit()]


def select_definite_questions(page):

    st.write(f"間違えた{page}問題")

    df = pd.read_csv(RECORD_FILE_ID)
    wrong_ids = set()

    cnt_rows = 0
    for index, row in df.iterrows():
        category = row['category']
        wrongs_str = row['wrongs']
        if category != page:
            continue
        if len(wrongs_str) == 1:
            print("HI", wrongs_str)
            wrong_ids.add(int(wrongs_str))
            cnt_rows += 1
        else:
            x = parse_wrongs(wrongs_str)
            for v in x:
                wrong_ids.add(v)
                cnt_rows += 1

    xs = sorted(list(wrong_ids))

    st.write(f"{', '.join(map(str, xs))}")

    # 検索バーを追加
    # search_term = st.text_input("検索:", "")
    #
    # # 検索フィルタリング
    # filtered_ids = [pid for pid in problem_ids if search_term.lower() in pid.lower()]

    # ユーザーが複数の問題IDを選択できるようにする
    selected_ids = st.multiselect(
        "選択する問題IDを選んでください:",
        #filtered_ids
        [x for x in range(1, cnt_rows + 1)]
    )

    st.write(f"選択された問題ID: {selected_ids}")

    return set(selected_ids)


def app(page):

    st.title(f"英検{page}問題")

    choice = select_question_kind()[:1]
    reflection_flag = 0
    if choice == "A":
        nums = select_num_questions()
        if PROBLEM_FILE_ID:
            data = load_csv_file(PROBLEM_FILE_ID)
            #data = load_data(PROBLEM_FILE_ID)
            data = pd.DataFrame(data)

            # 初回のみデータフレームの行をランダムにシャッフルして保存
            if "randomized_data" not in st.session_state:
                st.session_state.randomized_data = data.sample(frac=1).reset_index(drop=True)

            randomized_data = st.session_state.randomized_data
            randomized_data = randomized_data[:nums]

            print(randomized_data)

            id_to_answer = defaultdict(int)
            id_to_choice = defaultdict(int)

            for index, row in randomized_data.iterrows():
                id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
                choice = display_question(index, row, reflection_flag)
                id_to_choice[int(row["問題ID"]) - 1] = choice

        cnt = 0
        for k, v in id_to_choice.items():
            if v != "選":
                cnt += 1
        if cnt == len(id_to_choice) and nums:
            if st.button("提出"):
                pass
                #day, score, wrongs = calc_score(id_to_choice, id_to_answer)
                #record_score(day, score, page, wrongs)
    else:
        reflection_flag = 1
        if PROBLEM_FILE_ID:
            data = load_data(PROBLEM_FILE_ID)

        reflection_ids = select_definite_questions(page)

        id_to_answer = defaultdict(int)
        id_to_choice = defaultdict(int)

        for index, row in data.iterrows():
            if row["問題ID"] in reflection_ids:
                id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
                choice = display_question(index, row, reflection_flag)
                id_to_choice[int(row["問題ID"]) - 1] = choice

        cnt = 0
        for k, v in id_to_choice.items():
            if v != "選":
                cnt += 1
        if cnt == len(id_to_choice) and reflection_ids:
            if st.button("提出"):
                pass
                #day, score, wrongs = calc_score(id_to_choice, id_to_answer)