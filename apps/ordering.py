import streamlit as st
import pandas as pd
from collections import defaultdict
from eiken_common import load_csv_file, select_num_questions, select_question_kind, select_definite_questions, \
    calc_score, record_score, RECORD_FILE_ID

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

    choice = select_question_kind()[:1]
    reflection_flag = 0
    id_to_answer = defaultdict(int)
    id_to_choice = defaultdict(int)

    # ページが初めて読み込まれたときのみセッションをクリアする
    if "page_initialized" not in st.session_state or st.session_state.page_initialized != page:
        st.session_state.clear()
        st.session_state.page_initialized = page

    if choice == "A":
        nums = select_num_questions()
        if PROBLEM_FILE_ID:
            data = pd.DataFrame(load_csv_file(PROBLEM_FILE_ID))

            # 初回のみデータフレームの行をランダムにシャッフルして保存
            if "randomized_data" not in st.session_state:
                st.session_state.randomized_data = data.sample(frac=1).reset_index(drop=True)

            randomized_data = st.session_state.randomized_data[:nums]
            randomized_data = randomized_data[:nums]

            for index, row in randomized_data.iterrows():
                id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
                choice = display_ordering_question(index, row, reflection_flag)
                id_to_choice[int(row["問題ID"]) - 1] = choice

            ok = True
            for k, v in id_to_choice.items():
                if SYMBOL in v:
                    ok = False
            if ok and nums:
                if st.button("提出"):
                    day, score, wrongs = calc_score(id_to_choice, id_to_answer)
                    record_score(day, score, page, wrongs)

    else:
        reflection_flag = 1
        if RECORD_FILE_ID:
            data = load_csv_file(PROBLEM_FILE_ID)
            data = pd.DataFrame(data)

        reflection_ids = select_definite_questions(page, PROBLEM_FILE_ID)

        for index, row in data.iterrows():
            if row["問題ID"] in reflection_ids:
                id_to_answer[int(row["問題ID"]) - 1] = row["正解"]
                choice = display_ordering_question(index, row, reflection_flag)
                id_to_choice[int(row["問題ID"]) - 1] = choice
        ok = True
        for k, v in id_to_choice.items():
            if SYMBOL in v:
                ok = False
        if ok and reflection_ids:
            if st.button("提出"):
                calc_score(id_to_choice, id_to_answer)