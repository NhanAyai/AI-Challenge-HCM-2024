import streamlit as st
import dash.llm_chat
import dash.sidebar.paging
import longclip_model
import dash.sidebar.output
import dash.sidebar.query
import dash.output
import db
import dash
import openclip_model
import numpy as np
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

st.set_page_config(
    page_title="Video search dashboard",
    page_icon="🐍",
    layout="wide")


ss = st.session_state

if "llm_endpoint" not in ss:
    ss["llm_endpoint"] = "http://0.0.0.0:11434/api/chat"
if "query_result" not in ss:
    ss["query_result"] = None
    ss["history"] = [[]]
    ss["result"] = [[]]
    ss["page_num"] = 0
    ss["history_num"] = 0


if "max_result" not in ss:
    ss["max_result"] = 100

if "kf_dir" not in ss:
    ss["kf_dir"] = "./keyframes"


if "messages" not in ss:
    ss["messages"] = []


@st.cache_resource
def init_longclip(show_spinner=True):
    model = longclip_model.LongCLIPModel(
        "./ckpt/longclip-L.pt", "cpu")

    db_longclip = db.DB(
        "./db/faiss_LongCLIP.bin",
    )
    return model, db_longclip


@st.cache_resource
def init_metaclip(show_spinner=True):
    model = openclip_model.OpenCLIP(
        "ViT-L-14-quickgelu",
        "./ckpt/l14_400m.pt"
    )
    db_metaclip = db.DB(
        "./db/faiss_MetaCLIP.bin",
    )
    return model, db_metaclip


@st.cache_resource
def init_openclip(show_spinner=True):
    model = openclip_model.OpenCLIP(
        "ViT-H-14-quickgelu",
        "./ckpt/dfn5b_vit_h_14.bin"
    )
    db_metaclip = db.DB(
        "./db/faiss_openCLIP.bin",
    )
    return model, db_metaclip


@st.cache_resource
def init_miscelleneous(show_spinner=True):

    video_metadata = db.VideoMetadata(
        "./db/video_metadata.npy",
        "./db/index_frame.pkl",
        "./db/index_compact_2.npy"
    )

    return video_metadata


metadata = init_miscelleneous()

longclip_model, db_longclip = init_longclip()

metaclip_model, db_metaclip = init_metaclip()

openclip_model, db_openclip = init_openclip()


def search_text():
    texts = ss["search_query"]
    results = []
    if ss["query_longclip"]:
        longclip_token = longclip_model.encode_text(texts)
        results.append(
            db_longclip.query(
                longclip_token,
                ss["max_result"]
            )
        )

    if ss["query_metaclip"]:
        metaclip_token = metaclip_model.encode_text(texts)
        results.append(
            db_metaclip.query(
                metaclip_token,
                ss["max_result"]
            )
        )

    if ss["query_openclip"]:
        openclip_token = openclip_model.encode_text(texts)
        results.append(
            db_openclip.query(
                openclip_token,
                ss["max_result"]
            )
        )

    ss["page_num"] = 0
    ss["history_num"] = len(ss["history"])
    ss["history"].append(np.concatenate(results))
    dash.sidebar.output.update(ss, metadata)


def search_image(image_path):
    results = []
    if ss["query_longclip"]:
        longclip_token = longclip_model.encode_image(image_path)
        results.append(
            db_longclip.query(
                longclip_token,
                ss["max_result"]
            )
        )

    if ss["query_metaclip"]:
        metaclip_token = metaclip_model.encode_image(image_path)
        results.append(
            db_metaclip.query(
                metaclip_token,
                ss["max_result"]
            )
        )

    if ss["query_openclip"]:
        openclip_token = openclip_model.encode_image(image_path)
        results.append(
            db_openclip.query(
                openclip_token,
                ss["max_result"]
            )
        )

    ss["page_num"] = 0
    ss["history_num"] = len(ss["history"])
    ss["history"].append(np.concatenate(results))
    dash.sidebar.output.update(ss, metadata)


with st.sidebar:
    if len(ss["history"]) > 2:
        dash.sidebar.paging.history(dash.sidebar.output.update(ss, metadata))
    if len(ss["result"]) > 1:
        dash.sidebar.paging.paging()
    else:
        ss["page_num"] = 0

    tabs = st.tabs(["Query", "Output"])
    with tabs[0]:
        dash.sidebar.query.gadget(ss,  search_text)
    with tabs[1]:
        dash.sidebar.output.gadget(ss, metadata)


ss["page_num"] = max(0, ss["page_num"])

main_tabs = st.tabs(["Result", "LLM"])

results_container = main_tabs[0].container()
llm_container = main_tabs[1].container()

dash.output.show_result(
    ss["result"][ss["page_num"]],
    results_container,
    metadata,
    search_image,
    ss["display_columns"]
)

dash.llm_chat.llm_chat(llm_container)
