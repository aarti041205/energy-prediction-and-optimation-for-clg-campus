import os
import sys
import time
import streamlit as st

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from dashboard.api_client import post_chat
from dashboard.components.theme_manager import apply_saas_theme
from dashboard.components.navbar import render_navbar
from dashboard.components.footer import render_footer

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
apply_saas_theme()
render_navbar("AI Gemini RAG Command Assistant", "Generative AI Knowledge Retrieval Engine")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Suggested Prompts
st.markdown('<div class="saas-card">', unsafe_allowed_html=True)
st.write("**Suggested Prompts:**")
col1, col2, col3 = st.columns(3)
if col1.button("💡 What is the AI Lab baseline load?"):
    st.session_state.prompt_input = "What is the AI Lab baseline load?"
if col2.button("🌡️ How does temperature affect HVAC?"):
    st.session_state.prompt_input = "How does temperature affect HVAC?"
if col3.button("☀️ What is the rooftop solar capacity?"):
    st.session_state.prompt_input = "What is the rooftop solar capacity?"
st.markdown('</div>', unsafe_allowed_html=True)

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 Source Citations"):
                for s in msg["sources"]:
                    st.write(f"- **[{s['source']}]**: {s['snippet']}")

# Prompt Input
prompt = st.chat_input("Ask any question regarding campus energy telemetry or baseline...")
if hasattr(st.session_state, "prompt_input") and st.session_state.prompt_input:
    prompt = st.session_state.prompt_input
    st.session_state.prompt_input = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("Searching FAISS Vector DB & Consulting Gemini LLM..."):
            history_payload = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
            res = post_chat(prompt, history=history_payload)
            if res.get("success"):
                data = res["data"]
                answer = data["answer"]
                sources = data.get("sources", [])

                full_text = ""
                for word in answer.split(" "):
                    full_text += word + " "
                    placeholder.markdown(full_text + "▌")
                    time.sleep(0.012)

                placeholder.markdown(f"{answer}\n\n*Confidence Score: {data.get('confidence', 0.90)*100:.0f}%*")

                if sources:
                    with st.expander("📚 Source Citations"):
                        for s in sources:
                            st.write(f"- **[{s['source']}]**: {s['snippet']}")

                st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
            else:
                st.error(res.get("error"))

render_footer()
