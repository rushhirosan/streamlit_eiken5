import streamlit as st
from apps import reading, vocabulary, listening, achivement

# Define static pages as constants
PAGES = {
    "単語/熟語": vocabulary,
    "文章": reading,
    "リスニング": listening,
    "成果": achivement
}

def main():
    """
    Main app function for Streamlit.
    """
    st.sidebar.title('英検５級レベルの問題にチャレンジ！！\n問題か成果を選択してください')

    # Sidebar: Page selection
    selection = st.sidebar.selectbox("選択", list(PAGES.keys()), index=0)
    page = PAGES[selection]
    page.app(selection)

    # Add some space in the sidebar
    st.sidebar.write('\n' * 2)

    # Sidebar: Brief explanation of each page
    st.sidebar.info(
        """
        * **単語/熟語**: 単語/熟語の問題を解く。
        * **文章**: 文章の問題を解く。
        * **リスニング**: リスニングのの問題を解く。
        * **成果**: 今までの成果を見る。
        """
    )


if __name__ == "__main__":
    main()
