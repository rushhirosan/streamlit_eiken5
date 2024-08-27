import streamlit as st
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build


def exp():

    # 環境変数から認証情報を取得
    key_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    print(f"Key file path: {key_file}")  # これでパスが正しく取得されているか確認
    # credentials = service_account.Credentials.from_service_account_file(key_file)
    #
    # # 使用するAPIのサービス名とバージョンを指定
    # service = build('sheets', 'v4', credentials=credentials)


def app(page):
    st.title(f"英検{page}問題")
    exp()