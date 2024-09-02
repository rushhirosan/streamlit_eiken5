import streamlit as st
from eiken_common import load_problem

PROBLEM_FILE_ID = "1M2jANr3_9Zw8jeQfqXlhZFQaKso2lo9Yxcm4Pqdqha8"


def app(page):

    st.title(f"英検{page}問題")
    st.write(f"{page}に該当する日本語を選択してください")

    # ページが初めて読み込まれたときのみセッションをクリアする
    if "page_initialized" not in st.session_state or st.session_state.page_initialized != page:
        st.session_state.clear()
        st.session_state.page_initialized = page

    load_problem(PROBLEM_FILE_ID, page)
