import streamlit as st
import requests
import json
import uuid

st.set_page_config(page_title="Grivaniellovst AI Chat", layout="centered")
st.title("Grivaniellovst AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan semua pesan sebelumnya
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Prompt input
prompt = st.chat_input("Tulis sesuatu ke Grivaniellovst AI...")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Cookie dan token dari HAR capture
    doc_id = "24044662075146124"
    fb_dtsg = "NAfuqEblknvzAMBJvNDBEUtboLvq0SHdzWVozZMzgeiAvqnejEBglMA:23:1751695315"
    lsd = "hPoIHnyz9ZfMrW4cX2jesM"
    cookie = (
        "datr=rL9oaJzebjnBq_ipQINw3-WU; "
        "ps_l=1; ps_n=1; wd=1920x469; "
        "abra_csrf=SJB6Q39TgF15LqVAV2r5V8; "
        "abra_sess=Fsy7/rjN2rMCFi4YDmJSRjdLOVltNk1jWjVnFqb/xYYNAA=="
    )

    # Payload utama
    variables = {
        "message": {"sensitive_string_value": prompt},
        "externalConversationId": "92cb9611-112b-4559-a586-72911cc621da",
        "offlineThreadingId": str(uuid.uuid4().int)[:19],
        "threadSessionId": "d8e2cdad-da24-4f9e-845d-d8444fc434fe",
        "entrypoint": "KADABRA__PERMALINK__THREAD_VIEW",
        "selectedModel": "BASIC_OPTION",
        "attachments": [],
        "includeSpace": False,
        "server_timestamps": True
    }

    multipart_data = {
        "fb_api_caller_class": (None, "RelayModern"),
        "fb_api_req_friendly_name": (None, "useKadabraSendMessageMutation"),
        "doc_id": (None, doc_id),
        "server_timestamps": (None, "true"),
        "variables": (None, json.dumps(variables))
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-FB-LSD": lsd,
        "Cookie": cookie,
        "Accept": "*/*"
    }

    url = f"https://www.meta.ai/api/graphql/?fb_dtsg={fb_dtsg}&jazoest=25875&lsd={lsd}"

    with st.chat_message("assistant"):
        ph = st.empty()
        collected_texts = []

        try:
            with requests.post(url, headers=headers, files=multipart_data, stream=True, timeout=60) as resp:
                for line in resp.iter_lines(decode_unicode=True):
                    if not line or not line.strip().startswith("{"):
                        continue
                    try:
                        data = json.loads(line)

                        # Ambil agent_steps (stream)
                        steps = []
                        edges = (
                            data.get("data", {})
                            .get("xfb_silverstone_send_message", {})
                            .get("agent_stream", {})
                            .get("edges", [])
                        )
                        if edges:
                            for edge in edges:
                                steps += edge.get("node", {}).get("bot_response_message", {}).get("content", {}).get("agent_steps", [])
                        else:
                            steps = (
                                data.get("data", {})
                                .get("node", {})
                                .get("bot_response_message", {})
                                .get("content", {})
                                .get("agent_steps", [])
                            )

                        for step in steps:
                            for part in step.get("composed_text", {}).get("content", []):
                                txt = part.get("text", "")
                                if txt:
                                    collected_texts.append(txt.strip())
                    except Exception:
                        continue

        except Exception as e:
            ph.markdown(f"❌ Error koneksi: {e}")
            st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {e}"})
            st.stop()

        # ✅ Ambil satu hasil akhir yang paling lengkap
        final = ""
        max_len = 0
        for t in reversed(collected_texts):
            if len(t) >= max_len:
                final = t
                max_len = len(t)

        if final:
            ph.markdown(final)
            st.session_state.messages.append({"role": "assistant", "content": final})
        else:
            ph.markdown("❌ Meta AI tidak membalas.")
            st.session_state.messages.append({"role": "assistant", "content": "❌ Meta AI tidak membalas."})
