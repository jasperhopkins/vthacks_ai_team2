import streamlit as st

# Page setup
st.set_page_config(
    page_title="About | Prompt Compressor",
    page_icon="ℹ️",
    layout="wide"
)

# Top banner
st.markdown("""
    <div style='background-color:#F5F5F5; padding:20px; text-align:center; color:black; font-size:36px; font-weight:bold;'>
        ℹ️ About This App
    </div>
""", unsafe_allow_html=True)

# Content layout
st.markdown("## 🤖 What Is Prompt Compressor?")
st.markdown("""
Prompt Compressor is a Streamlit-based tool built for VTHacks 13 that leverages **LLMLingua** to simplify and optimize long prompts for large language models. It helps users compress verbose input while preserving semantic meaning, making it ideal for chatbot pipelines, prompt engineering, and token-efficient applications.
""")

st.markdown("## 🧠 Why We Built It")
st.markdown("""
- To explore how compression affects LLM performance
- To visualize token importance and retention
- To provide a hands-on tool for developers and researchers working with prompt-heavy workflows
""")

st.markdown("## 👥 Meet the Team")
st.markdown(""" 
- **Team Members** — Jasper Hopkins, Garrison Underwood
""")

st.markdown("## 🛠️ Technologies Used")
st.markdown("""
- [LLMLingua](https://github.com/microsoft/LLMLingua) for prompt compression  
- Streamlit for interactive UI  
- Python for backend logic  
""")

st.markdown("---")

st.markdown("## 📆 Project Timeline")

st.markdown("""
<style>
.timeline-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px;
    margin-top: 30px;
}
.timeline-card {
    background-color: #f0f0f0;
    border-left: 6px solid #4B8BBE;
    padding: 15px;
    width: 180px;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
    font-family: sans-serif;
}
.timeline-card h4 {
    margin: 0;
    font-size: 18px;
    color: #333;
}
.timeline-card p {
    margin: 5px 0 0;
    font-size: 14px;
    color: #666;
}
</style>

<div class="timeline-container">
    <div class="timeline-card">
        <h4>Sept 26 @ 8:00pm</h4>
        <p>Brainstormed and researches text compression.</p>
    </div>
    <div class="timeline-card">
        <h4>Sept 26 @ 9:00pm</h4>
        <p>Implemented a first draft that kinda cooked.</p>
    </div>
    <div class="timeline-card">
        <h4>Sept 27</h4>
        <p>Vibe coded Streamlit UI/UX. Made multiple pages for the site.</p>
    </div>
    <div class="timeline-card">
        <h4>Sept 27 @ Night</h4>
        <p>Lost track of time, forgot to shower, made an awesome program.</p>
    </div>
    <div class="timeline-card">
        <h4>Sept 28</h4>
        <p>Project sumbitted, nail bitting, nerves.</p>
    </div>
</div>
""", unsafe_allow_html=True)



# Footer
st.markdown("""
    <div style='text-align:center; font-size:14px; color:gray; padding-top:20px;'>
        Made with ❤️ at VTHacks 13 | Powered by LLMLingua + Streamlit
    </div>
""", unsafe_allow_html=True)