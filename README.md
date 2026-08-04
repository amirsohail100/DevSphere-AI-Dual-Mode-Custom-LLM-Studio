# 🤖 DevSphere AI — Dual-Mode Custom LLM Studio

DevSphere AI is a flexible, highly configurable AI chat interface designed for both non-technical users and developers. It provides seamless everyday AI conversation alongside an advanced Developer Studio for granular model tuning and prompt engineering.

---

## 🚀 Live Application

You can try the live app here: **[[[Insert Live Link Here]()]]**

---

### 💡 Problem Statement & What I Solved

#### 1. The Problem with Standard AI Chatbots:

- **Fixed Architecture & Strict Limits:** Regular chatbots don't allow control over system prompts, temperature, memory limits, or precise model selection.
- **API Key & Rate Constraints:** Standard apps force users onto a single provided API key or hardcoded model, causing rate-limit issues and zero flexibility for developers who want to use their own keys.
- **Lack of Memory Control:** Long conversations often exceed context windows, crashing the chat or draining API tokens unnecessarily.

#### 2. How DevSphere AI Fixes This:

- **Dual-Interface Mode:**
  - **Basic Chat Mode:** A clean, zero-config assistant for standard everyday queries powered by default settings.
  - **Developer Studio:** Total control over AI parameters—switch providers (Mistral, OpenAI, Gemini, Claude, DeepSeek), change model versions, set custom system prompts, and adjust temperatures.
- **Strict API Isolation & Privacy:** In Developer Mode, the user’s API key is required and masked, preventing unauthorized usage of system/owner API keys while providing dynamic provider switching.
- **Smart Memory Management:** Integrated automatic token/chat history trimming limits to prevent context window overflow and save token costs without breaking conversation flow.
- **Fault-Tolerant & Isolated Design:** Lazy-loading of dependencies ensures the UI stays lightweight and loads instantly without breaking if optional provider SDKs are missing.

---

### ✨ Features

- 🎛️ **Dual Mode UI:** Seamless toggle between Basic User Chat and Developer Studio.
- 🔑 **Masked & Secure API Keys:** `password` type fields to keep sensitive keys hidden.
- 🧠 **Dynamic Memory Trimming:** Configurable history limits and drop counts.
- 💻 **Syntax Highlighting:** Automatic detection and formatting of code blocks.
- ⚡ **Lazy Imports & Fallbacks:** Bulletproof UI loading with step-by-step dependency error guides.

---

## 📁 Project Structure

```text
lexilearn-ai/
├── .env                  # Fresh Mistral API Key (Keep it safe)
├── .gitignore            # Excludes .env and .venv from GitHub
├── requirements.txt      # Lightweight dependencies (Streamlit, LangChain)
├── backend.py            # LLM Logic & Dynamic Prompts
├── frontend.py           # Streamlit UI Components
├── UI_1.py               # UI image Basic chat bot
├── UI_2.py               # UI image Developer Studio_2.
├── UI_3.py               # UI image Developer Studio_3.
└── main.py               # Main Entry Point
```

---

## Cloning the Repository

To clone the repository, run the following command:

```bash
git clone https://github.com/amirsohail100/DevSphere-AI-Dual-Mode-Custom-LLM-Studio.git
```

## 💻 Installation

1. Install Python 3.10 or higher.

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3.  Create a `.env` file in the project root directory and add your Mistral API key:

```bash
MISTRAL_API_KEY = "your_api_key_here"
```

4. Run the application:

```bash
streamlit run main.py
```

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- Thanks to [Mistral AI](https://mistral.ai/) for providing the Mistral API.
- Thanks to [LangChain](https://github.com/hwchase17/langchain) for the LangChain library.
- Thanks to [Streamlit](https://github.com/streamlit/streamlit) for the Streamlit library.

DevSphere AI is a dual-mode LLM studio that solves strict API restrictions and lack of developer control in standard chatbots. Users enjoy a clean default AI chat, while developers get total control—switching providers, models, system prompts, temperature, memory trim limits, and using their own API keys dynamically with maximum privacy.
