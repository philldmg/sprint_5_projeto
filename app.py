import os
import pandas as pd
import streamlit as st
import plotly.express as px

# --- Configuração de Caminho Direto na Raiz ---
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, 'vehicles_us.csv')

# Lendo o conjunto de dados
car_data = pd.read_csv(csv_path)

# --- TRATAMENTO DE DADOS SÊNIOR (Data Cleaning Completo) ---

# 1. Forçar todas as variações de strings nulas para o tipo nulo real do pandas
for col in car_data.columns:
    if car_data[col].dtype == 'object':
        car_data[col] = car_data[col].astype(str).str.strip()
        car_data[col] = car_data[col].replace(['None', 'none', 'NaN', 'nan', '<NA>'], pd.NA)

# 2. Tratar coluna de tração integral (is_4wd): nulos significam que não é 4x4 (0)
car_data['is_4wd'] = car_data['is_4wd'].fillna(0).astype(int)

# 3. Tratar anos de modelo nulos usando a mediana por modelo do carro
car_data['model_year'] = pd.to_numeric(car_data['model_year'], errors='coerce')
car_data['model_year'] = car_data.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))
car_data['model_year'] = car_data['model_year'].fillna(car_data['model_year'].median()).astype(int)

# 4. Tratar quilometragem (odometer) usando a mediana baseada no ano do modelo
car_data['odometer'] = pd.to_numeric(car_data['odometer'], errors='coerce')
car_data['odometer'] = car_data.groupby('model_year')['odometer'].transform(lambda x: x.fillna(x.median()))
car_data['odometer'] = car_data['odometer'].fillna(car_data['odometer'].median()).astype(int)

# 5. Tratar cilindros (cylinders) usando a moda (valor mais frequente) por modelo de veículo
car_data['cylinders'] = pd.to_numeric(car_data['cylinders'], errors='coerce')
car_data['cylinders'] = car_data.groupby('model')['cylinders'].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else 6))
car_data['cylinders'] = car_data['cylinders'].astype(int)

# 6. Tratar colunas de texto categórico (paint_color) preenchendo com "unknown"
car_data['paint_color'] = car_data['paint_color'].fillna('unknown')

# 7. Garantir consistência da coluna de preço
car_data['price'] = pd.to_numeric(car_data['price'], errors='coerce')

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title="Dashboard de Veículos Profissional", layout="wide")

# --- Cabeçalho Principal ---
st.title('Dashboard Avançado de Análise de Vendas de Carros')
st.markdown("Uma visão analítica, higienizada e interativa sobre o inventário de anúncios de veículos.")
st.markdown("---")

# --- Painel de Métricas Rápidas ---
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
    
    show_histogram = st.checkbox('Analisar Distribuição de Quilometragem (Módulo 1)', value=True)
    show_scatter = st.checkbox('Analisar Preço vs Quilometragem (Módulo 2)', value=True)
    show_type_bar = st.checkbox('Analisar Preço Médio por Tipo de Veículo', value=False)
    show_condition_box = st.checkbox('Analisar Preço por Condição e Combustível', value=False)

with col_direita:
    st.subheader("Amostra Higienizada da Base de Dados")
    st.write("Cilindros e cores corrigidos para consistência estatística e visual:")
    st.dataframe(car_data.head(100), height=220)

st.markdown("---")

# --- Renderização Dinâmica dos Gráficos em Grid Seguro ---
st.subheader("Gráficos e Insights Visuais")

if any([show_histogram, show_scatter, show_type_bar, show_condition_box]):
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
        
    # Grid Avançado sem estouro de índice
    for i in range(0, len(ativos), 2):
        cols = st.columns(2)
        with cols[0]:
            st.plotly_chart(ativos[i], use_container_width=True)
        if i + 1 < len(ativos):
            with cols[1]:
                st.plotly_chart(ativos[i+1], use_container_width=True)
else:
    st.warning("Selecione pelo menos uma configuração de visualização no menu à esquerda para renderizar os gráficos.")