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
    Displays the sidebar for page selection and descriptions.
    Returns the selected page name and module.
    """
    st.sidebar.title('英検５級レベルの問題にチャレンジ❗❗')
    st.sidebar.write('問題か成果を選択して始めよう✏')
    st.sidebar.write('💯目指せ100点💯\n\n')

    # Sidebar: Page selection
    selection = st.sidebar.selectbox("選択", list(PAGES.keys()))

    # Sidebar: Page descriptions
    descriptions = {
        "単語/熟語": "単語/熟語の問題を解く。",
        "文章": "文章の問題を解く。",
        "リスニング": "リスニングの問題を解く。",
        "並び替え": "並び替えの問題を解く。",
        "成果": "今までの成果を見る。"
    }

    st.sidebar.info(f"**{selection}**: {descriptions.get(selection)}")

    return selection, PAGES[selection]


def main():
    """
    Main function to handle Streamlit app rendering.
    """
    selection, selected_page = display_sidebar()

    # Render the selected page and pass the selection as an argument
    if selected_page:
        selected_page.app(selection)  # Pass the selection (page name) to app()
    else:
        st.error("選択されたページが存在しません。")


if __name__ == "__main__":
    main()
