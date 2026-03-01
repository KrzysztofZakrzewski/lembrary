import streamlit as st
import base64

def render_loop_video(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <video width="100%" autoplay loop muted playsinline>
      <source src="data:video/mp4;base64,{data}" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)