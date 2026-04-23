import streamlit as st
import pandas as pd

# CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="Sistema ARIELO")
st.title("Sistema de Estoque - ARIELO")

# GESTÃO DE USUÁRIO
if 'usuario' not in st.session_state:
    st.session_state.usuario = ""

if not st.session_state.usuario:
    nome = st.text_input("Por favor, digite seu nome:")
    if nome:
        st.session_state.usuario = nome
        st.rerun()
else:
    st.write(f"Bem-vindo, {st.session_state.usuario}!")

    # LINK DA PLANILHA (O ID que você usou antes)
    file_id = '1ltaHWxs36rhlT27kMuM6BWNOyTjLCH1Q'
    url = f'https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx'

    @st.cache_data
    def carregar_dados(url_planilha):
        # O skiprows=1 pula a primeira linha de título da sua planilha
        return pd.read_excel(url_planilha, skiprows=1)

    try:
        df = carregar_dados(url)
        cod_busca = st.text_input("Qual o Cod. Referencia voce deseja consultar:").strip()

        if cod_busca:
            # Converte a coluna para texto para evitar erro de busca
            df['Cód. Referência'] = df['Cód. Referência'].astype(str)
            resultado = df[df['Cód. Referência'] == cod_busca]

            if resultado.empty:
                st.error("Codigo nao cadastrado!!!")
            else:
                # Pega a primeira descrição e soma a quantidade disponível
                descricao = resultado['Descrição'].iloc[0]
                qtd_total = pd.to_numeric(resultado['Qtd. Disponível'], errors='coerce').sum()

                st.success("Codigo encontrado!")
                st.metric(label="Total Disponivel", value=f"{int(qtd_total)} unidades")
                st.info(f"Produto: {descricao}")
                
                with st.expander("Ver detalhes por lote"):
                    st.write(resultado[['Nº Lote', 'Dt. Produção', 'Qtd. Disponível', 'Status']])

    except Exception as e:
        st.error(f"Erro ao acessar a base de dados: {e}")

    if st.button("Sair / Trocar Usuario"):
        st.session_state.usuario = ""
        st.rerun()