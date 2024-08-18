import streamlit as st


# リスニング
audio_file_path = "apps/audio/audio1.mp3"

def app(page):
    st.title(f"英検{page}問題")
    print("HELLO")
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
