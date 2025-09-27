import streamlit as st
from llmlingua import PromptCompressor

st.set_page_config(
    page_title="Prompt Compressor App",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Home Page")
st.page_link("pages/API_Configuration.py", label="API Configuration", icon="💻")
col1, col2, col3 = st.columns(3)

with col1:

    # st.title("Prompt Compressor")
    st.subheader("Prompt Compressor")
    prompt = st.text_area("",height=300, placeholder="Enter your prompt here...", label_visibility="collapsed")

    rate = st.slider("Compression Rate", 0.1, 1.0, 0.5)

    if st.button("Compress"):
        compressor = PromptCompressor(
            model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
            use_llmlingua2=True,
            device_map="cpu"
        )
        results = compressor.compress_prompt_llmlingua2(
            prompt,
            rate=rate,
            # force_tokens=['\n', '.', '!', '?', ','],
            chunk_end_tokens=['.', '\n'],
            return_word_label=True,
            drop_consecutive=True
        )
        with col2:
            st.subheader(f"Compressed Output: {results['rate']}")
            st.text_area("Output", value=results['compressed_prompt'],height=400, label_visibility="collapsed"
            )
            # st.markdown(f'<div class="wrap-text">{results['compressed_prompt']}</div>', unsafe_allow_html=True)
            # st.write(results['compressed_prompt'])

        word_sep = "\t\t|\t\t"
        label_sep = " "
        lines = results["fn_labeled_original_prompt"].split(word_sep)
        html_string = ""
        for line in lines:
            word, label = line.split(label_sep)
            color = "green" if label == '1' else "red"
            html_string += f"<span style='color:{color}'>{word}</span> "
            # st.markdown(f"<span style='color:{color}'>{word}</span>", unsafe_allow_html=True)
        with col3:
            st.subheader("Annotated Tokens")
            st.markdown(html_string, unsafe_allow_html=True)