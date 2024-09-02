import streamlit as st
from eiken_common import load_problem

PROBLEM_FILE_ID = "1sX8d-D4IzwzK_EwrBeyRWK--JiBV0oapFm8xzE3wWQY"


def app(page):

    # 4つのカラムを作成
    col1, col2, col3, col4 = st.columns(4)

    # 各カラムに対応する選択肢を表示
    with col1:
        option1 = st.selectbox("", ["", "drink", "a", "of", "cup", "coffee", "in", "this", "morning"], key='col1')

    with col2:
        option2 = st.selectbox("", ["", "drink", "a", "of", "cup", "coffee", "in", "this", "morning"], key='col2')

    with col3:
        option3 = st.selectbox("", ["", "drink", "a", "of", "cup", "coffee", "in", "this", "morning"], key='col3')

    with col4:
        option4 = st.selectbox("", ["", "drink", "a", "of", "cup", "coffee", "in", "this", "morning"], key='col4')

    # 結果を表示
    st.write(f"I {option1} {option2} {option3} {option4} drink a cup of coffee in this morning")
