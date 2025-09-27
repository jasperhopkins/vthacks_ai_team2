import streamlit as st
from llmlingua import PromptCompressor
from platformdirs import user_config_dir
from litellm import completion
import json
from pathlib import Path

st.set_page_config(
    page_title="Prompt Compressor App",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Home Page")
st.page_link("pages/API_Configuration.py", label="API Configuration", icon="💻")
st.page_link("pages/About.py", label="About", icon="ℹ️")

col1, col2, col3 = st.columns(3)

with col1:

    def get_config_path():
        config_dir = Path(user_config_dir("prompt-compressor", "ai-team-2"))
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "llm_config.json"

    def load_config():
        config_file = get_config_path()
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return get_default_config()
        return get_default_config()

    def get_default_config():
        return {
            "profiles": {
                "no-llm": {
                    "name": "No LLM (Just Compression)",
                    "provider": "none",
                    "model": "none",
                    "api_key": None,
                    "base_url": None
                }
            },
            "default_profile": "no-llm"
        }

    config = load_config()
    print(config)

    st.subheader("Prompt Compressor")
    prompt = st.text_area("Enter your prompt here...",height=300, placeholder="Enter your prompt here...", label_visibility="collapsed")

    st.subheader("🤖 LLM Configuration")
    if config["profiles"]:
        profile_options = {pid: profile["name"] for pid, profile in config["profiles"].items()}
        
        selected_profile_id = st.selectbox(
            "Choose LLM Profile:",
            options=list(profile_options.keys()),
            format_func=lambda x: profile_options[x],
            index=list(profile_options.keys()).index(config.get("default_profile", list(profile_options.keys())[0])) 
            if config.get("default_profile") in profile_options else 0
        )
        
        selected_profile = config["profiles"][selected_profile_id]
        
        # Show selected profile info
        if selected_profile["provider"] != "none":
            st.info(f"Selected: {selected_profile['name']} ({selected_profile['provider']}/{selected_profile['model']})")
        else:
            st.info("Selected: Compression only (no LLM call)")
    else:
        st.error("No LLM profiles configured. Please go to API Configuration to add some.")
        st.stop()
    
    print(selected_profile)

    rate = st.slider("Compression Rate", 0.1, 1.0, 0.5)

    if st.button("Compress"):
        if not prompt:
            st.warning("Please enter a valid prompt.", icon="☢️")
            st.stop()
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
            st.text_area("Compression Output", value=results['compressed_prompt'],height=400, label_visibility="collapsed")

        word_sep = "\t\t|\t\t"
        label_sep = " "
        lines = results["fn_labeled_original_prompt"].split(word_sep)
        html_string = ""
        for line in lines:
            word, label = line.split(label_sep)
            color = "green" if label == '1' else "red"
            html_string += f"<span style='color:{color}'>{word}</span> "
        with col3:
            st.subheader("Annotated Tokens")
            st.markdown(html_string, unsafe_allow_html=True)
            # include processing parameters (tokens count, etc)
            st.markdown("---")
            st.markdown(f"**Original Tokens:** {results['origin_tokens']}")
            st.markdown(f"**Compressed Tokens:** {results['compressed_tokens']}")
            
        with col2:
            st.subheader("LLM Response")
            if selected_profile['provider'] != None:
                response = response = completion(
                    model=selected_profile['model'],
                    messages=[{"role": "user", "content": results['compressed_prompt']}],
                    api_key=selected_profile['api_key'],
                    # max_tokens=1000,
                    temperature=.7,
                    # timeout=30,
                )
                st.text_area("LLM Response", value=response.choices[0].message.content, height=400, label_visibility="collapsed")