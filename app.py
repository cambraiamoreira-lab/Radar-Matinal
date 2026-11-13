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
    # ============================================
# ⚙️ LÓGICA DE PROCESSAMENTO E ENVIO
# ============================================
if enviado:
    # 1. Validação
    if len(temas_escolhidos) != 3:
        st.error("⚠️ Por favor, selecione EXATAMENTE 3 temas.")
    elif not nome or not telegram_user or not cidade:
        st.error("⚠️ Por favor, preencha todos os campos.")
    else:
        st.info("⏳ Processando sua configuração e buscando informações...")
        
        # SEU TOKEN DO TELEGRAM (Substitua pelo seu token real aqui!)
        TELEGRAM_TOKEN = "6162605645:AAH-1bhEwZ1dydIGBZMUu7IWFMvXmmFkN6Q"
        TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        
        # --- FUNÇÃO PARA BUSCAR CLIMA (API Gratuita wttr.in) ---
        def obter_clima(cidade):
            try:
                url = f"https://wttr.in/{cidade.replace(' ', '+')}?format=j1"
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    temp = data['current_condition'][0]['temp_C']
                    desc = data['current_condition'][0]['weatherDesc'][0]['value']
                    return f"🌤️ *Clima em {cidade.title()}*: {temp}°C, {desc}"
                return "🌤️ Clima: Não foi possível obter os dados agora."
            except:
                return "🌤️ Clima: Indisponível no momento."

        # --- FUNÇÃO PARA BUSCAR NOTÍCIAS (Usando Jina AI Reader + RSS, 100% Grátis e sem chave) ---
        def obter_noticia(tema):
            # Mapeamento de temas para feeds RSS confiáveis
            feeds = {
                "Política": "https://g1.globo.com/politica/rss2.xml",
                "Tecnologia": "https://g1.globo.com/tecnologia/rss2.xml",
                "Economia": "https://g1.globo.com/economia/rss2.xml",
                "Esportes": "https://ge.globo.com/rss/ge/",
                "Meio Ambiente": "https://g1.globo.com/natureza/rss2.xml",
                "Saúde": "https://g1.globo.com/saude/rss2.xml",
                "Entretenimento": "https://g1.globo.com/pop-arte/rss2.xml"
            }
            
            rss_url = feeds.get(tema, feeds["Tecnologia"])
            # Jina AI converte RSS em texto limpo gratuitamente
            jina_url = f"https://r.jina.ai/{rss_url}"
            
            try:
                resp = requests.get(jina_url, timeout=10)
                if resp.status_code == 200:
                    texto = resp.text
                    # Pega as primeiras linhas que contêm os títulos (simplificado)
                    linhas = [l.strip() for l in texto.split('\n') if l.strip() and not l.startswith('http')]
                    if len(linhas) > 2:
                        # A primeira linha costuma ser o título do feed, a segunda a primeira notícia
                        return f"📰 *{tema}*: {linhas[1]}"
                return f"📰 *{tema}*: Sem notícias recentes."
            except:
                return f"📰 *{tema}*: Indisponível no momento."

        # 2. Montar a Mensagem
        mensagem = f"☀️ *Bom dia, {nome}!*\n\nAqui está o seu *Radar Matinal* de {datetime.now().strftime('%d/%m')}:\n\n"
        mensagem += obter_clima(cidade) + "\n\n"
        mensagem += "━━━━━━━━━━━━━━━━━━\n\n"
        
        for tema in temas_escolhidos:
            mensagem += obter_noticia(tema) + "\n\n"
            
        mensagem += "━━━━━━━━━━━━━━━━━━\n"
        mensagem += "_Configurado via Radar Matinal App_"

        # 3. Enviar para o Telegram
        payload = {
            "chat_id": f"@{telegram_user}",
            "text": mensagem,
            "parse_mode": "Markdown"
        }
        
        try:
            resposta = requests.post(TELEGRAM_URL, json=payload, timeout=10)
            if resposta.json().get("ok"):
                st.success("✅ SUCESSO! A mensagem foi enviada para o seu Telegram.")
                st.markdown("📱 *Verifique seu celular agora!*")
            else:
                st.error(f"❌ Erro no Telegram: {resposta.json().get('description')}")
                st.info("💡 Dica: Verifique se você digitou o usuário do Telegram corretamente e se iniciou uma conversa com o bot @newscambraiabot.")
        except Exception as e:
            st.error(f"❌ Erro de conexão: {e}")

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align:center; color:#95A5A6; font-size:0.8rem;'>Radar Matinal © 2026</p>", unsafe_allow_html=True)
