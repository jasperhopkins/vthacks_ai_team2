import streamlit as st
# from litellm import completion
from platformdirs import user_config_dir
import json
from pathlib import Path

st.set_page_config(
    page_title="API Configuration",
    page_icon="💻",
    layout="wide"
)

# Config management functions
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

def save_config(config):
    config_file = get_config_path()
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

def get_default_config():
    return {
        "profiles": {
            "openai-gpt4": {
                "name": "GPT-4 Production",
                "provider": "openai",
                "model": "gpt-4",
                "api_key": "",
                "base_url": None
            },
            "local-llama": {
                "name": "Local Llama",
                "provider": "ollama",
                "model": "llama2",
                "api_key": None,
                "base_url": "http://localhost:11434"
            }
        },
        "default_profile": "openai-gpt4"
    }

# Load existing config
config = load_config()

st.title("💻 API Configuration")
st.page_link("Home.py", label="Home", icon="🏠")
st.write(f"Config stored at: `{get_config_path()}`")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Configured APIs")
    
    for profile_id, profile in config["profiles"].items():
        with st.expander(f"{profile['name']} ({profile['provider']})"):
            st.json({k: v if k != "api_key" else "***hidden***" for k, v in profile.items()})
            
            if st.button(f"Delete {profile['name']}", key=f"delete_{profile_id}"):
                del config["profiles"][profile_id]
                if config["default_profile"] == profile_id:
                    config["default_profile"] = list(config["profiles"].keys())[0] if config["profiles"] else None
                save_config(config)
                st.rerun()

with col2:
    st.subheader("Add New API")
    
    with st.form("add_api"):
        name = st.text_input("Display Name", placeholder="My Custom API")
        provider = st.selectbox("Provider", ["openai", "anthropic", "ollama", "custom"])
        model = st.text_input("Model", placeholder="gpt-4, claude-3-sonnet, etc.")
        api_url = st.text_input("Base URL", placeholder="http://localhost:11434 (optional)")
        api_key = st.text_input("API Key", placeholder="Enter your API key...", type="password")
        
        submitted = st.form_submit_button("Add API")
        
        if submitted:
            if name and provider and model:
                # Generate unique profile ID
                profile_id = name.lower().replace(" ", "-").replace("_", "-")
                counter = 1
                original_id = profile_id
                while profile_id in config["profiles"]:
                    profile_id = f"{original_id}-{counter}"
                    counter += 1
                
                # Add new profile
                config["profiles"][profile_id] = {
                    "name": name,
                    "provider": provider,
                    "model": model,
                    "api_key": api_key if api_key else None,
                    "base_url": api_url if api_url else None
                }
                
                save_config(config)
                st.success(f"Added {name}!")
                st.rerun()
            else:
                st.error("Please fill in at least Name, Provider, and Model")

# Default profile selector
if config["profiles"]:
    st.subheader("Default Profile")
    current_default = config.get("default_profile")
    profile_names = {pid: profile["name"] for pid, profile in config["profiles"].items()}
    
    selected = st.selectbox(
        "Choose default profile:",
        options=list(profile_names.keys()),
        format_func=lambda x: profile_names[x],
        index=list(profile_names.keys()).index(current_default) if current_default in profile_names else 0
    )
    
    if selected != current_default:
        config["default_profile"] = selected
        save_config(config)
        st.success(f"Default profile changed to {profile_names[selected]}")