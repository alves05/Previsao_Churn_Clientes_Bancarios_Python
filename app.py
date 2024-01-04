import pickle

import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def base_dados():
    """Carrega a base de dados."""
    dados = pd.read_csv('./dados/churn.csv')
    return dados


def modelo_ml():
    """Carrega o modelo de previção de churn."""
    modelo = pickle.load(open('./modelo/modelo_previsao_churn.sav', 'rb'))
    return modelo


def processamento_dados(dados):
    """Modela a base de dados para aplicação do modelo de ML."""

    # Removendo atributos que não são relevantes para previsão
    df = dados.drop(
        columns=['RowNumber', 'CustomerId', 'Surname', 'Exited'], axis=True
    )

    # Processando variáveis categoricas
    var_cat = [
        'Geography',
        'Gender',
        'NumOfProducts',
        'HasCrCard',
        'IsActiveMember',
    ]
    one_hot = make_column_transformer(
        (OneHotEncoder(handle_unknown='ignore'), var_cat),
        remainder='passthrough',
    )
    df_final = one_hot.fit_transform(df)
    df_final = pd.DataFrame(df_final, columns=one_hot.get_feature_names_out())

    # Variáveis numéricas
    var_num = [
        'remainder__CreditScore',
        'remainder__Age',
        'remainder__Tenure',
        'remainder__Balance',
        'remainder__EstimatedSalary',
    ]
    scaler = StandardScaler()
    df_final[var_num] = scaler.fit_transform(df_final[var_num])

    return df_final


def previsao_probabilidade(dados):
    """Faz a previsão da probabilidade de churn da base de dados usando o modelo de ML."""
    modelo = modelo_ml()
    dados_previsao = processamento_dados(dados)
    probabilidade = modelo.predict_proba(dados_previsao)
    df_probabilidade = pd.DataFrame({'ID Cliente': dados['CustomerId']})
    df_probabilidade['Probabilidade'] = probabilidade[:, 1] * 100

    return df_probabilidade


