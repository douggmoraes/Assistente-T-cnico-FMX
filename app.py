import streamlit as st
import pandas as pd
import os
import urllib.parse

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

    /* Botão do WhatsApp customizado */
    .btn-whatsapp {
        background-color: #25d366;
        color: white !important;
        padding: 8px 16px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 5px;
        margin-bottom: 15px;
    }
    .btn-whatsapp:hover {
        background-color: #1eb954;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔧 Assistente Técnico")
st.caption("Sistema de Consulta Rápida de Falhas e Manutenção")

# --- INICIALIZAÇÃO DO HISTÓRICO DE BUSCAS NA SESSÃO ---
if 'historico_buscas' not in st.session_state:
    st.session_state.historico_buscas = []

def adicionar_ao_historico(termo):
    termo_limpo = termo.strip().upper()
    if termo_limpo and termo_limpo not in st.session_state.historico_buscas:
        st.session_state.historico_buscas.insert(0, termo_limpo)
        st.session_state.historico_buscas = st.session_state.historico_buscas[:5]

# --- MENU SELETOR DE MANUAL ---
manual_selecionado = st.selectbox(
    "📚 Selecione o Manual de Consulta:",
    ["Manual FMX (Geral)", "Controladores Curtis (1232/1234/1236/1238)"]
)

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
    # --- HISTÓRICO DE BUSCAS RECENTES ---
    if st.session_state.historico_buscas:
        st.write("⏱️ **Buscas Recentes:**")
        cols_hist = st.columns(len(st.session_state.historico_buscas) + 1)
        for idx, item in enumerate(st.session_state.historico_buscas):
            if cols_hist[idx].button(f"🔍 {item}", key=f"hist_{idx}"):
                st.session_state['busca_input'] = item
        if cols_hist[-1].button("🗑️ Limpar", key="limpar_hist"):
            st.session_state.historico_buscas = []
            st.rerun()

    # --- OPÇÃO DE MODO DE BUSCA ---
    tipo_busca = st.radio(
        "Modo de Pesquisa:",
        ["Por Código da Falha (Ex.: 14)", "Por Palavra-Chave / Sintoma (Ex.: Temperatura, Encoder, Curto)"],
        horizontal=True
    )

    valor_padrao = st.session_state.get('busca_input', '')

    with st.form(key="form_pesquisa", clear_on_submit=False):
        codigo_input = st.text_input("🔍 Digite a sua busca:", value=valor_padrao, placeholder="Ex.: 14 ou Temperatura")
        btn_pesquisar = st.form_submit_button("🔎 Pesquisar Falha", use_container_width=True, type="primary")

    termo_busca = codigo_input.strip().upper()

    # Função utilitária de renderização de um resultado
    def renderizar_resultado(linha, codigo_ref):
        def limpar_texto(texto):
            t = str(texto).strip()
            if t in ["...", "..", ".", "-", "mostrar", "Mostrar", "nan", "NaN"]:
                return ""
            return t

        st.divider()

        # VARIÁVEIS PARA GERAR MENSAGEM DO WHATSAPP
        texto_para_whatsapp = ""

        # EXIBIÇÃO PARA MANUAL FMX
        if manual_selecionado == "Manual FMX (Geral)":
            cod_exibido = limpar_texto(linha.iloc[0]) if limpar_texto(linha.iloc[0]) else codigo_ref
            desc_exibida = limpar_texto(linha.iloc[1]) if limpar_texto(linha.iloc[1]) else "Não informada"
            causa_exibida = limpar_texto(linha.iloc[2]) if limpar_texto(linha.iloc[2]) else "Não informada"
            recon_exibido = limpar_texto(linha.iloc[4]) if len(linha) > 4 and limpar_texto(linha.iloc[4]) else "Não informado"
            solucao_exibida = limpar_texto(linha.iloc[5]) if len(linha) > 5 and limpar_texto(linha.iloc[5]) else "Não cadastrada"
            display_exibido = limpar_texto(linha.iloc[6]) if len(linha) > 6 and limpar_texto(linha.iloc[6]) else ""

            st.subheader(f"📌 Nº da Falha: `{cod_exibido}`")

            # Monta texto do WhatsApp
            texto_para_whatsapp = f"*ASSISTENTE TÉCNICO - DIAGNÓSTICO*\n" \
                                  f"*Manual:* {manual_selecionado}\n" \
                                  f"*Falha:* {cod_exibido}\n" \
                                  f"*Descrição:* {desc_exibida}\n" \
                                  f"*Causa:* {causa_exibida}\n" \
                                  f"*Solução:* {solucao_exibida}"

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

            if solucao_exibida and solucao_exibida != "Não cadastrada":
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

        # EXIBIÇÃO PARA MANUAL CURTIS
        else:
            cod_exibido = limpar_texto(linha.iloc[0]) if limpar_texto(linha.iloc[0]) else codigo_ref
            display_raw = limpar_texto(linha.iloc[1]) if len(linha) > 1 else ""
            consequencia_curtis = limpar_texto(linha.iloc[2]) if len(linha) > 2 and limpar_texto(linha.iloc[2]) else "Não informada"
            causa_curtis = limpar_texto(linha.iloc[3]) if len(linha) > 3 and limpar_texto(linha.iloc[3]) else "Não informada"
            verificacao_curtis = limpar_texto(linha.iloc[4]) if len(linha) > 4 and limpar_texto(linha.iloc[4]) else "Não informada"
            correcao_curtis = limpar_texto(linha.iloc[5]) if len(linha) > 5 and limpar_texto(linha.iloc[5]) else "Não informada"

            st.subheader(f"📌 Código da Falha: `{cod_exibido}`")

            # Monta texto do WhatsApp
            texto_para_whatsapp = f"*ASSISTENTE TÉCNICO - DIAGNÓSTICO*\n" \
                                  f"*Manual:* {manual_selecionado}\n" \
                                  f"*Código:* {cod_exibido}\n" \
                                  f"*Display:* {display_raw}\n" \
                                  f"*Causa:* {causa_curtis}\n" \
                                  f"*Correção:* {correcao_curtis}"

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

            if correcao_curtis and correcao_curtis != "Não informada":
                st.markdown(f"""
                <div class="card-solucao">
                    <h4 style="color: #5cd65c;">🛠️ Correção / Ação Recomendada</h4>
                    <p>{correcao_curtis}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ **Correção:** Sem instrução direta cadastrada nesta linha do manual.")

        # --- ÁREA DE COMPARTILHAMENTO E CÓPIA ---
        st.markdown("---")
        col_wsp, col_code = st.columns([1, 2])

        with col_wsp:
            texto_url = urllib.parse.quote(texto_para_whatsapp)
            link_whatsapp = f"https://api.whatsapp.com/send?text={texto_url}"
            st.markdown(f'<a href="{link_whatsapp}" target="_blank" class="btn-whatsapp">📲 Compartilhar no WhatsApp</a>', unsafe_allow_html=True)

        with col_code:
            st.caption("📋 **Copiar diagnóstico completo:**")
            st.code(texto_para_whatsapp, language="text")

    if btn_pesquisar and termo_busca:
        adicionar_ao_historico(termo_busca)

        # MODO 1: BUSCA POR CÓDIGO
        if "Código" in tipo_busca:
            coluna_codigo = df_falhas.iloc[:, 0].astype(str).str.strip().str.upper()
            resultado = df_falhas[coluna_codigo == termo_busca]

            if not resultado.empty:
                st.toast(f"Falha localizada no {manual_selecionado}!", icon="✅")
                renderizar_resultado(resultado.iloc[0], termo_busca)
            else:
                st.error(f"❌ O código **'{termo_busca}'** não foi encontrado no {manual_selecionado}.")

        # MODO 2: BUSCA POR PALAVRA-CHAVE EM TODAS AS COLUNAS
        else:
            mascara = df_falhas.astype(str).apply(
                lambda col: col.str.contains(termo_busca, case=False, na=False)
            ).any(axis=1)

            resultados = df_falhas[mascara]

            if not resultados.empty:
                qtd = len(resultados)
                st.success(f"🔍 Encontrada(s) **{qtd}** ocorrência(s) para o termo **'{termo_busca}'**.")

                if qtd == 1:
                    renderizar_resultado(resultados.iloc[0], termo_busca)
                else:
                    opcoes_codigos = [f"Código: {r.iloc[0]} - {str(r.iloc[1])[:40]}..." for _, r in resultados.iterrows()]
                    escolha = st.selectbox("Selecione qual falha deseja visualizar:", opcoes_codigos)
                    
                    idx_selecionado = opcoes_codigos.index(escolha)
                    renderizar_resultado(resultados.iloc[idx_selecionado], termo_busca)
            else:
                st.error(f"❌ Nenhuma falha contendo a palavra **'{termo_busca}'** foi encontrada.")

else:
    st.error(f"🚨 Arquivo '{arquivo_excel}' não foi localizado na pasta do projeto.")
