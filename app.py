import streamlit as st
from meta_client import send_message_to_meta

# Load custom CSS
def load_css():
    with open("style.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

load_css()

st.set_page_config(page_title="Meta AI Chat", layout="centered")

st.markdown('<div class="meta-chat-box">', unsafe_allow_html=True)

st.title("🤖 Chat dengan Meta AI")

# Inisialisasi session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input (modern style)
prompt = st.chat_input("Ketik sesuatu...")

if prompt:
    st.session_state.chat_history.append(("user", prompt))

    try:
        response = send_message_to_meta(prompt)
        reply = response["data"]["xfb_silverstone_send_message"]["bot_response_message"]["content"]["message"]
        st.session_state.chat_history.append(("ai", reply))
    except Exception as e:
        st.session_state.chat_history.append(("ai", f"⚠️ Error: {e}"))

# Tampilkan chat history dengan gaya modern
for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(f'<div class="chat-box chat-user">🧑‍💻 {message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-box chat-bot">🤖 {message}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
