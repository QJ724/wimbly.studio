import streamlit as st
import requests
import io
from PIL import Image
import time

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Nano Banana Flux", page_icon="🍌")

st.title("🍌 Nano Banana (Flux Edition)")
st.write("Genera immagini incredibili usando il modello FLUX.1 tramite Hugging Face.")

# --- BARRA LATERALE ---
with st.sidebar:
    st.header("Chiavi di Accesso")
    # Qui incollerai il token hf_... che hai usato prima
    hf_token = st.text_input("Hugging Face Token", type="password")
    
    st.divider()
    st.info("💡 Usa il token che hai creato su huggingface.co")

# --- AREA PRINCIPALE ---
prompt = st.text_area(
    "Descrivi la tua immagine:", 
    "Un astronauta che cavalca un cavallo su Marte, fotorealistico, 8k",
    height=100
)

# URL del nuovo server (Router)
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

def query_hugging_face(payload, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

# --- BOTTONE GENERAZIONE ---
if st.button("✨ Genera con Flux", type="primary"):
    if not hf_token:
        st.error("🛑 Inserisci il Token Hugging Face nella barra laterale!")
    else:
        with st.spinner('Flux sta disegnando... (attendi qualche secondo)'):
            try:
                # Chiamata all'API
                image_bytes = query_hugging_face({"inputs": prompt}, hf_token)
                
                # Gestione Errori del server
                if b"error" in image_bytes:
                    st.error(f"Errore dal server: {image_bytes}")
                else:
                    # Mostra l'immagine
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption="Generata con Flux.1 Schnell", use_container_width=True)
                    
                    # Bottone Download
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button(
                        label="⬇️ Scarica Immagine",
                        data=buf.getvalue(),
                        file_name="flux_banana.png",
                        mime="image/png"
                    )
                    st.success("Fatto! 🍌")

            except Exception as e:
                st.error(f"Qualcosa è andato storto: {e}")