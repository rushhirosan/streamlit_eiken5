from apps import reading
from apps import vocabulary
from apps import listening
from apps import achivement
import streamlit as st

# Static pages
PAGES = {
    "単語": vocabulary,
    "文章": reading,
    "リスニング": listening,
    "成果": achivement
}


def main():
    """
    Main app
    """
    st.sidebar.title('問題/成果を選択してください')

    # Sidebar body
    selection = st.sidebar.selectbox("選択", list(PAGES.keys()), index=0)
    page = PAGES[selection]
    page.app(selection)

    # Layout adjustment
    st.sidebar.write('\n')
    st.sidebar.write('\n')

    # Brief explanation
    st.sidebar.info(
        """
        * 単語
        単語の勉強をする。\n
        * 文章
        文章の勉強をする。\n
        * リスニング
        リスニングの勉強をする。\n
        * 成果
        今までの成果を見る。\n
        """
    )


if __name__ == "__main__":
    main()