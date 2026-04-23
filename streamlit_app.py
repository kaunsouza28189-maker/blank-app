import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistema ARIELO")
st.title("Sistema de Estoque - ARIELO")

if 'usuario' not in st.session_state:
    st.session_state.usuario = ""

if not st.session_state.usuario:
    nome = st.text_input("Por favor, digite seu nome:")
    if nome:
        st.session_state.usuario = nome
        st.rerun()
else:
    st.write(f"Bem-vindo, {st.session_state.usuario}!")

    file_id = '1ltaHWxs36rhlT27kMuM6BWNOyTjLCH1Q'
    url = f'https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx'

    @st.cache_data
    def carregar_dados(url_planilha):
        return pd.read_excel(url_planilha, skiprows=1)

    try:
        df = carregar_dados(url)
        cod_busca = st.text_input("Qual o Cod. Referência você deseja consultar:").strip()

        if cod_busca:
            df['Cód. Referência'] = df['Cód. Referência'].astype(str)
            resultado = df[df['Cód. Referência'] == cod_busca]

            if resultado.empty:
                st.error("Código não cadastrado!!!")
            else:
                descricao = resultado['Descrição'].iloc[0]
                qtd_total = pd.to_numeric(resultado['Qtd. Disponível'], errors='coerce').sum()

                st.success("Código encontrado!")
                st.metric(label="Total Disponível", value=f"{int(qtd_total)} unidades")
                st.info(f"Produto: {descricao}")
                
                with st.expander("Ver detalhes por lote"):
                    st.write(resultado[['Nº Lote', 'Dt. Produção', 'Qtd. Disponível', 'Status']])

    except Exception as e:
        st.error(f"Erro ao acessar a base de dados: {e}")

    if st.button("Sair / Trocar Usuário"):
        st.session_state.usuario = ""
        st.rerun()