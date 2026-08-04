import streamlit as st
import re

def render():
    """
    Main UI Render function to be called in main.py
    """
    try:
        # 1. Sidebar: Mode Selector
        st.sidebar.title("🎛️ Mode Selector")
        app_mode = st.sidebar.radio(
            "Choose Interface Mode:",
            ["Basic Chat", "Developer Studio"],
            index=0  # Default to Basic Chat
        )
        st.sidebar.markdown("---")

        # Mode switch handling: Reset history when switching modes
        if "previous_mode" not in st.session_state:
            st.session_state.previous_mode = app_mode

        if st.session_state.previous_mode != app_mode:
            st.session_state.messages = []
            st.session_state.previous_mode = app_mode

        dev_config = {}

        # 2. Sidebar Options
        if app_mode == "Developer Studio":
            st.sidebar.subheader("⚙️ Developer Options")
            
            dev_config["provider"] = st.sidebar.selectbox(
                "Select AI Model Provider:",
                ["MistralAI", "ChatGPT", "Gemini", "DeepSeek", "Claude"]
            )
            
            dev_config["model_version"] = st.sidebar.text_input(
                "Enter Model Name / Version:",
                placeholder="e.g., mistral-small-latest / gpt-4o-mini"
            )
            
            dev_config["api_key"] = st.sidebar.text_input(
                "Enter Your API Key:",
                type="password",
                help="Masked and kept safe in session."
            )
            
            dev_config["temperature"] = st.sidebar.slider(
                "Model Temperature:",
                min_value=0.0,
                max_value=1.0,
                value=0.10,
                step=0.05
            )
            
            dev_config["system_prompt"] = st.sidebar.text_area(
                "Enter Custom System Prompt:",
                placeholder="Type custom instructions for LLM...",
                height=120
            )
            
            st.sidebar.markdown("---")
            st.sidebar.subheader("🧠 Token & Memory Controls")
            
            dev_config["history_limit"] = st.sidebar.number_input(
                "Max History Limit (Messages):",
                min_value=2,
                max_value=100,
                value=21
            )
            
            dev_config["trim_count"] = st.sidebar.number_input(
                "Messages to Drop on Exceed:",
                min_value=1,
                max_value=10,
                value=10
            )

        else:
            st.sidebar.subheader("💬 Basic Mode Options")
            st.sidebar.info("Standard mode active with default settings.")

        # 3. Titles
        if app_mode == "Developer Studio":
            st.title("🛠️ DevSphere: Developer AI Studio")
            st.caption("Full control over models, temperature, system prompts, and memory limits.")
        else:
            st.title("💬 DevSphere: Smart AI Assistant")
            st.caption("Clean, simple, and fast AI conversation.")

        st.markdown("---")

        # 4. Chat History Initialization
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Code block parser helper
        def render_formatted_message(content):
            code_blocks = re.split(r'(```[\s\S]*?```)', content)
            for part in code_blocks:
                if part.startswith("```") and part.endswith("```"):
                    lines = part.strip("`").split("\n")
                    language = lines[0].strip() if lines[0].strip() else "python"
                    code_content = "\n".join(lines[1:]) if len(lines) > 1 else lines[0]
                    st.code(code_content, language=language)
                else:
                    if part.strip():
                        st.write(part)

        # 5. Display History Safely
        try:
            for message in st.session_state.messages:
                # Duck-typing to check role without requiring upfront imports
                role = getattr(message, "type", None) or getattr(message, "role", None)
                if role in ["human", "user"]:
                    with st.chat_message("user"):
                        render_formatted_message(getattr(message, "content", str(message)))
                elif role in ["ai", "assistant"]:
                    with st.chat_message("assistant"):
                        render_formatted_message(getattr(message, "content", str(message)))
        except Exception as e:
            if app_mode == "Developer Studio":
                st.error(f"❌ [DevError] Failed to render chat history: {str(e)}")
            else:
                st.warning("⚠️ Couldn't load chat history. Try clearing state.")

        # 6. Chat Input & Dynamic Import Processing
        user_input = st.chat_input("Type your message here...")

        if user_input:
            # -------------------------------------------------------------
            # DYNAMIC IMPORTS & DEPENDENCY SAFEGUARD
            # -------------------------------------------------------------
            try:
                from backend import load_LLM, Chat_bot
            except ModuleNotFoundError as import_err:
                missing_pkg = import_err.name
                st.error(f"⚠️ **Missing Dependency Error:** Package `{missing_pkg}` is not installed.")
                st.info(f"💡 Run this command in your terminal: `pip install -r requirements.txt` or `pip install {missing_pkg}`")
                st.stop()
            except Exception as gen_imp_err:
                st.error(f"❌ Failed to load backend modules: {str(gen_imp_err)}")
                st.stop()

            try:
                # Basic Chat Mode vs Developer Studio Logic Enforcement
                if app_mode == "Basic Chat":
                    api_key_val = None  # Backend falls back to default .env
                    provider_val = "MistralAI"
                    model_ver_val = "mistral-small-latest"
                    temp_val = 0.5
                    sys_prompt_val = None
                    limit_val = 21
                    remove_val = 10
                else:
                    user_provided_key = dev_config.get("api_key", "").strip()
                    
                    if not user_provided_key:
                        st.warning("⚠️ Please enter your API Key in the Developer Options sidebar to proceed.")
                        st.stop()
                    
                    api_key_val = user_provided_key
                    provider_val = dev_config.get("provider", "MistralAI")
                    model_ver_val = dev_config.get("model_version", "").strip()
                    
                    if not model_ver_val:
                        st.warning("⚠️ Please enter a valid Model Name/Version in Developer Options.")
                        st.stop()
                        
                    temp_val = dev_config.get("temperature", 0.1)
                    sys_prompt_val = dev_config.get("system_prompt", "").strip() or None
                    limit_val = dev_config.get("history_limit", 21)
                    remove_val = dev_config.get("trim_count", 10)

                # Render User Message immediately in UI
                with st.chat_message("user"):
                    render_formatted_message(user_input)

                # 1. Dynamic Load LLM
                llm = load_LLM(
                    API_KEY=api_key_val,
                    model_name=provider_val,
                    model_v=model_ver_val,
                    temp=temp_val
                )

                # 2. Call Chat_bot execution
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        bot_response = Chat_bot(
                            user_input=user_input,
                            chat_hist=st.session_state.messages,
                            llm=llm,
                            system_prompt=sys_prompt_val,
                            remove=remove_val,
                            limit=limit_val
                        )
                        render_formatted_message(bot_response)

            except ModuleNotFoundError as pkg_err:
                st.error(f"🚨 **Required SDK Missing:** `{pkg_err.name}` is missing for model provider '{provider_val}'.")
                st.info(f"Please run: `pip install {pkg_err.name}`")
            except Exception as e:
                if app_mode == "Developer Studio":
                    st.error(f"❌ [DevError] Execution failed: {str(e)}")
                else:
                    st.error("⚠️ Failed to generate response. Please check your API Key or connection.")

    except Exception as general_error:
        if 'app_mode' in locals() and app_mode == "Developer Studio":
            st.error(f"🚨 [Fatal Dev Error]: {str(general_error)}")
        else:
            st.error("🚨 Unexpected application error. Please refresh.")