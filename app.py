import requests
import streamlit as st
from datetime import datetime

# =========================
# Configuration
# =========================
TEMP_API_URL = st.secrets["TEMP_API_URL"]
API_KEY = st.secrets["API_KEY"]
URL = f"{TEMP_API_URL}/api/v1/generate"

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="YouTube Summarizer",
    page_icon="🎥",
    layout="wide",
)

# =========================
# Custom Styling
# =========================
st.markdown(
    """
<style>

.main {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

div[data-testid="stTextInput"] input {
    border-radius: 12px;
    padding: 0.8rem;
}

.stButton > button {
    width: 100%;
    height: 3rem;
    border-radius: 12px;
    font-size: 17px;
    font-weight: 600;
}

.summary-box {
    padding: 1.5rem;
    border-radius: 14px;
    border: 1px solid #E5E7EB;
    background: #FAFAFA;
    margin-top: 1rem;
    line-height: 1.8;
}

.hero {
    background: linear-gradient(135deg,#1E3A8A 0%,#2563EB 100%);
    padding: 2.5rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 2rem;
}

.hero h1{
    font-size:3rem;
    margin-bottom:0.3rem;
}

.hero p{
    font-size:1.1rem;
    color:#E5E7EB;
}

.hero-features{
    display:flex;
    gap:10px;
    flex-wrap:wrap;
    margin-top:20px;
}

.feature{
    background:rgba(255,255,255,.15);
    padding:8px 14px;
    border-radius:999px;
    font-size:14px;
}

</style>
""",
    unsafe_allow_html=True,
)

# =========================
# Session State
# =========================
if "summary" not in st.session_state:
    st.session_state.summary = None

if "last_url" not in st.session_state:
    st.session_state.last_url = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "loading" not in st.session_state:
    st.session_state.loading = False

# =========================
# Hero
# =========================
st.markdown(
    """
<div class="hero">

# 🎥 YouTube AI Summarizer

Generate concise, high-quality AI summaries from any public YouTube video in seconds.

<div class="hero-features">
<div class="feature">🎓 Lectures</div>
<div class="feature">🎙 Podcasts</div>
<div class="feature">📚 Tutorials</div>
<div class="feature">🎤 Interviews</div>
</div>

</div>
""",
    unsafe_allow_html=True,
)

# =========================
# Sidebar
# =========================
with st.sidebar:

    st.title("Settings")

    st.caption("Customize your summary.")

    max_length = st.slider(
        "Maximum Summary Length",
        min_value=500,
        max_value=5000,
        value=3000,
        step=100,
    )

    st.divider()

    st.info(
        """
**Tips**

• Public videos only

• Videos with captions work best

• Longer summaries preserve more detail
"""
    )

# =========================
# Main Layout
# =========================
left, right = st.columns([1, 2], gap="large")

# =========================
# Input Card
# =========================
with left:

    with st.container(border=True):

        st.subheader("Video")

        st.caption("Paste any public YouTube video.")

        youtube_url = st.text_input(
            "YouTube URL",
            placeholder="https://youtu.be/example",
            label_visibility="collapsed",
        )

        if youtube_url:

            try:
                if youtube_url:
                    st.markdown("#### Preview")

                    try:
                        st.video(youtube_url)

                    except Exception:
                        st.warning("Unable to preview this video.")

            except Exception:
                st.warning("Unable to preview this video.")

        generate = st.button(
            "⏳ Generating..." if st.session_state.loading else "Generate Summary",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.loading,
        )

# =========================
# Output Card
# =========================
with right:

    with st.container(border=True):

        st.subheader("AI Summary")

        if generate:

            if not youtube_url:
                st.warning("Please enter a YouTube URL.")
                st.stop()

            headers = {"Authorization": f"Bearer {API_KEY}"}

            payload = {
                "youtube_url": youtube_url,
                "max_length": max_length,
            }

            with st.spinner("Analyzing video..."):

                try:

                    response = requests.post(
                        URL,
                        headers=headers,
                        json=payload,
                        timeout=300,
                    )

                    response.raise_for_status()

                    summary = response.json()["response"]["summary"]

                    st.session_state.summary = summary
                    st.session_state.last_url = youtube_url

                    # Save to history
                    st.session_state.history.insert(
                        0,
                        {
                            "url": youtube_url,
                            "summary": summary,
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        },
                    )

                    # Keep only latest 5
                    st.session_state.history = st.session_state.history[:5]

                    st.success("Summary generated successfully!")
                    st.session_state.loading = False

                    words = len(summary.split())

                    reading_time = max(1, words // 200)

                    m1, m2, m3, m4 = st.columns(4)

                    with m1:
                        st.metric(
                            "Words",
                            words,
                        )

                    with m2:
                        st.metric(
                            "Reading Time",
                            f"{reading_time} min",
                        )

                    with m3:
                        st.metric(
                            "Limit",
                            max_length,
                        )

                    with m4:
                        st.metric(
                            "Compression",
                            "AI",
                        )

                    st.subheader("✨ AI Summary")
                    st.caption("Your generated summary will appear below.")

                    summary_container = st.container(border=True)

                    with summary_container:

                        st.markdown("### Generated Summary")

                        st.markdown(summary)

                    action1, action2 = st.columns(2)

                    with action1:

                        st.download_button(
                            "Download Summary",
                            st.session_state.summary,
                            file_name="youtube_summary.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )

                    with action2:

                        st.code(
                            st.session_state.summary,
                            language=None,
                        )

                except requests.exceptions.Timeout:

                    st.session_state.loading = False

                    st.error(
                        """
                The request timed out.

                Try again in a few seconds.
                """
                    )

                except requests.exceptions.HTTPError:
                    st.session_state.loading = False
                    st.error(
                        """
                The server returned an unexpected response.

                Please try again later.
                """
                    )

                except requests.exceptions.ConnectionError:
                    st.session_state.loading = False
                    st.error(
                        """
                Unable to connect to the API.

                Check your internet connection.
                """
                    )

                except Exception as e:

                    st.session_state.loading = False
                    st.error(
                        f"""
                        Something went wrong while generating the summary.
                        """
                    )

        else:

            st.markdown(
                        """
                    ### Ready to summarize

                    Paste a YouTube URL and click **Generate Summary**.
                    """
                    )

# =========================
# Recent Summaries
# =========================

st.divider()

st.subheader("Recent Summaries")

if st.session_state.history:

    for index, item in enumerate(st.session_state.history):

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.markdown(
                    f"""
                    **Video**

                    {item["url"]}

                    {item["time"]}
                    """
                )

            with col2:

                if st.button(
                    "Open",
                    key=f"history_{index}",
                ):
                    st.session_state.summary = item["summary"]
                    st.session_state.last_url = item["url"]
                    st.rerun()

else:

    st.info(
        "No summaries yet. Generate your first summary to see it here."
    )