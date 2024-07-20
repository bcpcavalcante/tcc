## Importar as bibliotecas
import pandas as pd

## Carregar o arquivo csv
df2024 = pd.read_csv(r'c:\Repos\tcc-bruna\fonte.csv')
df2019 = pd.read_excel(r'C:\Repos\tcc-bruna\verificadoativos07-05-2019abr-2019.xlsx')

## Comparar a quantidade de servidores entre os dois dataframes, nas bibliotecas
df2024 = df2024.dropna(subset=['SETOR'])
df2019 = df2019.dropna(subset=['SETOR'])

## Vamos remover todas as observações que não possuem a substring ''BIBLIOTECA'' na coluna 'SETOR'
df_bibliotecas24 = df2024[df2024['SETOR'].str.contains('BIBLIOTECA')]
df_bibliotecas19 = df2019[df2019['SETOR'].str.contains('BIBLIOTECA')]

##Remover as linhas cuja variável 'SETOR' é BIBLIOTECA MUNICIPAL MARIO DE ANDRADE , BIBLIOTECA PUBLICA MUNICIPAL LOUIS BRAILLE, BIBLIOTECA PUBLICA MUNICIPAL SERGIO MILLIET, BIBLIOTECA JOAO CABRAL DE MELO NETO (CEU), BIBLIOTECA JORNALISTA ROBERTO MARINHO (CEU) e BIBLIOTECA RACHEL DE QUEIROZ (CEU)
excluir = [
    'BIBLIOTECA MUNICIPAL MARIO DE ANDRADE',
    'BIBLIOTECA PUBLICA MUNICIPAL LOUIS BRAILLE',
    'BIBLIOTECA PUBLICA MUNICIPAL SERGIO MILLIET',
    'BIBLIOTECA JOAO CABRAL DE MELO NETO',
    'BIBLIOTECA JORNALISTA ROBERTO MARINHO',
    'BIBLIOTECA RACHEL DE QUEIROZ'
]

pattern = '|'.join(excluir)

df_bibliotecas24 = df_bibliotecas24[~df_bibliotecas24['SETOR'].str.contains(pattern)]

df_bibliotecas19 = df_bibliotecas19[~df_bibliotecas19['SETOR'].str.contains(pattern)]

def comparar_data_exerc(df2024, df2019):
    ## Converter a coluna 'DATA_EXERCICIO' para datetime
    df2024['DATA_INICIO_EXERC'] = pd.to_datetime(df2024['DATA_INICIO_EXERC'], errors='coerce')
    df2019['DATA_INICIO_EXERC'] = pd.to_datetime(df2019['DATA_INICIO_EXERC'], errors='coerce')    
    ## Criar uma nova tabela com o nome do servidor e a data de exercício do df2024 e df2019. Caso o servidor não esteja presente no dataframe de 2024, a data de exercício será nula.
    df_data_exerc = pd.merge(df2024[['NOME', 'DATA_INICIO_EXERC']], df2019[['NOME', 'DATA_INICIO_EXERC']], on='NOME', how='left', suffixes=('_2024', '_2019'))

    return df_data_exerc

df_data_exerc_bibliotecas = comparar_data_exerc(df_bibliotecas24, df_bibliotecas19)

def identificando_consistencia_de_data_inic_exer(df_data_exerc):
    ## Identificar as mudanças
    df_data_exerc['CONSISTENTE'] = df_data_exerc['DATA_INICIO_EXERC_2024'] == df_data_exerc['DATA_INICIO_EXERC_2019']
    ## Filtrar as mudanças
    df_mudancas = df_data_exerc[df_data_exerc['CONSISTENTE'] == True]
    ## Selecionaremos todos os regis

    return df_data_exerc

df_incons = identificando_consistencia_de_data_inic_exer(df_data_exerc_bibliotecas)

def resolver_inconsistencias(df_incons):
    ## Analizaremos a tabela de inconsistências criando uma nova coluna "DATA_INICIO_EXERC" que será preenchida com o valor da coluna "DATA_INICIO_EXERC_2019" caso a coluna "CONSISTENTE" seja False e o valor da coluna "DATA_INICIO_EXERC_2024" não seja nulo. Nos casos em que a coluna "CONSISTENTE" seja False, e o valor da coluna "DATA_INICIO_EXERC_2019" seja nulo, a coluna "DATA_INICIO_EXERC" será preenchida com o valor da coluna "DATA_INICIO_EXERC_2024".

    df_incons['DATA_INICIO_EXERC'] = df_incons['DATA_INICIO_EXERC_2019']
    df_incons.loc[df_incons['DATA_INICIO_EXERC'].isnull(), 'DATA_INICIO_EXERC'] = df_incons['DATA_INICIO_EXERC_2024']

    ## Removeremos as colunas "DATA_INICIO_EXERC_2024", "DATA_INICIO_EXERC_2019" e "CONSISTENTE"
    df_incons = df_incons.drop(columns=['DATA_INICIO_EXERC_2024', 'DATA_INICIO_EXERC_2019', 'CONSISTENTE'])

    return df_incons
    
       

