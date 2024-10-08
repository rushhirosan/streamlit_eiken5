import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(__file__))

from eiken_common import load_problem

PROBLEM_FILE_ID = "14PmuhBLAv54cUmYeQfo2BqwJHe8FQWUIaZAoJry78So"


def app(page):

    st.title(f"英検{page}問題")
    sentence = "内の `()` に当てはまる英語か、会話文の答えとして正しい選択肢を選択してください📝"
    st.markdown(f"{page}{sentence}")

    # ページが初めて読み込まれたときのみセッションをクリアする
    if "page_initialized" not in st.session_state or st.session_state.page_initialized != page:
        st.session_state.clear()
        st.session_state.page_initialized = page

    load_problem(PROBLEM_FILE_ID, page)