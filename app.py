import streamlit as st
from apps import reading, vocabulary, listening, achivement

# Define static pages as constants
PAGES = {
    "単語": vocabulary,
    "文章": reading,
    "リスニング": "listening",
    "成果": "achivement"
}

def main():
    """
    Main app function for Streamlit.
    """
    st.sidebar.title('問題/成果を選択してください')

    # Sidebar: Page selection
    selection = st.sidebar.selectbox("選択", list(PAGES.keys()), index=0)
    page = PAGES[selection]
    page.app(selection)

    # Add some space in the sidebar
    st.sidebar.write('\n' * 2)

    # Sidebar: Brief explanation of each page
    st.sidebar.info(
        """
        * **単語**: 単語の勉強をする。
        * **文章**: 文章の勉強をする。
        * **リスニング**: リスニングの勉強をする。
        * **成果**: 今までの成果を見る。
        """
    )


if __name__ == "__main__":
    main()
