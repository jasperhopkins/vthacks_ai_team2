import streamlit as st
from llmlingua import PromptCompressor
from platformdirs import user_config_dir
from litellm import completion
import json
from pathlib import Path
import time

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

    st.subheader("Prompt Compressor")

    prompt = st.text_area("Enter your prompt here...", height=300, value=st.session_state.prompt, placeholder="Enter your prompt here...", label_visibility="collapsed")

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
            llm_col1, llm_col2, llm_col3 = st.columns(3)
            with llm_col1:
                temperature = st.slider("Temperature", 0.0, 2.0, 0.7)
            with llm_col2:
                max_completion_tokens = st.slider("Max Tokens", 0, 65536, 4096)
            with llm_col3:
                top_p = st.slider("Top P", 1, 30, 1)

            st.info(f"Selected: {selected_profile['name']} ({selected_profile['provider']}/{selected_profile['model']})")
        else:
            st.info("Selected: Compression only (no LLM call)")
    else:
        st.error("No LLM profiles configured. Please go to API Configuration to add some.")
        st.stop()

    rate = st.slider("Compression Rate", 0.1, 1.0, 0.5)

    if 'history' not in st.session_state:
        st.session_state.history = [];

    button_col1, button_col2, button_col3 = st.columns(3)
    with button_col1:
        add_history = st.checkbox("Add prompt and response to history", value=False)
    with button_col2:
        if st.button("Enhance"):
            pass
    with button_col3:
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
                if selected_profile['model'] != "none":
                    st.subheader("LLM Response")
                    response = response = completion(
                        model=selected_profile['model'],
                        messages= st.session_state.history + [{"role": "user", "content": results['compressed_prompt']}],
                        api_key=selected_profile['api_key'],
                        temperature=temperature,
                        max_completion_tokens=max_completion_tokens,
                        top_p=top_p,
                        stream=True,
                        base_url=selected_profile['base_url'] 
                    )

                    chat = ""
                    response_text = ""
                    for message in st.session_state.history:
                        chat += f"{message['role']}:\n\n{message['content']}\n\n"
                    chat += f"user:\n\n{results['compressed_prompt']}\n\nassistant:\n\n"
                    placeholder = st.empty()
                    placeholder.text_area("LLM Response", value=chat, height=400, label_visibility="collapsed", key="first_output")

                    for chunk in response:
                        if chunk.choices[0].delta.content:
                            chat += chunk.choices[0].delta.content
                            response_text += chunk.choices[0].delta.content
                            placeholder.text_area("LLM Response", value=chat + " ", height=400, label_visibility="collapsed", key=f"stream_output_{len(chat)}")
                            time.sleep(.01)
                    placeholder.text_area("LLM Response", value=chat + " ", height=400, label_visibility="collapsed", key="final_output")

                    if add_history:
                        
                        compressed_response = compressor.compress_prompt_llmlingua2(
                            response_text,
                            rate=rate,
                            chunk_end_tokens=['.', '\n'],
                            return_word_label=True,
                            drop_consecutive=True
                        )

                        st.session_state.history += [{"role": "user", "content": results['compressed_prompt']}, {"role": "assistant", "content": compressed_response['compressed_prompt']}]
