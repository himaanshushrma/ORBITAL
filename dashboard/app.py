import os
import sys
import cv2
import time
import tempfile
import streamlit as st

# ======================================================
# STREAMLIT CONFIG (MUST BE FIRST)
# ======================================================

st.set_page_config(
    page_title="ORBITAL AI",
    page_icon="🚦",
    layout="wide"
)

# ======================================================
# LOAD CSS
# ======================================================

def load_css():
    css_path = os.path.join(
        os.path.dirname(__file__),
        "theme.css"
    )

    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

load_css()

# ======================================================
# IMPORT ENGINE
# ======================================================

CURRENT = os.path.dirname(__file__)
SRC = os.path.abspath(
    os.path.join(CURRENT, "../vision/src")
)

if SRC not in sys.path:
    sys.path.append(SRC)

from engine import stream_video

# ======================================================
# SESSION STATE
# ======================================================

if "mission_start" not in st.session_state:
    st.session_state.mission_start = None

# ======================================================
# HEADER
# ======================================================

st.markdown("""
<div style="
padding:20px;
border:1px solid #00E5FF;
border-radius:14px;
background:linear-gradient(90deg,#07101D,#0B1F35);
box-shadow:0 0 20px rgba(0,229,255,.15);
">

<h1 style="
margin:0;
color:#00E5FF;
font-family:Orbitron;
">
🚀 ORBITAL AI COMMAND CENTER
</h1>

<p style="
margin-top:6px;
color:#9BDFFF;
font-family:'JetBrains Mono';
">
EDGE • UAV • COMPUTER VISION • TRAFFIC INTELLIGENCE
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ======================================================
# UPLOAD
# ======================================================

uploaded = st.file_uploader(
    "Upload Traffic Video",
    type=["mp4", "avi", "mov"]
)

if uploaded:

    temp_video = os.path.join(
        tempfile.gettempdir(),
        "orbital_input.mp4"
    )

    with open(temp_video, "wb") as f:
        f.write(uploaded.read())

    st.success("Video uploaded successfully.")
    st.video(temp_video)

    st.write("")

    # ==================================================
    # START MISSION
    # ==================================================

    if st.button(
        "🚀 START MISSION",
        type="primary",
        use_container_width=True
    ):

        st.session_state.mission_start = time.time()

        left, right = st.columns([3, 1])

        with left:
            video_placeholder = st.empty()

        with right:
            total_box = st.empty()
            visible_box = st.empty()
            congestion_box = st.empty()
            fps_box = st.empty()
            timer_box = st.empty()

        st.write("")
        lane_box = st.empty()

        progress = st.progress(0)

        frame_counter = 0

        output_path = None
        report_path = None

        # ==================================================
        # LIVE STREAM
        # ==================================================

        for data in stream_video(temp_video):

            frame_counter += 1

            rgb = cv2.cvtColor(
                data["frame"],
                cv2.COLOR_BGR2RGB
            )

            video_placeholder.image(
                rgb,
                channels="RGB",
                use_container_width=True
            )

            total_box.metric(
                "TOTAL VEHICLES",
                data["total"]
            )

            visible_box.metric(
                "VISIBLE",
                data["visible"]
            )

            congestion_box.metric(
                "CONGESTION",
                data["congestion"]
            )

            fps_box.metric(
                "FPS",
                int(data["fps"])
            )

            elapsed = int(
                time.time() -
                st.session_state.mission_start
            )

            mins = elapsed // 60
            secs = elapsed % 60

            timer_box.metric(
                "MISSION TIME",
                f"{mins:02}:{secs:02}"
            )

            lane_box.markdown(
                f"""
## 🛰 LANE TELEMETRY

| Lane | Vehicles |
|------|---------:|
| **Lane 1** | {data["lanes"][1]} |
| **Lane 2** | {data["lanes"][2]} |
| **Lane 3** | {data["lanes"][3]} |
| **Lane 4** | {data["lanes"][4]} |
"""
            )

            progress.progress(
                min(frame_counter / 300, 1.0)
            )

            output_path = data["output"]
            report_path = data["report"]

        # ==================================================
        # COMPLETE
        # ==================================================

        progress.empty()

        st.success("🎯 Mission Completed Successfully")

        col1, col2 = st.columns(2)

        with col1:
            with open(output_path, "rb") as f:
                st.download_button(
                    "🎥 DOWNLOAD VIDEO",
                    data=f,
                    file_name="ORBITAL_processed.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )

        with col2:
            with open(report_path, "rb") as f:
                st.download_button(
                    "📄 DOWNLOAD REPORT",
                    data=f,
                    file_name="ORBITAL_Traffic_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )