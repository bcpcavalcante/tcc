#Instalando as bibliotecas
#%pip install pandas

## Importar as bibliotecas
import pandas as pd

## Carregar o arquivo csv
df = pd.read_csv(r'c:\Repos\tcc-bruna\fonte.csv')

## Verificar o formato dos dados
df.info()

## Verificar a quantidade de valores nulos
df.isnull().sum()
## Remover as linhas que possuem valor nulo na coluna 'SETOR'
df = df.dropna(subset=['SETOR'])

## Selecionar as linhas que utilizaremos na análise
## Vamos remover todas as observações que não possuem a substring ''BIBLIOTECA'' na coluna 'SETOR'
df_bibliotecas = df[df['SETOR'].str.contains('BIBLIOTECA')]

## Verificar o formato dos dados resultantes
df_bibliotecas.info()

##Remover as linhas cuja variável 'SETOR' é BIBLIOTECA MUNICIPAL MARIO DE ANDRADE , BIBLIOTECA PUBLICA MUNICIPAL LOUIS BRAILLE, BIBLIOTECA PUBLICA MUNICIPAL SERGIO MILLIET, BIBLIOTECA JOAO CABRAL DE MELO NETO (CEU), BIBLIOTECA JORNALISTA ROBERTO MARINHO (CEU) e BIBLIOTECA RACHEL DE QUEIROZ (CEU)
df_bibliotecas = df_bibliotecas[~df_bibliotecas['SETOR'].str.contains('BIBLIOTECA MUNICIPAL MARIO DE ANDRADE')]
df_bibliotecas = df_bibliotecas[~df_bibliotecas['SETOR'].str.contains('BIBLIOTECA PUBLICA MUNICIPAL LOUIS BRAILLE')]
df_bibliotecas = df_bibliotecas[~df_bibliotecas['SETOR'].str.contains('BIBLIOTECA PUBLICA MUNICIPAL SERGIO MILLIET')]
df_bibliotecas = df_bibliotecas[~df_bibliotecas['SETOR'].str.contains('BIBLIOTECA JOAO CABRAL DE MELO NETO')]
df_bibliotecas = df_bibliotecas[~df_bibliotecas['SETOR'].str.contains('BIBLIOTECA JORNALISTA ROBERTO MARINHO')]
df_bibliotecas = df_bibliotecas[~df_bibliotecas['SETOR'].str.contains('BIBLIOTECA RACHEL DE QUEIROZ')]

##Mostar a lista de bibliotecas distinta
df_bibliotecas['SETOR'].unique()

##Mostrar as informações dos setores
setores_contagem = df_bibliotecas['SETOR'].value_counts()
setores_contagem = setores_contagem.reset_index()
setores_contagem.columns = ['SETOR', 'QUANTIDADE']
setores_contagem = setores_contagem.sort_values(by='QUANTIDADE', ascending=False)
print(setores_contagem)

##Removendo as colunas que não serão utilizadas
bibliotecas = df_bibliotecas.drop(columns=['VINCULO', 'REF_CARGO_BAS', 'GRUPO', 'REF_CARGO_COM', 'ESCOL_CARGO_COMISSAO', 'JORNADA', 'ORGAO_EXT', 'RACA', 'DEFICIENTE'])

##Info da base de dados limpa
bibliotecas.info()

## Transformando a coluna ANO_NASCIMENTO em inteiro
bibliotecas['ANO_NASCIMENTO'] = bibliotecas['ANO_NASCIMENTO'].astype(int)

#Verificar se a coluna foi transformada
bibliotecas.info()

##Criar uma coluna idade
bibliotecas['IDADE'] = 2024 - bibliotecas['ANO_NASCIMENTO']

## Transformar os valores da coluna data de admissão em datetime
bibliotecas['DATA_INICIO_EXERC'] = pd.to_datetime(bibliotecas['DATA_INICIO_EXERC'])

# Verificar se alguma data não pôde ser convertida
invalid_dates = bibliotecas[bibliotecas['DATA_INICIO_EXERC'].isna()]
print(invalid_dates)

bibliotecas.info()

##Contar quantos servidores ingressaram antes de 19/03/2022
antes_2022 = bibliotecas[bibliotecas['DATA_INICIO_EXERC'] < '2022-03-19']
print(f'Quantidade de servidores que ingressaram antes de 19/03/2022: {antes_2022.shape[0]}')

##Desses servidores, quantos terão mais de 20 anos de serviço até 2024
antes_2022_mais_20_serv = antes_2022[antes_2022['DATA_INICIO_EXERC'] < '2005-01-01']
print(f'Quantidade de servidores que ingressaram antes de 18/03/2022 e terão mais de 20 anos de serviço até 2024: {antes_2022_mais_20_serv.shape[0]}')

