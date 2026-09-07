import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(page_title="Assistente Técnico FMX", layout="wide", page_icon="🔧")

# Estilização CSS com cores bem definidas e textos brancos de alto contraste
st.markdown("""
    <style>
    .card-box {
        background-color: #1e222a;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4da6ff;
        margin-bottom: 20px;
        color: #ffffff !important;
    }
    .card-solucao {
        background-color: #172b1d;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin-bottom: 20px;
        color: #ffffff !important;
    }
    .card-recon {
        background-color: #2a2217;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ffcc00;
        margin-bottom: 20px;
        color: #ffffff !important;
    }
    .card-display {
        background-color: #2a1e17;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff9900;
        margin-bottom: 20px;
        color: #ffffff !important;
    }
    
    .card-box p, .card-solucao p, .card-recon p, .card-display p,
    .card-box span, .card-solucao span, .card-recon span, .card-display span {
        color: #ffffff !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    
    .card-display code {
        color: #ffcc00 !important;
        font-size: 16px !important;
        font-weight: bold;
    }
    .stTextInput > div > div > input {
        font-size: 18px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔧 Assistente Técnico FMX")
st.caption("Sistema de Consulta Rápida de Falhas e Manutenção")

excel_perfeito = 'Manual_Perfeito.xlsx'

@st.cache_data
def carregar_dados():
    if os.path.exists(excel_perfeito):
        return pd.read_excel(excel_perfeito).fillna("")
    return None

df_falhas = carregar_dados()

if df_falhas is not None:
    codigo = st.text_input("🔍 Digite o código da falha:", placeholder="Ex.: A1205 ou 1205").strip().upper()

    if st.button("🔎 Pesquisar Falha", use_container_width=True, type="primary"):
        if codigo:
            resultado = df_falhas[df_falhas['Código'].astype(str).str.strip().str.upper() == codigo]

            if not resultado.empty:
                st.toast("Falha localizada com sucesso!", icon="✅")
                linha = resultado.iloc[0]
                
                def limpar_texto(texto):
                    t = str(texto).strip()
                    if t in ["...", "..", ".", "-", "mostrar", "Mostrar", "nan", "NaN"]:
                        return ""
                    return t

                cod_exibido = limpar_texto(linha.iloc[0]) if limpar_texto(linha.iloc[0]) else codigo
                desc_exibida = limpar_texto(linha.iloc[1]) if limpar_texto(linha.iloc[1]) else "Não informada"
                causa_exibida = limpar_texto(linha.iloc[2]) if limpar_texto(linha.iloc[2]) else "Não informada"
                recon_exibido = limpar_texto(linha.iloc[4]) if len(linha) > 4 and limpar_texto(linha.iloc[4]) else "Não informado"
                solucao_exibida = limpar_texto(linha.iloc[5]) if len(linha) > 5 and limpar_texto(linha.iloc[5]) else ""
                display_exibido = limpar_texto(linha.iloc[6]) if len(linha) > 6 and limpar_texto(linha.iloc[6]) else ""

                st.divider()

                # 1. NÚMERO DA FALHA
                st.subheader(f"📌 Nº da Falha: `{cod_exibido}`")

                # 2. DESCRIÇÃO
                st.markdown(f"""
                <div class="card-box">
                    <h4 style="color: #66b3ff; margin-top:0;">📋 Descrição</h4>
                    <p>{desc_exibida}</p>
                </div>
                """, unsafe_allow_html=True)

                # 3. CAUSA
                st.markdown(f"""
                <div class="card-box">
                    <h4 style="color: #66b3ff; margin-top:0;">🧩 Causa</h4>
                    <p>{causa_exibida}</p>
                </div>
                """, unsafe_allow_html=True)

                # 4. RESPOSTA / SOLUÇÃO
                if solucao_exibida:
                    st.markdown(f"""
                    <div class="card-solucao">
                        <h4 style="color: #5cd65c; margin-top:0;">🛠️ Resposta / Solução</h4>
                        <p>{solucao_exibida}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("ℹ️ **Resposta / Solução:** Sem solução específica cadastrada no manual para este código.")

                # 5. RECONHECIMENTO
                st.markdown(f"""
                <div class="card-recon">
                    <h4 style="color: #ffcc00; margin-top:0;">🔄 Reconhecimento / Reset</h4>
                    <p>{recon_exibido}</p>
                </div>
                """, unsafe_allow_html=True)

                # 6. DISPLAY
                if display_exibido:
                    st.markdown(f"""
                    <div class="card-display">
                        <h4 style="color: #ffb366; margin-top:0;">💻 Display / Mensagem IHM</h4>
                        <p><code>{display_exibido}</code></p>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                st.error(f"❌ O código **'{codigo}'** não foi encontrado na base de dados do manual.")
        else:
            st.warning("⚠️ Por favor, digite um código de falha antes de pesquisar.")
else:
    st.error("🚨 Arquivo 'Manual_Perfeito.xlsx' não localizado na pasta do projeto.")