## Importando as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt

## Carregando os arquivos para o ambiente
def carregar_dados():
    df2024 = pd.read_csv(r'C:\Repos\tcc-bruna\fonte.csv')
    df2019 = pd.read_excel(r'C:\Repos\tcc-bruna\verificadoativos07-05-2019abr-2019.xlsx')
    return df2024, df2019

## Preparando os dados para iniciar a analise
def preparar_dados(df, colunas_desnecessarias, setores_ignorados):
    ## Remover as observações que não possuem a variável 'SETOR'
    df = df.dropna(subset=['SETOR'])
    
    ## Remover as variáveis que não serão utilizadas
    colunas_a_remover = [col for col in colunas_desnecessarias if col in df.columns]
    df = df.drop(columns=colunas_a_remover)   

    ## Vamos remover todas as observações que não possuem a substring ''BIBLIOTECA'' na coluna 'SETOR'
    df = df[df['SETOR'].str.contains('BIBLIOTECA')]
    
    ## Remover as observações que não serão analisadas
    df = df[~df['SETOR'].isin(setores_ignorados)]

    ## Transformar a coluna ANO_NASCIMENTO em inteiro
    df['ANO_NASCIMENTO'] = df['ANO_NASCIMENTO'].astype(int)

    ## Transformar a coluna 'DATA_INICIO_EXERCICIO' em datetime
    df['DATA_INICIO_EXERC'] = pd.to_datetime(df['DATA_INICIO_EXERC'], errors='coerce')
    
    return df

## Visualizar o resultado da preparação dos dados
def viualizar_dados(df):
    ## Visualizar as primeiras observações de df2024
    df.info()
    df.head()
 
## Nessa função, vamos analisar a quantidade de servidores e servidoras que poderão se aposentar em 2024 e em 2029. Para isso, vamos considerar as condições da regra de transição (categoria pedágio): Para ambos os sexos, ter mais de 20 anos de serviço público. Para homens, ter mais de 60 anos de idade. Para mulheres, ter mais de 57 anos de idade.

def analise_aposentadorias_para_ano(df2024, df2019 ,projecao_anos):

    # Iniciaremos resolvendo a inconsistência de datas de início de exercício dos datasets. Devido a reestruturação de carreira que aconteceu em 2022, os servidores que optaram por mudar a carreira, tiveram a data de início de exercício alterada para a data de início da nova carreira. Para resolver essa inconsistência, vamos comparar as datas de início de exercício dos servidores que estão presentes nos dois datasets e atualizar a data de início de exercício de 2024 para a data de início de exercício de 2019, caso seja diferente a fim de calcularmos o tempo de serviço público de forma correta.

    # Fazer uma cópia do DataFrame para garantir que o original não seja modificado
    df = df2024.copy()
           
    # Inicializar a coluna 'CONSISTENTE' com True
    df['CONSISTENTE'] = True
    
    # Iterar sobre as linhas do df2024
    for idx, row in df  .iterrows():
        nome = row['NOME']
        data_inicio_exerc_2024 = row['DATA_INICIO_EXERC']
        
        # Procurar o mesmo servidor no df2019
        if nome in df2019['NOME'].values:
            data_inicio_exerc_2019 = df2019[df2019['NOME'] == nome]['DATA_INICIO_EXERC'].values[0]
            
            # Comparar as datas e atualizar se necessário
            if pd.notna(data_inicio_exerc_2019) and (data_inicio_exerc_2024 != data_inicio_exerc_2019):
                df2024.at[idx, 'DATA_INICIO_EXERC'] = data_inicio_exerc_2019
                df2024.at[idx, 'CONSISTENTE'] = False
    
    ## Resolvida as inconsistências, vamos calcular o tempo de serviço público de cada servidor, e sua idade no ano que será feita a projeção.

    # Calcular a idade e o tempo de serviço público
    for ano in projecao_anos:
        # Calcular a idade e o tempo de serviço público até o ano de projeção
        df[f'IDADE_{ano}'] = ano - df['ANO_NASCIMENTO'].astype(int)
        df[f'TEMPO_SERVICO_PUBLICO_{ano}'] = ano - df['DATA_INICIO_EXERC'].dt.year

        # Criar a variável 'APTO_APOSENTADORIA' considerando:
        # Homens: idade >= 60 e tempo de serviço público >= 20
        # Mulheres: idade >= 57 e tempo de serviço público >= 20

        df[f'APTO_APOSENTADORIA_{ano}'] = ((df[f'IDADE_{ano}'] >= 60) & (df[f'TEMPO_SERVICO_PUBLICO_{ano}'] >= 20) & (df['SEXO'] == 'M')) | ((df[f'IDADE_{ano}'] >= 57) & (df[f'TEMPO_SERVICO_PUBLICO_{ano}'] >= 20) & (df['SEXO'] == 'F'))

    # Vamos limpar o DataFrame para retornar apenas as variáveis de interesse
    df = df[['NOME', 'SEXO', 'SETOR', 'CARGO_BASICO', 'IDADE_2024', 'TEMPO_SERVICO_PUBLICO_2024', 'APTO_APOSENTADORIA_2024', 'IDADE_2029', 'TEMPO_SERVICO_PUBLICO_2029', 'APTO_APOSENTADORIA_2029']] 
    
    # Retornar o DataFrame atualizado
    return df

