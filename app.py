import streamlit as st
from apps import reading, vocabulary, listening, ordering, achivement

# Define pages mapping
PAGES = {
    "単語/熟語": vocabulary,
    "文章": reading,
    "リスニング": listening,
    "並び替え": ordering,
    "成果": achivement
}


def display_sidebar():
    """
    Displays the sidebar with page selection and descriptions.
    """
    st.sidebar.title('英検５級レベルの問題にチャレンジ❗❗\n問題か成果を選択してください✏')
    st.sidebar.write('\n' * 2)

    # Sidebar: Page selection
    selection = st.sidebar.selectbox("選択", list(PAGES.keys()), index=0)

    # Sidebar: Brief explanation of each page
    st.sidebar.info(
        """
        * **単語/熟語**: 単語/熟語の問題を解く。
        * **文章**: 文章の問題を解く。
        * **リスニング**: リスニングの問題を解く。
        * **並び替え**: 並び替えの問題を解く。
        * **成果**: 今までの成果を見る。
        """
    )

    return selection


def main():
    """
    Main function to handle Streamlit app rendering.
    """
    selection = display_sidebar()
    page = PAGES.get(selection)

    if page:
        page.app(selection)
    else:
        st.error("選択されたページが存在しません。")


if __name__ == "__main__":
    main()
