import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Conexão com Google Sheets usando secrets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = st.secrets["gcp_service_account"]
credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
gc = gspread.authorize(credentials)

# Tentar abrir a planilha
try:
    sh = gc.open("Radar de Problemas SGS")
    worksheet = sh.sheet1
except Exception as e:
    st.error("Erro ao conectar à planilha: verifique se o nome está correto e se a conta de serviço tem acesso.")
    st.stop()

# Login simples
def autenticar():
    with st.sidebar:
        st.subheader("Login")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if usuario == "Jaime" and senha == "12345@.":
                st.session_state["logado"] = True
            else:
                st.error("Usuário ou senha inválido.")

if "logado" not in st.session_state:
    autenticar()
else:
    st.title("Radar de Problemas SGS")

    # Formulário
    with st.form("formulario"):
        nome = st.text_input("Responsável pela abertura")
        setor = st.selectbox("Área", ["Qualidade", "SAC", "Projetos", "Engenharia", "RH", "Controladoria"])
        tipo = st.selectbox("Tipo do problema", ["Processo fora do combinado", "Processo não estabelecido", "Falta/Falha de comunicação"])
        descricao = st.text_area("Descrição")
        status = st.selectbox("Status", ["Aberta", "Em análise", "Concluída"])
        prazo = st.date_input("Prazo")
        enviado = st.form_submit_button("Registrar")

        if enviado:
            worksheet.append_row([nome, setor, tipo, descricao, status, str(prazo)])
            st.success("Registro enviado com sucesso!")

    # Tabela
    st.subheader("Registros existentes")
    dados = worksheet.get_all_records()
    df = pd.DataFrame(dados)
    st.dataframe(df)