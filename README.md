# Dashboard Avançado de Análise de Vendas de Carros

Uma visão analítica, estatisticamente higienizada e interativa sobre o inventário de anúncios de veículos baseada em dados reais do mercado norte-americano.

---

##  Índice
* [Sobre o Projeto](#-sobre-o-projeto)
* [Tratamento de Dados (Data Cleaning)](#️-tratamento-de-dados-data-cleaning)
* [Funcionalidades e Visualizações](#-funcionalidades-e-visualizações)
* [Tecnologias Utilizadas](#️-tecnologias-utilizadas)
* [Como Rodar o Projeto](#-como-rodar-o-projeto)
* [Critérios de Avaliação Atendidos](#-critérios-de-avaliação-atendidos)
* [Autor](#-autor)
* [Próximos Passos](#-próximos-passos)

---

## Sobre o Projeto
Este projeto consiste em uma aplicação web interativa desenvolvida com **Streamlit**, cujo objetivo principal é fornecer insights visuais de negócio para análise de frotas e anúncios de veículos comerciais e particulares. O pipeline inclui ingestão de dados brutos (`vehicles_us.csv`).

---

## Tratamento de Dados (Data Cleaning)
A base de dados continha diversas inconsistências e valores nulos (escondidos sob a string `"None"` ou células vazias). Seguindo critérios de boas práticas, apliquei imputações estatísticas para não enviesar os resultados:

- [x] **Variações de Nulos:** Strings textuais como `'None'`, `'none'`, e `'NaN'` foram convertidas para nulos reais (`pd.NA`).
- [x] **Coluna `is_4wd`:** Valores ausentes foram interpretados como falta de tração integral e preenchidos com `0` (Falso).
- [x] **Coluna `model_year`:** Valores nulos foram substituídos pela **mediana do ano do modelo agrupada por veículo (`model`)**, preservando a coerência cronológica do fabricante.
- [x] **Coluna `odometer`:** Quilometragens ausentes foram tratadas utilizando a **mediana de quilometragem agrupada pelo ano do modelo do carro** (veículos mais antigos tendem a ter mais rodagem).
- [x] **Coluna `cylinders`:** Cilindradas ausentes foram preenchidas usando a **moda (valor mais frequente) baseada no modelo específico do veículo**.
- [x] **Coluna `paint_color`:** Cores nulas foram padronizadas como `"unknown"` (desconhecido).

---

## Funcionalidades e Visualizações
O painel permite a ativação dinâmica de múltiplos módulos analíticos por meio de checkboxes na barra lateral:
* **Métricas Gerais:** Exibição em tempo real do volume de anúncios, preço médio geral e quilometragem média do inventário.
* **Distribuição de Quilometragem:** Gráfico de histograma indicando a dispersão de rodagem da frota.
* **Preço vs Quilometragem:** Gráfico de dispersão evidenciando a desvalorização do veículo de acordo com o uso.
* **Preço Médio por Tipo:** Gráfico de barras ordenado revelando quais categorias (SUV, Pickup, Truck) retêm maior valor de mercado.
* **Visão por Condição e Combustível:** Gráfico de caixa (Boxplot) cruzando o estado de conservação do veículo com os tipos de combustível disponíveis.

---

## Tecnologias Utilizadas
1. **Python 3.14+**
2. **Streamlit** (Interface e renderização da aplicação web)
3. **Pandas** (Tratamento e manipulação de DataFrames)
4. **Plotly Express** (Gráficos interativos e dinâmicos)

---

## Como Rodar o Projeto

### Pré-requisitos
Certifique-se de possuir o Python instalado em sua máquina.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/philldmg/sprint_5_projeto.git](https://github.com/philldmg/sprint_5_projeto.git)
   cd sprint_5_projeto

2. **Crie eative o ambiente virtual:**
    ```bash
    python -m venv .venv

    #No Windows (PowerShell):
    .\.venv\Scripts\Activate.ps1

    #No Linux/Mac:
    source .venv/bin/activate

3. **Instale as dependências listadas:**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt

4. **Execute a aplicação localmente:**
    ```bash
    python -m streamlit run app.py