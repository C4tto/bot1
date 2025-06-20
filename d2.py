import streamlit as st
import requests

# config
st.set_page_config(page_title="Chatbot con Groq", layout="centered")
st.title("Chatbot con Groq")

# api_key
api_key = "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"

# modelos
modelos = [
    "llama3-8b-8192",
    "llama3-70b-8192",
]

modelo_seleccionado = st.selectbox("Elegí el modelo de Groq", modelos_disponibles)

# historial
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Escribí tu mensaje")

if st.button("Enviar") and api_key and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    print(f"[Usuario]: {user_input}")

    # req 
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": modelo_seleccionado,
            "messages": st.session_state.chat_history,
            "temperature": 0.7
        }
    )

    # respuesta
    if response.status_code == 200:
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        print(f"[Bot]: {reply}")
    else:
        st.error("Error en la respuesta")
        print(f"[Error ]: {response.status_code} - {response.text}")

# Mostrar historial en pantalla
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**Yo:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
