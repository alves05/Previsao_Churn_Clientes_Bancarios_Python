# Previsão de Churn para clientes bancários
Prever a rotatividade de clientes num banco.

### Dicionário dos dados:

- RowNumber—corresponde ao número do registo (linha) e não tem qualquer efeito na saída.
- CustomerId—contém valores aleatórios e não tem qualquer efeito sobre a saída do cliente do banco.
- Surname—o apelido de um cliente não tem qualquer impacto na sua decisão de abandonar o banco.
- CreditScore—pode ter um efeito na rotatividade dos clientes, uma vez que um cliente com uma pontuação de crédito mais elevada tem menos probabilidades de abandonar o banco.
- Geography—a localização de um cliente pode afetar a sua decisão de abandonar o banco.
- Gender—é interessante explorar se o género desempenha um papel na saída de um cliente do banco.
- Age—este facto é certamente relevante, uma vez que os clientes mais idosos têm menos probabilidades de abandonar o seu banco do que os mais jovens.
- Tenure—refere-se ao número de anos em que o cliente é cliente do banco. Normalmente, os clientes mais antigos são mais fiéis e têm menos probabilidades de abandonar um banco.
- Balance—é também um excelente indicador da rotatividade dos clientes, uma vez que as pessoas com um saldo mais elevado nas suas contas têm menos probabilidades de abandonar o banco do que as que têm saldos mais baixos.
- NumOfProducts—refere-se ao número de produtos que um cliente adquiriu através do banco.
- HasCrCard—indica se um cliente tem ou não um cartão de crédito. Esta coluna também é relevante, uma vez que as pessoas com um cartão de crédito têm menos probabilidades de abandonar o banco.
- IsActiveMember—os clientes activos têm menos probabilidades de abandonar o banco.
- EstimatedSalary—tal como acontece com o equilíbrio, as pessoas com salários mais baixos têm mais probabilidades de abandonar o banco do que as pessoas com salários mais elevados.
- Exited—utilizado como objetivo. 1 se o cliente abandonou o banco durante um determinado período ou 0 se não o fez.

Como sabemos, é muito mais dispendioso angariar um novo cliente do que manter um cliente existente.

É vantajoso para os bancos saber o que leva um cliente a tomar a decisão de abandonar a empresa.

A prevenção do churn permite às empresas desenvolver programas de fidelização e campanhas de retenção para manter o maior número possível de clientes.


link https://www.kaggle.com/datasets/mathchi/churn-for-bank-customers

### Ferramentas

- Python
- Streamlit

### Passos:

1. Obejtivo
2. Problema de negócio
3. Obtenção dos dados
4. Análise exploratória
5. Tratamento dos valores faltantes
6. Pré-processamento dos dados
7. validação cruzada dos modelos de machine learning
	1. Naive Bayes
	2. Random Forest
	3. KNN
	4. Regression Logistic
	5. SVM
	6. Redes Neurais Artificiais
8. Teste de hipóteses
9. Tunning hiperparâmetros
10. Treinamento do modelo
11. Implementação em aplicação web
