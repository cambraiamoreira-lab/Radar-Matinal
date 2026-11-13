import streamlit as st
import requests
import json
from datetime import datetime

# ============================================
# 🎨 CONFIGURAÇÃO E DESIGN (Tema Radar)
# ============================================
st.set_page_config(
    page_title="Radar Matinal",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

COR_PRINCIPAL = "#1A252F"  # Azul Marinho
COR_DESTAQUE = "#F39C12"   # Laranja
COR_FUNDO = "#F4F6F7"

st.markdown(f"""
<style>
    .stApp {{ background-color: {COR_FUNDO}; }}
    .main .block-container {{
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        max-width: 600px;
        margin: 0 auto;
    }}
    h1, h2, h3 {{ color: {COR_PRINCIPAL}; font-weight: 700; text-align: center; }}
    .stButton>button {{
        background: {COR_DESTAQUE};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 1rem 2rem;
        font-weight: 700;
        font-size: 1.1rem;
        width: 100%;
    }}
    .info-box {{
        background: #e8f4f8;
        border-left: 4px solid #3498db;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>📡 Radar Matinal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#7f8c8d;'>Configure o seu resumo diário personalizado</p>", unsafe_allow_html=True)
st.markdown("---")

# ============================================
# 📝 FORMULÁRIO DE CONFIGURAÇÃO
# ============================================
with st.form("config_form"):
    st.markdown("### 👤 Seus Dados")
    nome = st.text_input("Seu Nome", placeholder="Ex: Sergio")
    telegram_user = st.text_input("Seu usuário do Telegram (sem o @)", placeholder="Ex: sergio123")
    
    st.markdown("### 🌤️ Localização")
    cidade = st.text_input("Sua Cidade (para o Clima)", placeholder="Ex: Sao Paulo", help="Use o nome da cidade em inglês ou português, sem acentos se possível.")
    
    st.markdown("### 📰 Escolha 3 Temas de Notícias")
    st.markdown("<div class='info-box'>💡 O sistema buscará a notícia mais recente e relevante de cada tema escolhido.</div>", unsafe_allow_html=True)
    
    temas_disponiveis = ["Política", "Tecnologia", "Economia", "Esportes", "Meio Ambiente", "Saúde", "Entretenimento"]
    temas_escolhidos = st.multiselect(
        "Selecione exatamente 3 temas:",
        temas_disponiveis,
        default=["Política", "Tecnologia", "Economia"]
    )
    
    st.markdown("### 🔢 Quantidade")
    qtd_noticias = st.radio("Quantas manchetes por tema?", [1, 3, 5], index=0, horizontal=True)
    
    st.markdown("---")
    enviado = st.form_submit_button("💾 SALVAR E TESTAR ENVIO NO TELEGRAM")