## Criaremos agora uma função para visualizar os cenários de aposentadoria para os anos de 2024 e 2029.

def cenario_pos_aposentadoria(df, ano_projecao):
    # Verificar se o ano de projeção é válido
    if ano_projecao not in [2024, 2029]:
        raise ValueError("Ano de projeção deve ser 2024 ou 2029")

    # Contar o total de servidores por setor
    total_servidores = df['SETOR'].value_counts().reset_index()
    total_servidores.columns = ['Setor', 'Total de servidores']

    # Contar os aptos a aposentadoria por setor
    aptos_aposentadoria = df[df[f'APTO_APOSENTADORIA_{ano_projecao}']]['SETOR'].value_counts().reset_index()
    aptos_aposentadoria.columns = ['Setor', 'Aptos a aposentadoria']

    # Mesclar as tabelas para calcular os remanescentes
    cenario = total_servidores.merge(aptos_aposentadoria, on='Setor', how='left')
    cenario['Aptos a aposentadoria'] = cenario['Aptos a aposentadoria'].fillna(0).astype(int)
    cenario['Remanescentes'] = cenario['Total de servidores'] - cenario['Aptos a aposentadoria']

    # Filtrar os analistas remanescentes
    analistas_remanescentes = df[(~df[f'APTO_APOSENTADORIA_{ano_projecao}']) & 
                                 (df['CARGO_BASICO'].str.contains('ANALISTA DE INFORMACOES CULTURA E DESPORTO', na=False))]['SETOR'].value_counts().reset_index()
    analistas_remanescentes.columns = ['Setor', 'Remanescentes analistas bibliotecárias(os)']

    # Mesclar a tabela de analistas remanescentes
    cenario = cenario.merge(analistas_remanescentes, on='Setor', how='left')
    cenario['Remanescentes analistas bibliotecárias(os)'] = cenario['Remanescentes analistas bibliotecárias(os)'].fillna(0).astype(int)
    
    # Remover a coluna 'Aptos a aposentadoria'

    cenario = cenario.drop(columns='Aptos a aposentadoria')

    return cenario

## Criaremos agora funções para plotar as análises realizadas.:
#1. Total de servidores por setor nos anos de 2019 e 2024, com as colunas 'Setor', 'Total de servidores 2019' e 'Total de servidores 2024'.
def preparar_dados_tabela(df2019, df2024):
    # Contar o total de servidores por setor para 2019 e 2024
    total_servidores_2019 = df2019['SETOR'].value_counts().reset_index()
    total_servidores_2019.columns = ['Setor', 'Total Servidores 2019']

    total_servidores_2024 = df2024['SETOR'].value_counts().reset_index()
    total_servidores_2024.columns = ['Setor', 'Total Servidores 2024']

    # Mesclar os dados em um único DataFrame
    tabela_total_servidores = pd.merge(total_servidores_2019, total_servidores_2024, on='Setor', how='outer').fillna(0)
    tabela_total_servidores['Total Servidores 2019'] = tabela_total_servidores['Total Servidores 2019'].astype(int)
    tabela_total_servidores['Total Servidores 2024'] = tabela_total_servidores['Total Servidores 2024'].astype(int)

    return tabela_total_servidores


## Começaremos a chamar as variáveis que serão utilizadas para a análise comparativa.

df2024, df2019 = carregar_dados()

colunas_desnecessarias = ['VINCULO', 'REF_CARGO_BAS', 'GRUPO', 'REF_CARGO_COM', 'ESCOL_CARGO_COMISSAO', 'JORNADA', 'ORGAO_EXT', 'RACA', 'DEFICIENTE']

setores_ignorados = [
    'BIBLIOTECA MUNICIPAL MARIO DE ANDRADE',
    'BIBLIOTECA PUBLICA MUNICIPAL LOUIS BRAILLE',
    'BIBLIOTECA PUBLICA MUNICIPAL SERGIO MILLIET',
    'BIBLIOTECA JOAO CABRAL DE MELO NETO - CEU VILA CUR',
    'BIBLIOTECA JORNALISTA ROBERTO MARINHO - CEU BUTANT',
    'BIBLIOTECA RACHEL DE QUEIROZ - CEU ALVARENGA'
]

df2024 = preparar_dados(df2024, colunas_desnecessarias, setores_ignorados)

df2019 = preparar_dados(df2019, colunas_desnecessarias, setores_ignorados)

viualizar_dados(df2024)

viualizar_dados(df2019)

projecao_anos = [2024, 2029]

df_aposen = analise_aposentadorias_para_ano(df2024, df2019, projecao_anos)

df_aposen.info()

df_cenario_2024 = cenario_pos_aposentadoria(df_aposen, 2024)

df_cenario_2029 = cenario_pos_aposentadoria(df_aposen, 2029)

tabela_total_servidores = preparar_dados_tabela(df2019, df2024) 