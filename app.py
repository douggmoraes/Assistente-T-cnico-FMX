import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(page_title="Assistente Técnico", layout="wide", page_icon="🔧")

# Estilização CSS otimizada: cartões compactos, sem folgas e alinhados à esquerda
st.markdown("""
    <style>
    /* Expande a área útil da página na tela */
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
        max-width: 95% !important;
    }

    /* Regras visuais para todos os cartões */
    .card-box, .card-solucao, .card-recon, .card-display {
        padding: 10px 15px !important;
        border-radius: 6px !important;
        margin-bottom: 10px !important;
        width: 100% !important;
        text-align: left !important;
    }

    .card-box {
        background-color: #1e222a;
        border-left: 5px solid #4da6ff;
    }
    .card-solucao {
        background-color: #172b1d;
        border-left: 5px solid #28a745;
    }
    .card-recon {
        background-color: #2a2217;
        border-left: 5px solid #ffcc00;
    }
    .card-display {
        background-color: #2a1e17;
        border-left: 5px solid #ff9900;
    }

    /* Alinhamento à esquerda e espaçamentos internos enxutos */
    .card-box p, .card-solucao p, .card-recon p, .card-display p,
    .card-box div, .card-solucao div, .card-recon div, .card-display div {
        color: #ffffff !important;
        font-size: 15px !important;
        line-height: 1.4 !important;
        margin: 4px 0 0 0 !important;
        text-align: left !important;
        white-space: pre-wrap !important;
    }

    .card-box h4, .card-solucao h4, .card-recon h4, .card-display h4 {
        margin: 0 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        text-align: left !important;
    }

    .txt-display-ingles {
        color: #ffcc00 !important;
        font-size: 15px !important;
        font-weight: bold;
        font-family: monospace;
        background-color: #111111;
        padding: 2px 8px;
        border-radius: 4px;
        display: inline-block;
    }

    .txt-display-traducao {
        color: #66b3ff !important;
        font-size: 15px !important;
        font-weight: 500;
    }

    .stTextInput > div > div > input {
        font-size: 18px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔧 Assistente Técnico")
st.caption("Sistema de Consulta Rápida de Falhas e Manutenção")

# --- MENU SELETOR DE MANUAL ---
manual_selecionado = st.selectbox(
    "📚 Selecione o Manual de Consulta:",
    ["Manual FMX (Geral)", "Controladores Curtis (1232/1234/1236/1238)"]
)

# Define o arquivo com base na seleção
if manual_selecionado == "Manual FMX (Geral)":
    arquivo_excel = 'Manual_Perfeito.xlsx'
else:
    arquivo_excel = 'Manual_curtis.xlsx' if os.path.exists('Manual_curtis.xlsx') else 'Manual_Curtis.xlsx'

@st.cache_data
def carregar_dados(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        return pd.read_excel(caminho_arquivo).fillna("")
    return None

df_falhas = carregar_dados(arquivo_excel)

if df_falhas is not None:
    # Form para capturar botão ou ENTER
    with st.form(key="form_pesquisa", clear_on_submit=False):
        codigo_input = st.text_input("🔍 Digite o código da falha:", placeholder="Ex.: A1205, 1205 ou 14")
        btn_pesquisar = st.form_submit_button("🔎 Pesquisar Falha", use_container_width=True, type="primary")

    codigo = codigo_input.strip().upper()

    if btn_pesquisar and codigo:
        coluna_codigo = df_falhas.iloc[:, 0].astype(str).str.strip().str.upper()
        resultado = df_falhas[coluna_codigo == codigo]

        if not resultado.empty:
            st.toast(f"Falha localizada no {manual_selecionado}!", icon="✅")
            linha = resultado.iloc[0]
            
            def limpar_texto(texto):
                t = str(texto).strip()
                if t in ["...", "..", ".", "-", "mostrar", "Mostrar", "nan", "NaN"]:
                    return ""
                return t

            st.divider()

            # --- EXIBIÇÃO PARA O MANUAL FMX ---
            if manual_selecionado == "Manual FMX (Geral)":
                cod_exibido = limpar_texto(linha.iloc[0]) if limpar_texto(linha.iloc[0]) else codigo
                desc_exibida = limpar_texto(linha.iloc[1]) if limpar_texto(linha.iloc[1]) else "Não informada"
                causa_exibida = limpar_texto(linha.iloc[2]) if limpar_texto(linha.iloc[2]) else "Não informada"
                recon_exibido = limpar_texto(linha.iloc[4]) if len(linha) > 4 and limpar_texto(linha.iloc[4]) else "Não informado"
                solucao_exibida = limpar_texto(linha.iloc[5]) if len(linha) > 5 and limpar_texto(linha.iloc[5]) else ""
                display_exibido = limpar_texto(linha.iloc[6]) if len(linha) > 6 and limpar_texto(linha.iloc[6]) else ""

                st.subheader(f"📌 Nº da Falha: `{cod_exibido}`")

                st.markdown(f"""
                <div class="card-box">
                    <h4 style="color: #66b3ff;">📋 Descrição</h4>
                    <p>{desc_exibida}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="card-box">
                    <h4 style="color: #66b3ff;">🧩 Causa</h4>
                    <p>{causa_exibida}</p>
                </div>
                """, unsafe_allow_html=True)

                if solucao_exibida:
                    st.markdown(f"""
                    <div class="card-solucao">
                        <h4 style="color: #5cd65c;">🛠️ Resposta / Solução</h4>
                        <p>{solucao_exibida}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("ℹ️ **Resposta / Solução:** Sem solução específica cadastrada no manual para este código.")

                st.markdown(f"""
                <div class="card-recon">
                    <h4 style="color: #ffcc00;">🔄 Reconhecimento / Reset</h4>
                    <p>{recon_exibido}</p>
                </div>
                """, unsafe_allow_html=True)

                if display_exibido:
                    st.markdown(f"""
                    <div class="card-display">
                        <h4 style="color: #ffb366;">💻 Display / Mensagem IHM</h4>
                        <p><span class="txt-display-ingles">{display_exibido}</span></p>
                    </div>
                    """, unsafe_allow_html=True)

            # --- EXIBIÇÃO PARA O MANUAL CURTIS ---
            else:
                cod_exibido = limpar_texto(linha.iloc[0]) if limpar_texto(linha.iloc[0]) else codigo
                display_raw = limpar_texto(linha.iloc[1]) if len(linha) > 1 else ""
                consequencia_curtis = limpar_texto(linha.iloc[2]) if len(linha) > 2 and limpar_texto(linha.iloc[2]) else "Não informada"
                causa_curtis = limpar_texto(linha.iloc[3]) if len(linha) > 3 and limpar_texto(linha.iloc[3]) else "Não informada"
                verificacao_curtis = limpar_texto(linha.iloc[4]) if len(linha) > 4 and limpar_texto(linha.iloc[4]) else "Não informada"
                correcao_curtis = limpar_texto(linha.iloc[5]) if len(linha) > 5 and limpar_texto(linha.iloc[5]) else ""

                st.subheader(f"📌 Código da Falha: `{cod_exibido}`")

                if display_raw:
                    partes_display = display_raw.split("\n\n")
                    texto_ingles = partes_display[0].strip()
                    texto_traducao = partes_display[1].strip() if len(partes_display) > 1 else ""

                    html_display = f'<span class="txt-display-ingles">{texto_ingles}</span>'
                    if texto_traducao:
                        html_display += f'<div class="txt-display-traducao">🌐 <b>{texto_traducao}</b></div>'

                    st.markdown(f"""
                    <div class="card-display">
                        <h4 style="color: #ffb366;">💻 Texto no Display do Handset / Tradução</h4>
                        {html_display}
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="card-box">
                    <h4 style="color: #66b3ff;">⚠️ A Falha Provoca (Consequência)</h4>
                    <p>{consequencia_curtis}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="card-box">
                    <h4 style="color: #66b3ff;">🧩 Causas Possíveis</h4>
                    <p>{causa_curtis}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="card-recon">
                    <h4 style="color: #ffcc00;">🔍 Razão / Verificação</h4>
                    <p>{verificacao_curtis}</p>
                </div>
                """, unsafe_allow_html=True)

                if correcao_curtis:
                    st.markdown(f"""
                    <div class="card-solucao">
                        <h4 style="color: #5cd65c;">🛠️ Correção / Ação Recomendada</h4>
                        <p>{correcao_curtis}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("ℹ️ **Correção:** Sem instrução direta cadastrada nesta linha do manual.")

        else:
            st.error(f"❌ O código **'{codigo}'** não foi encontrado no {manual_selecionado}.")
else:
    st.error(f"🚨 Arquivo '{arquivo_excel}' não foi localizado na pasta do projeto.")