##Desses servidores, quantos são do sexo masculino e nasceram antes de 1965
antes_2022_mais_20_serv_masc = antes_2022_mais_20_serv[(antes_2022_mais_20_serv['SEXO'] == 'M') & (antes_2022_mais_20_serv['ANO_NASCIMENTO'] < 1965)]
print(f'Quantidade de servidores do sexo masculino que ingressaram antes de 18/03/2022, terão mais de 20 anos de serviço até 2024 e nasceram antes de 1965: {antes_2022_mais_20_serv_masc.shape[0]}')

##Faremos o mesmo para os servidores do sexo feminino, e considerando as mulheres que nasceram antes de 1968
antes_2022_mais_20_serv_fem = antes_2022_mais_20_serv[(antes_2022_mais_20_serv['SEXO'] == 'F') & (antes_2022_mais_20_serv['ANO_NASCIMENTO'] < 1968)]
print(f'Quantidade de servidores do sexo feminino que ingressaram antes de 18/03/2022, terão mais de 20 anos de serviço até 2024 e nasceram antes de 1968: {antes_2022_mais_20_serv_fem.shape[0]}')

##Dessa tabela de servidoras, quantas tem mais de 30 anos de serviço
antes_2022_mais_20_serv_fem_mais_30_serv = antes_2022_mais_20_serv_fem[antes_2022_mais_20_serv_fem['DATA_INICIO_EXERC'] < '1995-01-01']
print(f'Quantidade de servidoras do sexo feminino que ingressaram antes de 18/03/2022, terão mais de 20 anos de serviço até 2024, nasceram antes de 1968 e terão mais de 30 anos de serviço até 2024: {antes_2022_mais_20_serv_fem_mais_30_serv.shape[0]}')

##Dos servidores do sexo masculino que ingressaram antes de 18/03/2022, quantos terão mais de 35 anos de serviço até 2024
antes_2022_mais_20_serv_masc_mais_35_serv = antes_2022_mais_20_serv_masc[antes_2022_mais_20_serv_masc['DATA_INICIO_EXERC'] < '1990-01-01']
print(f'Quantidade de servidores do sexo masculino que ingressaram antes de 18/03/2022, terão mais de 20 anos de serviço até 2024, nasceram antes de 1965 e terão mais de 35 anos de serviço até 2024: {antes_2022_mais_20_serv_masc_mais_35_serv.shape[0]}')

##Faremos projeções para o ano de 2029
##Dos servidores que entraram antes de 18/03/2022, quantos terão mais de 25 anos de serviço até 2029
antes_2022_mais_20_serv_mais_25_serv = antes_2022[antes_2022['DATA_INICIO_EXERC'] < '2009-01-01']
print(f'Quantidade de servidores que ingressaram antes de 18/03/2022 e terão mais de 25 anos de serviço até 2029: {antes_2022_mais_20_serv_mais_25_serv.shape[0]}')

## Vamos criar um dataset, com as servidoras que tem mais de 62 anos, e no mínimo 10 anos de serviço público
servFem_possivelmente_aposentaveis = bibliotecas[(bibliotecas['SEXO'] == 'F') & (bibliotecas['ANO_NASCIMENTO'] <= 1962) & (bibliotecas['DATA_INICIO_EXERC'] < '2014-01-01')]

##Mostrar a quantidade de servidoras aposentáveis
print(f'Quantidade de servidoras do sexo feminino que ingressaram antes de 2014 e nasceram em/antes de 1962:{len(servFem_possivelmente_aposentaveis)}')

##Dentre esses servidores, quantos tem mais de 25 anos de serviço público
servFem_certamente_aposentaveis = servFem_possivelmente_aposentaveis[servFem_possivelmente_aposentaveis['DATA_INICIO_EXERC'] < '1999-01-01']
print(f'Quantidade de servidoras do sexo feminino que ingressaram antes de 2014 e nasceram em/antes de 1962 e tem mais de 25 anos de serviço público:{len(servFem_certamente_aposentaveis)}')

##Faremos o mesmo para os servidores do sexo masculino
servMasc_possivelmente_aposentaveis = bibliotecas[(bibliotecas['SEXO'] == 'M') & (bibliotecas['ANO_NASCIMENTO'] <= 1959) & (bibliotecas['DATA_INICIO_EXERC'] < '2014-01-01')]
print(f'Quantidade de servidores do sexo masculino que ingressaram antes de 2014 e nasceram em/antes de 1959:{len(servMasc_possivelmente_aposentaveis)}')

