import pandas as pd
from datetime import datetime

# Caminho para o arquivo Excel
file_path = '/Users/bruna/Downloads/Servidores.xlsx'

# Ler a planilha específica pelo nome ('2019')
df = pd.read_excel(file_path, sheet_name='2019')

# Garantir que a coluna DATA_INICIO_EXERC está no formato de data
df['DATA_INICIO_EXERC'] = pd.to_datetime(df['DATA_INICIO_EXERC'], format='%d/%m/%Y', errors='coerce')

# Calcular o tempo de contribuição em anos
data_atual = datetime.now()
df['TEMPO_CONTRIBUICAO'] = (data_atual - df['DATA_INICIO_EXERC']).dt.days / 365.25

# Filtrar os servidores do sexo M com 35 anos ou mais de contribuição
masculino_aposentados = df[(df['SEXO'] == 'M') & (df['TEMPO_CONTRIBUICAO'] >= 35)]

# Contar quantos servidores do sexo M já possuem 35 anos de contribuição
quantidade_masculino_aposentados = len(masculino_aposentados)

# Mostrar o resultado
print(f"Quantidade de servidores do sexo M com 35 anos ou mais de contribuição: {quantidade_masculino_aposentados}")


