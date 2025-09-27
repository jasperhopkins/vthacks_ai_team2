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
- **Team Members** — (Add names and roles here)
""")

st.markdown("## 🛠️ Technologies Used")
st.markdown("""
- [LLMLingua](https://github.com/microsoft/LLMLingua) for prompt compression  
- Streamlit for interactive UI  
- Python for backend logic  
""")

st.markdown("---")

# Footer
st.markdown("""
    <div style='text-align:center; font-size:14px; color:gray; padding-top:20px;'>
        Made with ❤️ at VTHacks 13 | Powered by LLMLingua + Streamlit
    </div>
""", unsafe_allow_html=True)