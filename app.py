import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Assistente Técnico FMX", layout="wide")

st.title("🔧 Assistente Técnico FMX")
st.write("Sistema de Consulta de Falhas")

excel_perfeito = 'Manual_Perfeito.xlsx'

if os.path.exists(excel_perfeito):
    # Lê a planilha com todas as falhas
    df_falhas = pd.read_excel(excel_perfeito).fillna("")

    codigo = st.text_input("Digite o código da falha", placeholder="Ex.: A1205").strip().upper()

    if st.button("Pesquisar"):
        if codigo:
            # Busca qualquer código na planilha inteira
            resultado = df_falhas[df_falhas['Código'].astype(str).str.strip().str.upper() == codigo]

            if not resultado.empty:
                st.success("Código localizado")
                linha = resultado.iloc[0]
                
                # Função inteligente para limpar lixos visuais do Excel original
                def limpar_texto(texto):
                    t = str(texto).strip()
                    if t in ["...", "..", ".", "-", "mostrar", "Mostrar"]:
                        return ""
                    return t

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Código")
                    st.write(limpar_texto(linha.iloc[0]) if limpar_texto(linha.iloc[0]) else codigo)

                    st.subheader("Descrição")
                    st.write(limpar_texto(linha.iloc[1]) if limpar_texto(linha.iloc[1]) else "Não informada")

                    st.subheader("Causa")
                    st.write(limpar_texto(linha.iloc[2]) if limpar_texto(linha.iloc[2]) else "Não informada")

                with col2:
                    st.subheader("Consequência")
                    st.write(limpar_texto(linha.iloc[3]) if limpar_texto(linha.iloc[3]) else "Não informada")

                    st.subheader("Reconhecimento")
                    st.write(limpar_texto(linha.iloc[4]) if limpar_texto(linha.iloc[4]) else "Não informado")

                    # FORÇA O TÍTULO FIXO "SOLUÇÃO" (Lê a 6ª coluna da sua planilha)
                    st.subheader("Solução")
                    texto_solucao = limpar_texto(linha.iloc[5]) if len(linha) > 5 else ""
                    if not texto_solucao:
                        st.write("Sem solução cadastrada para esta falha no Excel")
                    else:
                        st.write(texto_solucao)

                    # FORÇA O TÍTULO FIXO "DISPLAY" (Lê a 7ª coluna da sua planilha)
                    st.subheader("Display")
                    texto_display = limpar_texto(linha.iloc[6]) if len(linha) > 6 else ""
                    st.write(texto_display if texto_display else "Não informado")
            else:
                st.error(f"O código '{codigo}' não foi encontrado na planilha Manual_Perfeito.xlsx.")
else:
    st.error("Erro: O arquivo 'Manual_Perfeito.xlsx' não foi encontrado nesta pasta.")