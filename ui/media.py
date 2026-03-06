# ================
# IMPORTS
# ================
import streamlit as st
import base64

# ================
# FUNCTIONS
# ================

# --- RENDER LOOP VIDEO
# --- Goes to ui.landingpage.py
def render_loop_video(path):
# Renders a looping video in the Streamlit interface.
# The video file is read as binary data, encoded to Base64,
# and embedded directly into an HTML <video> tag.
# This allows the video to autoplay and loop without
# requiring a separate video file request from the browser.
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <video width="100%" autoplay loop muted playsinline>
      <source src="data:video/mp4;base64,{data}" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)