import streamlit as st


ss = st.session_state


def change_page(change):
    c = ss["page_num"] + change
    if c >= 0 and c < len(ss["result"]):
        ss["page_num"] = c


def change_history(change, update_func):
    c = ss["history_num"] + change
    if c >= 0 and c < len(ss["history"]):
        ss["history_num"] = c

        ss["page_num"] = 0


def paging():
    ss["page_num"] = st.slider(
        label="Page",
        value=ss["page_num"],
        min_value=0,
        max_value=len(ss["result"]) - 1
    )

    cols = st.columns(2)

    cols[0].button(
        label="<<",
        on_click=change_page,
        args=(-1,),
        key="ab",
        use_container_width=True)
    cols[1].button(
        label="\>\>",
        on_click=change_page,
        args=(1,),
        key="ac",
        use_container_width=True)


def history(update_func):
    ss["history_num"] = st.slider(
        label="History",
        value=ss["history_num"],
        min_value=1,
        max_value=len(ss["history"]) - 1,
    )

    cols = st.columns(2)

    cols[0].button(
        label="<<",
        on_click=change_history,
        args=(-1, update_func),
        use_container_width=True)
    cols[1].button(
        label="\>\>",
        on_click=change_history,
        args=(1, update_func),
        use_container_width=True)
