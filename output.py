import streamlit as st
import query_result as qr
import numpy as np
from db import VideoMetadata
import pickle


def update(ss, metadata: VideoMetadata):

    frame_result, count = qr.group_occurence(
        ss["history"][ss["history_num"]]
    )

    result = np.array(
        metadata.map_indices(frame_result)
    )

    result[:, 0] = count.astype(int)

    result = sorted(
        result,
        key=lambda x: x[0],
        reverse=True
    )

    match ss["group_input"]:
        case None:
            result = [["", result]]
        case "Video":
            result = qr.group_by_video(result)

    ss["result"] = qr.paging(result, ss["image_per_page"])


@st.fragment
def gadget(ss, metadata):
    ss["group_input"] = st.selectbox(
        "Group method",
        (None, "Video", "Occurence")
    )
    ss["fetch_nearby"] = st.slider(
        "Fetch nearby frame",
        min_value=0,
        max_value=30,
        value=5
    )

    ss["display_columns"] = st.slider(
        "Display columns",
        value=3,
        min_value=1,
        max_value=8
    )
    ss["image_per_page"] = st.slider(
        "Image per page",
        value=100,
        min_value=1,
        max_value=200
    )
    if st.button(
        label="Update",
        use_container_width=True,
        on_click=update,
        args=(ss, metadata)
    ):
        st.rerun()
