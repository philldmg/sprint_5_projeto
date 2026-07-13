import os
import pandas as pd
import streamlit as st
import plotly.express as px

# --- Configuração de Caminho Direto na Raiz ---
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, 'vehicles_us.csv')

# Lendo o conjunto de dados
car_data = pd.read_csv(csv_path)

# --- TRATAMENTO DE DADOS SÊNIOR (Data Cleaning) ---
# 1. Padronizar strings "None" ou "none" para valores nulos reais (NaN)
car_data = car_data.replace(['None', 'none'], pd.NA)

# 2. Tratar coluna de tração integral (is_4wd): nulos significam que não é 4x4 (0)
car_data['is_4wd'] = car_data['is_4wd'].fillna(0).astype(int)

# 3. Tratar anos de modelo nulos usando a mediana por modelo do carro
car_data['model_year'] = pd.to_numeric(car_data['model_year'], errors='coerce')
car_data['model_year'] = car_data.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))
# Caso algum modelo ainda fique nulo (sem histórico), preenche com a mediana geral
car_data['model_year'] = car_data['model_year'].fillna(car_data['model_year'].median()).astype(int)

# 4. Tratar quilometragem (odometer) usando a mediana baseada no ano do modelo
car_data['odometer'] = pd.to_numeric(car_data['odometer'], errors='coerce')
car_data['odometer'] = car_data.groupby('model_year')['odometer'].transform(lambda x: x.fillna(x.median()))
# Caso reste algum nulo por ano raro, preenche com a mediana geral
car_data['odometer'] = car_data['odometer'].fillna(car_data['odometer'].median())

# Converter colunas de preço para numérico garantindo consistência
car_data['price'] = pd.to_numeric(car_data['price'], errors='coerce')

# --- Configuração da Página ---
st.set_page_config(page_title="Dashboard de Veículos Profissional", layout="wide")

# --- Cabeçalho Principal ---
st.title('Dashboard Avançado de Análise de Vendas de Carros')
st.markdown("Uma visão analítica, higienizada e interativa sobre o inventário de anúncios de veículos.")
st.markdown("---")

# --- Painel de Métricas Rápidas (Dados Tratados) ---
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="Total de Anúncios Analisados", value=f"{len(car_data):,}")
with col_m2:
    st.metric(label="Preço Médio de Mercado", value=f"${car_data['price'].mean():,.2f}")
with col_m3:
    st.metric(label="Quilometragem Média Real", value=f"{car_data['odometer'].mean():,.0f} mi")

st.markdown("---")

# --- Layout Lateral de Configurações ---
col_esquerda, col_direita = st.columns([1, 2])

with col_esquerda:
    st.subheader("Filtros e Configurações")
    st.write("Marque as análises que deseja exibir no painel principal:")
    
    # Critérios Base de Avaliação
    show_histogram = st.checkbox('Analisar Distribuição de Quilometragem (Módulo 1)', value=True)
    show_scatter = st.checkbox('Analisar Preço vs Quilometragem (Módulo 2)', value=True)
    
    # Novas Configurações Avançadas de Negócio
    show_type_bar = st.checkbox('Analisar Preço Médio por Tipo de Veículo', value=False)
    show_condition_box = st.checkbox('Analisar Preço por Condição e Combustível', value=False)

with col_direita:
    st.subheader("Amostra Limpa da Base de Dados")
    st.write("Os valores ausentes foram tratados estatisticamente por agrupamento:")
    st.dataframe(car_data.head(100), height=220)

st.markdown("---")

# --- Renderização Dinâmica dos Gráficos ---
st.subheader("Gráficos e Insights Visuais")

# Layout em grid de duas colunas para otimizar espaço se múltiplos gráficos estiverem ativos
if any([show_histogram, show_scatter, show_type_bar, show_condition_box]):
    
    # Criar uma lista de gráficos ativos para organizar na tela
    ativos = []
    
    if show_histogram:
        fig_hist = px.histogram(car_data, x="odometer", title="Distribuição de Quilometragem (Sem Nulos)", color_discrete_sequence=['#228B22'])
        ativos.append(fig_hist)
        
    if show_scatter:
        fig_scatter = px.scatter(car_data, x="odometer", y="price", title="Preço vs Quilometragem", opacity=0.4, color_discrete_sequence=['#1f77b4'])
        ativos.append(fig_scatter)
        
    if show_type_bar:
        df_price_type = car_data.groupby('type')['price'].mean().reset_index().sort_values(by='price', ascending=False)
        fig_bar = px.bar(df_price_type, x='type', y='price', title='Preço Médio por Tipo de Veículo', labels={'price':'Preço Médio ($)', 'type':'Tipo'}, color='price', color_continuous_scale='Viridis')
        ativos.append(fig_bar)
        
    if show_condition_box:
        fig_box = px.box(car_data, x='condition', y='price', color='fuel', title='Distribuição de Preço por Condição e Combustível', category_orders={"condition": ["new", "like new", "excellent", "good", "fair", "salvage"]})
        ativos.append(fig_box)
        
    # Distribui os gráficos selecionados de 2 em 2 colunas de forma organizada
    for i in range(0, len(ativos), i+2):
        cols = st.columns(2)
        if i < len(ativos):
            cols[0].plotly_chart(ativos[i], use_container_width=True)
        if i + 1 < len(ativos):
            cols[1].plotly_chart(ativos[i+1], use_container_width=True)
            
else:
    st.warning("Selecione pelo menos uma configuração de visualização no menu à esquerda para renderizar os gráficos.")