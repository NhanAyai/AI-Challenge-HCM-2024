import streamlit as st

YOUTUBE_URL = f"https://youtu.be"

ss = st.session_state


def display_image_full(
        f,
        metadata,
        youtube_popup_callback,
        nearby_popup_callback,
        search_nearby_callback,
        kidx,
):
    vid_name = f"L{f[2]:02d}_V{f[3]:03d}"
    set_name = f"Videos_L{f[2]:02d}_a"

    fps, youtube_id = metadata.get_by_name(vid_name)

    time = int(f[4]/fps)
    url = f"{YOUTUBE_URL}/{youtube_id}"

    path = f"{ss['kf_dir']}/{set_name}/{vid_name}/{f[4]:06d}.jpg"
    container = st.container(border=True)
    with container:
        m, s = divmod(time, 60)

        st.caption(
            f"Occurence {f[0]} - Time {m}:{s:02d}",
        )

        st.image(
            image=path,
            use_column_width=True
        )

        st.code(
            f"{vid_name}, {time*1000}",
            language="markdown"
        )

        cols = st.columns(3)
        cols[0].button(
            label="YouTube Video",
            use_container_width=True,
            on_click=youtube_popup_callback,
            args=(url, time), key=f"{kidx}0"
        )
        cols[1].button(
            label="Show nearby",
            use_container_width=True,
            on_click=nearby_popup_callback,
            args=(f, metadata, set_name, vid_name, fps),
            key=f"{kidx}1"
        )
        cols[2].button(
            label="Search similiar",
            use_container_width=True,
            on_click=search_nearby_callback,
            args=(path,),
            key=f"{kidx}2"
        )
    return container


def display_img_nearby(
        f,
        fps,
        set_name,
        vid_name,
):
    with st.container(border=True):
        time = int(f[4]/fps)
        m, s = divmod(time, 60)

        path = f"{ss['kf_dir']}/{set_name}/{vid_name}/{f[4]:06d}.jpg"

        st.caption(
            f"Occurence {f[0]} - Time {m}:{s:02d}",
        )

        st.image(
            image=path,
            use_column_width=True
        )

        st.code(
            f"{vid_name}, {time * 1000}",
            language="markdown"
        )
    pass
