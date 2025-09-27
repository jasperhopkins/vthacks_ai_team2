import streamlit as st
from llmlingua import PromptCompressor

st.title("Prompt Compressor")
prompt = st.text_area("Enter your prompt")

rate = st.slider("Compression Rate", 0.1, 1.0, 0.6)

if st.button("Compress"):
    compressor = PromptCompressor(
        model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
        use_llmlingua2=True,
        device_map="cpu"
    )
    results = compressor.compress_prompt_llmlingua2(
        prompt,
        rate=rate,
        force_tokens=['\n', '.', '!', '?', ','],
        chunk_end_tokens=['.', '\n'],
        return_word_label=True,
        drop_consecutive=True
    )
    st.subheader("Compressed Output")
    st.write(results['compressed_prompt'])

    st.subheader("Annotated Tokens")
    word_sep = "\t\t|\t\t"
    label_sep = " "
    lines = results["fn_labeled_original_prompt"].split(word_sep)
    for line in lines:
        word, label = line.split(label_sep)
        color = "green" if label == '1' else "red"
        st.markdown(f"<span style='color:{color}'>{word}</span>", unsafe_allow_html=True)
