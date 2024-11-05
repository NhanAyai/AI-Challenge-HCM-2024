import streamlit as st
from prompt import Prompt


@st.fragment
def gadget(ss,
           search):

    prompt_input = st.text_area("Prompt")

    st.header(
        "Options",
        divider=True
    )
    cols = st.columns(2)

    with cols[0]:
        tokenize_input = st.toggle("Tokenize")

    with cols[1]:
        ss["query_longclip"] = st.toggle(
            "Long CLIP",
            value=True
        )

        ss["query_metaclip"] = st.toggle(
            "META CLIP",
            value=False
        )

        ss["query_openclip"] = st.toggle(
            "OPENCLIP",
            value=False
        )

    ss["prompt"] = Prompt(text=prompt_input)

    if tokenize_input:
        ss["token_sentence"] = ss["prompt"].tokenize()

        ss["token_sentence"].append(ss["prompt"].text)

        ss["search_query"] = st.multiselect(
            label="Tokenize sentence",
            options=ss["token_sentence"]
        )
    else:
        ss["search_query"] = ss["prompt"].text

    st.header(
        "Query text",
        divider=True
    )
    st.write(ss["search_query"])

    ss["max_result"] = st.slider(
        "Max result for query",
        value=100,
        min_value=1,
        max_value=1000
    )
    if st.button(
        label="search",
        on_click=search,
        use_container_width=True
    ):
        st.rerun()
