import streamlit as st
from meta_client import send_message_to_meta

st.set_page_config(page_title="Meta AI Chat", layout="centered")

st.markdown('<link rel="stylesheet" href="style.css">', unsafe_allow_html=True)
st.markdown('<div class="meta-chat-box">', unsafe_allow_html=True)

st.title("🤖 Chat dengan Meta AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

prompt = st.chat_input("Ketik pesan...")

if prompt:
    st.session_state.chat_history.append(("user", prompt))
    
    try:
        response = send_message_to_meta(prompt)
        reply = response["data"]["xfb_silverstone_send_message"]["bot_response_message"]["content"]["message"]
        st.session_state.chat_history.append(("ai", reply))
    except Exception as e:
        st.session_state.chat_history.append(("ai", f"⚠️ Error: {e}"))

# Tampilkan history
for role, message in st.session_state.chat_history:
    bubble_class = "meta-bubble-user" if role == "user" else "meta-bubble-ai"
    st.markdown(f'<div class="{bubble_class}">{message}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