def main():
    st.set_page_config(page_title='Análise de Churn', page_icon='🔄')
    st.markdown(
        "<h3 style='text-align: center; font-family: Verdana'>Análise e Monitoramento dos Clientes</h3>",
        unsafe_allow_html=True,
    )
    st.header('', divider='gray')
    st.sidebar.image('./img/outros/logo.png', use_column_width='always')
    st.sidebar.markdown(
        "<h3 style='text-align: center; font-family: Verdana'>Filtros:</h3>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown('')

    # Definindo colunas dos dados
    colunas = [
        'CustomerId',
        'Gender',
        'Geography',
        'Age',
        'CreditScore',
        'NumOfProducts',
        'Tenure',
        'IsActiveMember',
    ]
    dados = base_dados()

    # Aplicando modelo
    probabilidade = previsao_probabilidade(dados)

    # Tratando os dados da base
    tabela = dados[colunas]
    tabela['Churn %'] = probabilidade['Probabilidade'].astype(float).round(2)
    tabela['CustomerId'] = tabela['CustomerId'].astype(str)
    tabela['IsActiveMember'] = tabela['IsActiveMember'].replace(
        [0, 1], ['Ativo', 'Não Ativo']
    )
    tabela['Gender'] = tabela['Gender'].replace(
        ['Female', 'Male'], ['Feminino', 'Masculino']
    )
    tabela['Geography'] = tabela['Geography'].replace(
        ['France', 'Spain', 'Germany'], ['França', 'Espanha', 'Alemanha']
    )
    tabela = tabela.rename(
        columns={
            'CustomerId': 'ID Cliente',
            'Gender': 'Gênero',
            'Geography': 'País',
            'Age': 'Idade',
            'CreditScore': 'Score',
            'NumOfProducts': 'Produtos',
            'Tenure': 'Tempo',
            'IsActiveMember': 'Atividade',
        }
    )

    # Configurando filtros
    nivel = st.sidebar.slider('Probabilidade de Churn %:', 50, 100, 75)
    idade_min, idade_max = st.sidebar.select_slider(
        'Faixa de Etária (anos):',
        options=[18, 20, 30, 40, 50, 60, 70, 80, 92],
        value=[18, 92],
    )
    tempo_min, tempo_max = st.sidebar.select_slider(
        'Tempo como Cliente (anos):',
        options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        value=[0, 10],
    )
    quantidade_min, quantidade_max = st.sidebar.select_slider(
        'Quantidade de Produtos:', options=[1, 2, 3, 4], value=[1, 4]
    )
    cl1, cl2 = st.sidebar.columns(2)
    genero = cl1.radio('Gênero:', ['Feminino', 'Masculino', 'Todos'], index=2)
    pais = cl2.radio(
        'País:', ['Alemanha', 'Espanha', 'França', 'Todos'], index=3
    )
    atividade = st.sidebar.radio(
        'Atividade dos Clientes:', ['Ativo', 'Não Ativo', 'Todos'], index=2
    )

    for indice, linha in tabela.iterrows():
        if linha['Churn %'] > nivel:
            tabela.at[indice, 'Status'] = '🔴'
        elif linha['Churn %'] < 50:
            tabela.at[indice, 'Status'] = '🟢'
        else:
            tabela.at[indice, 'Status'] = '🟡'

    if genero != 'Todos':
        tabela = tabela[tabela['Gênero'] == genero]

    if pais != 'Todos':
        tabela = tabela[tabela['País'] == pais]

    if atividade != 'Todos':
        tabela = tabela[tabela['Atividade'] == atividade]

    tabela = tabela[
        (tabela['Idade'] >= idade_min) & (tabela['Idade'] <= idade_max)
    ]
    tabela = tabela[
        (tabela['Tempo'] >= tempo_min) & (tabela['Tempo'] <= tempo_max)
    ]
    tabela = tabela[
        (tabela['Produtos'] >= quantidade_min)
        & (tabela['Produtos'] <= quantidade_max)
    ]

    # Plot da tabela
    st.markdown('')
    st.markdown(
        "<h6 style='text-align: center; font-family: Verdana'>Tabela de Monitoramento dos Clientes com Probabilidade de Churn</h6>",
        unsafe_allow_html=True,
    )
    st.dataframe(tabela, width=850, height=350)
    st.write('🔴: Em Churn |', '🟡: Risco de Churn |', '🟢: Sem Risco de Churn')
    st.header('', divider='gray')

    # Análise
    st.markdown('')
    st.markdown(
        "<h5 style='text-align: center; font-family: Verdana'>Distribuição e Taxa de Probabilidade de Churn</h5>",
        unsafe_allow_html=True,
    )
    st.header('', divider='gray')

    # Configurando gráficos
    total_status = tabela.groupby('Status').size().reset_index(name='Contagem')
    label_mapping = {
        '🔴': 'Em Churn',
        '🟡': 'Risco de Churn',
        '🟢': 'Sem Risco de Churn',
    }
    total_status['Status'] = total_status['Status'].map(label_mapping)

    # Gráfico de barra
    barra = px.bar(
        total_status,
        x='Status',
        y='Contagem',
        width=500,
        color='Status',
        color_discrete_map={
            'Em Churn': '#ff8d89',
            'Risco de Churn': '#ffd589',
            'Sem Risco de Churn': '#8efaab',
        },
        text='Contagem',
    )
    barra.update_traces(
        textfont=dict(size=14, family='Verdana', color='black')
    )
    barra.update_layout(
        title='Distribuição de Probabilidade de Churn', title_x=0.1
    )

    # Gráfico de pizza
    pizza = px.pie(
        tabela,
        names='Status',
        color='Status',
        hole=0.5,
        color_discrete_map={'🟢': '#8efaab', '🟡': '#ffd589', '🔴': '#ff8d89'},
        width=270,
    )
    pizza.update_traces(
        textfont=dict(size=14, family='Verdana', color='black')
    )
    pizza.update_layout(
        showlegend=False, title='Taxa de Probabilidade de Churn', title_x=0.01
    )

    # Plot dos gráficos
    col1, col3 = st.columns([2.2, 1])
    col1.plotly_chart(barra)
    col3.plotly_chart(pizza)
    st.header('', divider='gray')
    st.caption('Relatório versão 1.0')


if __name__ == '__main__':
    main()
