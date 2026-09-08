# 🔧 Assistente Técnico 
essa aplicaçao saiu da necessidade de consultar manuais de orientaçoes de falhas de equipamentos 
nesse caso de manuais de empilhadeiras

O **Assistente Técnico ** é uma aplicação web desenvolvida em Python e Streamlit para consulta rápida e diagnóstico de falhas técnicas com base em manuais operacionais (`Manual_Perfeito.xlsx`). 

O sistema foi desenhado para proporcionar uma interface responsiva, de alto contraste e fácil leitura para técnicos em campo e operadores.

---

## 🚀 Funcionalidades

- **Consulta Rápida por Código:** Busca instantânea de códigos de falha e erros operacionais.
- **Estrutura Sequencial de Diagnóstico:** Exibição clara e organizada na seguinte ordem de prioridade:
  1. 📌 **Número da Falha**
  2. 📋 **Descrição da Falha**
  3. 🧩 **Provável Causa**
  4. 🛠️ **Resposta / Solução Recomendada**
  5. 🔄 **Procedimento de Reconhecimento / Reset**
  6. 💻 **Mensagem no Display / IHM**
- **Interface Responsiva & Embeddable:** Otimizada para celulares, tablets e integração via `iframe` em portais HTML internos.
- **Cache de Dados Integrado:** Leitura otimizada da planilha Excel utilizando `@st.cache_data` para alta performance.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Framework Web:** [Streamlit](https://streamlit.io/)
- **Manipulação de Dados:** [pandas](https://pandas.pydata.org/)
- **Leitura de Excel:** `openpyxl`
- **Hospedagem:** Streamlit Community Cloud
- **Integração Web:** HTML5 / CSS3 (`iframe`)

---

## 📁 Estrutura do Repositório

```text
├── .streamlit/
│   └── config.toml          # Configurações de segurança e permissão de embed (X-Frame-Options)
├── app.py                   # Código principal da aplicação Streamlit
├── Manual_Perfeito.xlsx     # Base de dados em Excel contendo os códigos e soluções
├── requirements.txt         # Lista de dependências Python para o servidor na nuvem
├── index.html               # Portal web em HTML para incorporação da ferramenta
└── README.md                # Documentação do projeto 