servMasc_certamente_aposentaveis = servMasc_possivelmente_aposentaveis[servMasc_possivelmente_aposentaveis['DATA_INICIO_EXERC'] < '1989-01-01']
print(f'Quantidade de servidores do sexo masculino que ingressaram antes de 2014 e nasceram em/antes de 1959 e tem mais de 35 anos de serviço público:{len(servMasc_certamente_aposentaveis)}')

##criar um novo dataframe sem os servidores e servidoras que certamente se aposentarão
certamente_aposentaveis = pd.concat([servFem_certamente_aposentaveis, servMasc_certamente_aposentaveis], ignore_index=True)
certamente_aposentaveis.info()

##criar um novo dataframe sem os servidores e servidoras que possivelmente se aposentarão
possivelmente_aposentaveis = pd.concat([servFem_possivelmente_aposentaveis, servMasc_possivelmente_aposentaveis], ignore_index=True)
possivelmente_aposentaveis.info()

##Removendo do dataset original os servidores e servidoras que certamente se aposentarão, usando a coluna REGISTRO como chave
servidores_restantes = bibliotecas[~bibliotecas['REGISTRO'].isin(certamente_aposentaveis['REGISTRO'])]
servidores_restantes.info()

##Verificando após a remoção de servidores que possivelmente se aposentarão, quantos servidores restaram em cada setor
setores_contagem_apos = servidores_restantes['SETOR'].value_counts()
setores_contagem_apos = setores_contagem_apos.reset_index()
setores_contagem_apos.columns = ['SETOR', 'QUANTIDADE']
setores_contagem_apos = setores_contagem_apos.sort_values(by='QUANTIDADE', ascending=False)
print(setores_contagem_apos)

##Do dataframe bibliotecas, extrairemos um dataset com as servidoras que terão mais de 57 anos ao final de 2024, e que terão mais de 30 anos de serviço público
servidoras_30mais = bibliotecas[(bibliotecas['SEXO'] == 'F') & (bibliotecas['ANO_NASCIMENTO'] <= 1967) & (bibliotecas['DATA_INICIO_EXERC'] < '1994-01-01')]
print(f'Quantidade de servidoras do sexo feminino que ingressaram antes de 1994 e nasceram em/antes de 1967:{len(servidoras_30mais)}')

##Calculando idades 
masc_65 = bibliotecas[(bibliotecas['SEXO'] == 'M') & (bibliotecas['IDADE'] >= 65)]
print(f'Quantidade de servidores do sexo masculino que terão 65 anos em 2024: {masc_65.shape[0]}')
fem_62 = bibliotecas[(bibliotecas['SEXO'] == 'F') & (bibliotecas['IDADE'] >= 62)]
print(f'Quantidade de servidores do sexo feminino que terão 62 anos em 2024: {fem_62.shape[0]}')


##Faremos uma projeção para o final de 2029, e verificaremos quantas servidoras terão mais de 62 anos, e mais de 10 anos de serviço público
proj_4anos_servidoras_62_10 = bibliotecas[(bibliotecas['SEXO'] == 'F') & (bibliotecas['IDADE'] <= 1967) & (bibliotecas['DATA_INICIO_EXERC'] < '2020-01-01')]
print(f'Quantidade de servidoras do sexo feminino que ingressaram antes de 2020 e nasceram em/antes de 1967:{len(proj_4anos_servidoras_62_10)}')

##Vamos verificar quantas dessas terão mais de 25 anos de serviço público
proj_4anos_servidoras_62_25 = proj_4anos_servidoras_62_10[proj_4anos_servidoras_62_10['DATA_INICIO_EXERC'] < '2005-01-01']
print(f'Quantidade de servidoras do sexo feminino que ingressaram antes de 2019 e nasceram em/antes de 1967 e tem mais de 25 anos de serviço público:{len(proj_4anos_servidoras_62_25)}')

##Faremos o mesmo para os servidores do sexo masculino
proj_4anos_servidores_65_10 = bibliotecas[(bibliotecas['SEXO'] == 'M') & (bibliotecas['ANO_NASCIMENTO'] <= 1964) & (bibliotecas['DATA_INICIO_EXERC'] < '2020-01-01')]
print(f'Quantidade de servidores do sexo masculino que ingressaram antes de 2020 e nasceram em/antes de 1964:{len(proj_4anos_servidores_65_10)}')

proj_4anos_servidores_65_25 = proj_4anos_servidores_65_10[proj_4anos_servidores_65_10['DATA_INICIO_EXERC'] < '2005-01-01']
print(f'Quantidade de servidores do sexo masculino que ingressaram antes de 2019 e nasceram em/antes de 1964 e tem mais de 25 anos de serviço público:{len(proj_4anos_servidores_65_25)}')