df_resolvido = resolver_inconsistencias(df_incons)

## Criaremos uma função que vai substituir os dados da coluna data de início de exercício do df2024 pelos dados resolvidos
def introduzir_dados_resolvidos(df_resolvido, df_bibliotecas24):
    ##Para cada observação da tabela de dados resolvidos, vamos substituir o valor da coluna "DATA_INICIO_EXERC" na tabela de df_bibliotecas24
    for i in df_resolvido.index:
        nome = df_resolvido.loc[i, 'NOME']
        df_bibliotecas24.loc[df_bibliotecas24['NOME'] == nome, 'DATA_INICIO_EXERC'] = df_resolvido.loc[i, 'DATA_INICIO_EXERC']
    ## Retornar a tabela de df_bibliotecas24
    
    return df_bibliotecas24

df_bibliotecas24_resolvido = introduzir_dados_resolvidos(df_resolvido, df_bibliotecas24)

## Criaremos uma função que vai identificar os servidores e servidoras que poderão se aposentar em 2024, para isso consideraremos as seguintes regras de transição (categoria pedágio): Para amnbos sexos, ter mais de 20 anos de serviço público. Para homens, ter mais de 60 anos de idade. Para mulheres, ter mais de 57 anos de idade.

def identificar_aposentadoria(df_bibliotecas24_resolvido):
    
    ## Criar uma nova coluna "IDADE_EM_2024" que será preenchida com a diferença entre o ano de 2024 e o ano de nascimento do servidor
    df_bibliotecas24_resolvido['IDADE_EM_2024'] = 2024 - df_bibliotecas24_resolvido['ANO_NASCIMENTO'].astype(int)
    ## Criar uma nova coluna "TEMPO_DE_SERVICO_EM_2024" que será preenchida com a diferença entre o ano de 2024 e o ano de início do exercício do servidor
    df_bibliotecas24_resolvido['TEMPO_DE_SERVICO_EM_2024'] = 2024 - df_bibliotecas24_resolvido['DATA_INICIO_EXERC'].dt.year
    ## Criar uma nova coluna "APTA_A_APOSENTAR" que será preenchida com True caso o servidor tenha mais de 20 anos de serviço público e mais de 60 anos de idade (homens) ou mais de 57 anos de idade (mulheres)
    df_bibliotecas24_resolvido['APTA_A_APOSENTAR'] = (df_bibliotecas24_resolvido['TEMPO_DE_SERVICO_EM_2024'] >= 20) & ((df_bibliotecas24_resolvido['IDADE_EM_2024'] >= 60) | ((df_bibliotecas24_resolvido['IDADE_EM_2024'] >= 57) & (df_bibliotecas24_resolvido['SEXO'] == 'F')))
    ## Filtrar as observações que são aptas a se aposentar
    df_aposentadoria = df_bibliotecas24_resolvido[df_bibliotecas24_resolvido['APTA_A_APOSENTAR'] == True]
    ## Retornar a tabela de df_aposentadoria
    return df_aposentadoria

df_aposentadoria = identificar_aposentadoria(df_bibliotecas24_resolvido)



##Mostrar as informações dos setores do ano de 2024 e 2019
def contar_servidores_por_setor(df, ano):
    setores_contagem = df['SETOR'].value_counts().reset_index()
    setores_contagem.columns = ['SETOR', 'QUANTIDADE']
    setores_contagem = setores_contagem.sort_values(by='QUANTIDADE', ascending=False)
    print(f'Quantidade de servidores por setor em {ano}:\n{setores_contagem}')
    return setores_contagem

setores_contagem_24 = contar_servidores_por_setor(df_bibliotecas24, 2024)
setores_contagem_19 = contar_servidores_por_setor(df_bibliotecas19, 2019)



##  Criaremos uma tabela comparativa entre os dois anos, mostrando a quantidade de servidores em cada setor em 2019 e 2024
comparativo = pd.merge(setores_contagem_19, setores_contagem_24, on='SETOR', how='outer')
comparativo.columns = ['SETOR', '2019', '2024']
comparativo = comparativo.fillna(0)
comparativo['2019'] = comparativo['2019'].astype(int)
comparativo['2024'] = comparativo['2024'].astype(int)
comparativo = comparativo.sort_values(by='2024', ascending=False)
# print(f'Comparativo entre 2019 e 2024:\n{comparativo}')

