import os
import pandas as pd
import streamlit as st
import plotly.express as px

# --- Configuração de Caminho Baseado na Raiz do Critério ---
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, 'vehicles_us.csv')

# Lendo o conjunto de dados
car_data = pd.read_csv(csv_path)

# --- Configuração da Página ---
st.set_page_config(page_title="Dashboard de Veículos", layout="wide")

# --- Cabeçalho Principal (Critério: Pelo menos um cabeçalho com texto) ---
st.title('Dashboard de Análise de Vendas de Carros')
st.markdown("Uma visão analítica e interativa sobre o inventário de anúncios de veículos.")
st.markdown("---")

# --- Painel de Métricas Rápidas ---
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="Total de Anúncios", value=f"{len(car_data):,}")
with col_m2:
    st.metric(label="Preço Médio", value=f"${car_data['price'].mean():,.2f}")
with col_m3:
    st.metric(label="Quilometragem Média", value=f"{car_data['odometer'].mean():,.0f} mi")

st.markdown("---")

# --- Painel de Configurações (Critério: Pelo menos um botão ou caixa de seleção) ---
col_esquerda, col_direita = st.columns([1, 2])

with col_esquerda:
    st.subheader("Configurações de Visualização")
    st.write("Marque as opções para renderizar as análises:")
    show_histogram = st.checkbox('Analisar Distribuição de Quilometragem', value=True)
    show_scatter = st.checkbox('Analisar Preço vs Quilometragem', value=True)

with col_direita:
    st.subheader("Visão Geral dos Dados")
    st.dataframe(car_data.head(100), height=200)

st.markdown("---")

# --- Seção Dinâmica de Gráficos (Critérios: Pelo menos 1 histograma e 1 gráfico de dispersão) ---
if show_histogram or show_scatter:
    st.subheader("Gráficos e Análises Visuais")
    
    if show_histogram and show_scatter:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig_hist = px.histogram(car_data, x="odometer", title="Distribuição da Quilometragem", color_discrete_sequence=['#228B22'])
            st.plotly_chart(fig_hist, use_container_width=True)
        with col_g2:
            fig_scatter = px.scatter(car_data, x="odometer", y="price", title="Preço vs Quilometragem", opacity=0.5)
            st.plotly_chart(fig_scatter, use_container_width=True)
            
    elif show_histogram:
        fig_hist = px.histogram(car_data, x="odometer", title="Distribuição da Quilometragem", color_discrete_sequence=['#228B22'])
        st.plotly_chart(fig_hist, use_container_width=True)
        
    elif show_scatter:
        fig_scatter = px.scatter(car_data, x="odometer", y="price", title="Preço vs Quilometragem", opacity=0.5)
        st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.warning("Use o painel de configurações para selecionar ao menos um gráfico para exibição.")