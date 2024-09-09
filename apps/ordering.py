import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(__file__))

from collections import defaultdict
from eiken_common import load_csv_file, select_num_questions, \
    select_question_kind, select_definite_questions, RECORD_FILE_ID, submit_answer

# 定数
SYMBOL = "_"
PROBLEM_FILE_ID = "1sX8d-D4IzwzK_EwrBeyRWK--JiBV0oapFm8xzE3wWQY"


def display_ordering_question(question_index, row, reflection_flag):
    """問題と選択肢を表示し、選択された回答を返す"""
    if not reflection_flag:
        st.write(f"**問題 {question_index + 1}**")
    else:
        st.write(f"**問題ID: {question_index + 1}**")
    st.write(row['問題文'])

    # 4つのカラムを作成
    col1, col2, col3, col4 = st.columns(4)

    # 各カラムに対応する選択肢を表示
    with col1:
        option1 = st.selectbox("-", [SYMBOL, row["選択肢A"], row["選択肢B"], row["選択肢C"], row["選択肢D"]],
                               key=f'{question_index}_col1', label_visibility='hidden')

    with col2:
        option2 = st.selectbox("-", [SYMBOL, row["選択肢A"], row["選択肢B"], row["選択肢C"], row["選択肢D"]],
                               key=f'{question_index}_col2', label_visibility='hidden')

    with col3:
        option3 = st.selectbox("-", [SYMBOL, row["選択肢A"], row["選択肢B"], row["選択肢C"], row["選択肢D"]],
                               key=f'{question_index}_col3', label_visibility='hidden')

    with col4:
        option4 = st.selectbox("-", [SYMBOL, row["選択肢A"], row["選択肢B"], row["選択肢C"], row["選択肢D"]],
                               key=f'{question_index}_col4', label_visibility='hidden')

    if SYMBOL in [option1, option2, option3, option4]:
        st.warning("選択肢を選んでください。")

    # 結果を返却
    res = option1 + " " + option2 + " " + option3 + " " + option4 + "."
    st.write(res)
    return res


def app(page):
    st.title(f"英検{page}問題")
    st.write("選択肢から解答を選択してください📝")

    # セッションの初期化
    if "page_initialized" not in st.session_state or st.session_state.page_initialized != page:
        st.session_state.clear()
        st.session_state.page_initialized = page

    choice = select_question_kind()[:1]
    reflection_flag = choice != "A"

    # 共通処理: データのロードと初期化
    data = pd.DataFrame(load_csv_file(PROBLEM_FILE_ID))
    if reflection_flag:
        reflection_ids = select_definite_questions(page, PROBLEM_FILE_ID)
        data = data[data["問題ID"].isin(reflection_ids)]

    if "randomized_data" not in st.session_state and not reflection_flag:
        st.session_state.randomized_data = data.sample(frac=1).reset_index(drop=True)

    questions = st.session_state.randomized_data[:select_num_questions()] if not reflection_flag else data

    id_to_answer = defaultdict(int)
    id_to_choice = defaultdict(int)

    # 問題を処理して解答を収集する
    for index, row in questions.iterrows():
        id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
        choice = display_ordering_question(index, row, reflection_flag)
        id_to_choice[int(row["問題ID"]) - 1] = choice

    # 全ての解答が選択されているか確認する
    all_answers_provided = all(SYMBOL not in v for v in id_to_choice.values())

    # 解答の送信
    if all_answers_provided and len(id_to_choice) > 0:
        submit_answer(id_to_choice, id_to_answer, page)