## Queremos uma tabela com o total de servidores em 2019 e 2024
total_2019 = setores_contagem_19['QUANTIDADE'].sum()
total_2024 = setores_contagem_24['QUANTIDADE'].sum()
# print(f'Total de servidores em 2019: {total_2019}')
# print(f'Total de servidores em 2024: {total_2024}')


## Criaremos uma função que gerará uma tabela com as colunas SETOR, QUANTIDADE_SERVIDORES, e QUANTIDADE_APTOS_A_APOSENTAR

def comparativo_aposentadoria(df_aposentadoria, setores_contagem_24):
    ## Criar uma nova tabela com o nome do setor, a quantidade de servidores em 2024 e a quantidade de servidores aptos a se aposentar em 2024
    df_aposentadoria_por_setor = pd.merge(setores_contagem_24, df_aposentadoria['SETOR'].value_counts().reset_index(), on='SETOR', how='left')
    df_aposentadoria_por_setor.columns = ['SETOR', 'QUANTIDADE_SERVIDORES', 'QUANTIDADE_APTOS_A_APOSENTAR']
    df_aposentadoria_por_setor = df_aposentadoria_por_setor.fillna(0)

    # Criar uma coluna com a subtração entre a quantidade de servidores e a quantidade de servidores aptos a se aposentar
    df_aposentadoria_por_setor['QUANTIDADE_NAO_APTOS_A_APOSENTAR'] = df_aposentadoria_por_setor['QUANTIDADE_SERVIDORES'] - df_aposentadoria_por_setor['QUANTIDADE_APTOS_A_APOSENTAR']
    
    # Transformar os valores float em int
    df_aposentadoria_por_setor['QUANTIDADE_SERVIDORES'] = df_aposentadoria_por_setor['QUANTIDADE_SERVIDORES'].astype(int)
    df_aposentadoria_por_setor['QUANTIDADE_APTOS_A_APOSENTAR'] = df_aposentadoria_por_setor['QUANTIDADE_APTOS_A_APOSENTAR'].astype(int)
    df_aposentadoria_por_setor['QUANTIDADE_NAO_APTOS_A_APOSENTAR'] = df_aposentadoria_por_setor['QUANTIDADE_NAO_APTOS_A_APOSENTAR'].astype(int)

    return df_aposentadoria_por_setor


df_aposentadoria_por_setor = comparativo_aposentadoria(df_aposentadoria, setores_contagem_24)

## Criaremos uma função que filtrará os servidores pelo valor da coluna CARGO_BASICO, retornando aqueles que contém a substring 'ANALISTA DE INFORMACOES CULTURA E DESPORTO' no nome do cargo, desses servidores, retornaremos os que possuem a coluna 'APTA_A_APOSENTAR' como False

def filtrar_analista(df_bibliotecas24_resolvido):
    ## Filtrar os servidores pelo valor da coluna CARGO_BASICO
    df_analista = df_bibliotecas24_resolvido[df_bibliotecas24_resolvido['CARGO_BASICO'].str.contains('ANALISTA DE INFORMACOES CULTURA E DESPORTO')]
    ## Filtrar os servidores que possuem a coluna 'APTA_A_APOSENTAR' como False
    df_analista_nao_apto = df_analista[df_analista['APTA_A_APOSENTAR'] == False]
    return df_analista_nao_apto

df_analista_nao_apto = filtrar_analista(df_bibliotecas24_resolvido)

##Criaremos uma função que gerará uma tabela com as colunas SETOR, QUANTIDADE_SERVIDORES, e QUANTIDADE_NAO_APTOS_A_APOSENTAR, considerando apenas os servidores analistas

def comparativo_aposentadoria_analista(df_analista_nao_apto):
    ## Criar uma nova tabela com o nome do setor, a quantidade de servidores em 2024 e a quantidade de servidores não aptos a se aposentar em 2024, se o número for zero, preencheremos com zero
    df_analista_nao_apto_por_setor = df_analista_nao_apto['SETOR'].value_counts().reset_index()
    df_analista_nao_apto_por_setor.columns = ['SETOR', 'QUANTIDADE_NAO_APTOS_A_APOSENTAR']
    df_analista_nao_apto_por_setor = pd.merge(setores_contagem_24, df_analista_nao_apto_por_setor, on='SETOR', how='left')
    df_analista_nao_apto_por_setor = df_analista_nao_apto_por_setor.fillna(0)
    df_analista_nao_apto_por_setor['QUANTIDADE_NAO_APTOS_A_APOSENTAR'] = df_analista_nao_apto_por_setor['QUANTIDADE_NAO_APTOS_A_APOSENTAR'].astype(int)
    
    

    return df_analista_nao_apto_por_setor

df_analista_nao_apto_por_setor = comparativo_aposentadoria_analista(df_analista_nao_apto)
df_analista_nao_apto_por_setor.head(10)




