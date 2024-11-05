import streamlit as st
import requests
import json

ss = st.session_state
MSG_TEMPLATE = {
    "model": "llama2",
    "messages": [{
        "role": "user",
        "content": ""
    }],
    "stream": True
}


def update_endpoint(endpoint: str):
    ss["llm_endpoint"] = endpoint


def sent_chat(msg):
    msg_dict = MSG_TEMPLATE.copy()
    msg_dict["messages"][0]["content"] = msg
    r = requests.post(
        ss["llm_endpoint"],
        json=msg_dict,
        stream=True
    )
    for msg in r.iter_lines():
        if msg:
            yield json.loads(msg)["message"]["content"]


def llm_chat(container):
    with container:
        with st.expander(
                label="LLM Endpoint",
        ):
            llm_endpoint_u = st.text_input(
                label="URL",
                value=ss["llm_endpoint"]
            )
            st.button(
                label="Update endpoint",
                on_click=lambda x: update_endpoint(x),
                args=(llm_endpoint_u,)
            )

        messages_container = st.container(height=300)

        for msg in ss["messages"]:
            messages_container.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            ss["messages"].append({"role": "user", "content": prompt})

            messages_container.chat_message("user").write(prompt)

            with messages_container.chat_message("assistant"):
                stream = sent_chat(prompt)
                response = st.write_stream(stream)
            ss["messages"].append({"role": "assistant", "content": response})
