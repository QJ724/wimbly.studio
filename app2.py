import streamlit as st
import requests
import io
from PIL import Image

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Wimbly Studio", page_icon="🎨", layout="wide")

# --- RECUPERO LA CHIAVE SEGRETA ---
try:
    hf_token = st.secrets["HF_TOKEN"]
except:
    st.warning("⚠️ Chiave segreta non trovata. Inseriscila manualmente nella sidebar.")
    hf_token = None

# --- MENU MODELLI ---
MODELS = {
    "🚀 Flux Schnell": "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell",
    "🎨 Stable Diffusion XL": "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0",
    "👾 Animagine XL (Anime)": "https://router.huggingface.co/hf-inference/models/cagliostrolab/animagine-xl-3.1"
}

# --- MENU RISOLUZIONI (Trucco del Prompt) ---
# Invece di pixel, usiamo stringhe che aggiungiamo al prompt
ASPECT_RATIOS = {
    "Quadrato (1:1)": "",  # Default
    "Paesaggio (16:9)": " --ar 16:9",
    "Ritratto (9:16)": " --ar 9:16",
    "Standard (4:3)": " --ar 4:3"
}

# --- INTERFACCIA UTENTE ---
st.title("Wimbly Studio 🎨")
st.write("Crea immagini con l'Intelligenza Artificiale.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Pannello di Controllo")
    
    # 1. Scelta Modello
    selected_model_name = st.selectbox("Modello AI", list(MODELS.keys()))
    api_url = MODELS[selected_model_name]
    
    # 2. Scelta Formato
    selected_ratio_name = st.selectbox("Formato", list(ASPECT_RATIOS.keys()))
    ratio_suffix = ASPECT_RATIOS[selected_ratio_name]
    
    st.divider()
    if not hf_token:
        hf_token = st.text_input("Token HF", type="password")

# --- LOGICA DI CHIAMATA ---
def query_hugging_face(payload, token, url):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, headers=headers, json=payload)
    return response.content

# --- AREA CENTRALE ---
col1, col2 = st.columns([2, 1])

with col1:
    prompt_utente = st.text_area(
        "Descrivi la tua immaginazione:", 
        "Un astronauta che cavalca un cavallo su Marte, fotorealistico, 8k",
        height=150
    )
    
    generate_btn = st.button("✨ Genera Immagine", type="primary", use_container_width=True)

with col2:
    st.info(f"**Modello:** {selected_model_name}\n\n**Formato:** {selected_ratio_name}")

# --- ESECUZIONE ---
if generate_btn:
    if not hf_token:
        st.error("🛑 Manca il Token! Inseriscilo nei Secrets o nella barra laterale.")
    else:
        with st.spinner(f'Sto chiedendo a {selected_model_name} di disegnare...'):
            try:
                # TRUCCO: Uniamo il prompt dell'utente con il comando formato
                # Esempio: "Gatto blu" + " --ar 16:9"
                final_prompt = prompt_utente + ratio_suffix
                
                # Payload SEMPLIFICATO (Senza parametri che rompono l'API)
                payload = {
                    "inputs": final_prompt,
                }
                
                image_bytes = query_hugging_face(payload, hf_token, api_url)
                
                if b"error" in image_bytes:
                    st.error(f"Errore dal server: {image_bytes}")
                else:
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    st.image(image, caption=f"Generata con {selected_model_name}", use_container_width=True)
                    
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button(
                        label="⬇️ Scarica Immagine",
                        data=buf.getvalue(),
                        file_name="wimbly_art.png",
                        mime="image/png",
                        use_container_width=True
                    )
                    st.success("Fatto! 🚀")

            except Exception as e:
                st.error(f"Qualcosa è andato storto: {e}")