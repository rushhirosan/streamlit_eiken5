import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(__file__))

from eiken_common import load_problem

PROBLEM_FILE_ID = "1M2jANr3_9Zw8jeQfqXlhZFQaKso2lo9Yxcm4Pqdqha8"


def app(page):

    st.title(f"英検{page}問題")

    st.session_state.clear()

    load_problem(PROBLEM_FILE_ID, page)