#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# UNIVERSIDADE DE SÃO PAULO
# MBA DATA SCIENCE & ANALYTICS USP/ESALQ

# SCRIPT TCC - ALEX DE LIMA BASSI

# Titulo TCC: Fatores Individuais e Contextuais Associados à Mortalidade por 
    Doenças Crônicas em Adultos no Brasil: Uma Abordagem com Regressão 
    Logística Multinível 

"""
#%%

'''
########################################################################
#                Instalação dos pacotes a serem utilizados             #
########################################################################
'''
!pip install pandas
!pip install numpy
!pip install -U seaborn
!pip install matplotlib
!pip install plotly
!pip install scipy
!pip install statsmodels
!pip install scikit-learn
!pip install statstests
!pip install pymer4
!pip install -q watermark
!pip install chardet
!pip install xlrd

#%%
'''
######################################################################### 
#                   Pacotes Utilizadas                                  #
#########################################################################
'''

# Manipulação de dados em formato de dataframe
import pandas as pd

# Operações matemáticas
import numpy as np 

# Visualização gráfica
import seaborn as sns 

# Visualização gráfica
import matplotlib.pyplot as plt 

# Estimação de modelos
import statsmodels.api as sm 
#from pymer4.models import lmer # estimação de modelos HLM3 neste código

# Estatística chi2
from scipy import stats 

# Comparação entre modelos
from statsmodels.iolib.summary2 import summary_col 

# Inserção de KDEs em gráficos
from scipy.stats import gaussian_kde 

# Plotagem de gráficos separados
from matplotlib.gridspec import GridSpec 

# Adiciona um indicador de progresso do código
from tqdm import tqdm 

# Cria diretórios temporários 
import tempfile

# Permite manipular o sistema operacional
import os

# Permite fazer requisições HTTP a partir do python
import requests

# Detectar codificação
import chardet

# Tirar caracteres especiais
import unicodedata

# Utilizar regular expression com as colunas do dataaframe
import re

#%%
'''
##############################################################################
##############################################################################
#                ESTIMAÇÃO DE MODELOS HIERÁRQUICOS LINEARES                  #
#                    DE DOIS NÍVEIS COM DADOS AGRUPADOS                      #
##############################################################################
##############################################################################

##############################################################################
#        DESCRIÇÃO E EXPLORAÇÃO DO DATASET 'SIM_INDICADORES_MUNICIPAIS'      #
##############################################################################

##### Nível 1 – **Indivíduo (registro de óbito)**

 Idade
 Sexo
 Escolaridade
 Raça/cor
 Código Município Residência
 CID-10 (grupo de causa)


##### Nível 2 – **Município**
 Agropecuária
 Indústria
 Serviços Administração Pública 
 Serviços (exceto Administração Pública)
 Impostos
 Renda per capita
 IDH
 IDHM
 IDHM Renda 2010
 IDHM Longevidade 2010
 IDHM Educação 2010

'''
#%%

'''
########################################################################
# Função para imprimir as bibliotecas utilizadas no código inclusive R #
########################################################################

'''
def print_versions(libs):
    import importlib
    import importlib.metadata

    for lib in libs:
        try:
            # Primeiro tenta pegar via importlib.metadata
            version = importlib.metadata.version(lib)
        except importlib.metadata.PackageNotFoundError:
            try:
                # Se não encontrar, tenta importar e pegar __version__
                module = importlib.import_module(lib)
                version = getattr(module, '__version__', 'sem __version__')
            except ImportError:
                version = 'não instalado'
        print(f"{lib}: {version}")

# Lista de bibliotecas utilizadas, incluindo pymer4 e statstests
libs_usadas = ['numpy', 'pandas', 'matplotlib', 'scipy', 'sklearn', 'seaborn', 'plotly',
               'statsmodels','statstests','pymer4', 'watermark']
print_versions(libs_usadas)

#%%
'''
#####################################################################################################
# Imprime a versão das bibliotecas utilizadas apenas do PYTHON e informações do sistema operacional #
####################################################################################################
'''
#Registrar os pacotes e versões utilizados
%load_ext watermark

#informações do Sistema operacional, compilador e implementação do Python
%watermark -v -m

# Imprime a versão das bibliotecas do python   
%watermark --iversions   

 
#%%
'''
#############################################################################
#    Criação de variáveis que armazenaram as urls de download dos arquivos  #
#############################################################################
'''
# DATASUS
url = "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SIM/DO24OPEN.csv"

#SEADE
#url2 = "https://repositorio.seade.gov.br/dataset/1bd90672-72a8-47cb-a34d-ab9eb703735d/resource/c2eb14df-60e0-44d6-9e7a-9fcdc339c4ad/download/pib-municipios-2021_site.xlsx"

# URL Alternativa quando site da SEADE estiver fora do ar
url2 = "https://raw.githubusercontent.com/albbassiStudent/repositorio_tcc/refs/heads/main/fontes_dados/pib-municipios-2021-seade.csv"

#Código Municípios IBGE
url3 = "https://github.com/albbassiStudent/repositorio_tcc/raw/refs/heads/main/fontes_dados/cod_municipios_ibge.csv"

#PNUD IDH
url4 = "https://github.com/albbassiStudent/repositorio_tcc/raw/refs/heads/main/fontes_dados/idh_municipios_2010_atlas_desenvolvimento_humano.csv" 


#%%    

# Download primeira base de dados SIM DATASUS    
#################################################################
#        INICIO EXTRAÇÃO DADOS SIM DATASUS                      #
#################################################################
    
# DATASUS
with tempfile.TemporaryDirectory() as temp_dir:
    filename =  "dados_sim_2024.csv"
    filepath = os.path.join(temp_dir, filename)
    response = requests.get(url, stream=True)
            
    if response.status_code == 200:
        # Tamanho total do arquivo em bytes
        total = int(response.headers.get('content-length', 0))
        chunk_size = 1024  # 1 KB por iteração

        # Cria uma barra de progresso
        with open(filepath, 'wb') as f, tqdm(
            desc=filename,
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1024
        ) as bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

        print(f"\nDownload completo! Arquivo salvo em: {filepath}")
        caminho = filepath
        # Lê do CSV e guarda os dados em um Dataframe
        df_dados_sim_2024 = pd.read_csv(caminho, sep=';', encoding='utf-8')
    else:
        print(f"Erro ao baixar arquivo: código {response.status_code}")

    
#################################################################
#               FIM EXTRAÇÃO DADOS SIM DATASUS                  #
#################################################################   

#%%    

#################################################################
#               INICIO EXTRAÇÃO DADOS SEADE                     #
#################################################################


#Criação do diretório temporario para guarda dos arquivos até a carga do Dataframe
with tempfile.TemporaryDirectory() as temp_dir:
    filename2 = "dados_seade_2021.xlsx"
    filepath = os.path.join(temp_dir, filename2)
    response2 = requests.get(url2, stream=True, verify=False)

    if response2.status_code == 200:
        # Tamanho total do arquivo em bytes
        total = int(response2.headers.get('content-length', 0))
        chunk_size = 10  # 10B por iteração

        # Cria uma barra de progresso
        with open(filepath, 'wb') as f, tqdm(
            desc=filename2,
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1
        ) as bar:
            for chunk in response2.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

        print(f"\nDownload completo! Arquivo salvo em: {filepath}")
        caminho2 = filepath

        # Ler o XLSX
        #df_dados_seade_2021 = pd.read_excel(caminho2, usecols='A:E,G:H,I', skiprows=12, header=None, names=['municipios', 'agropecuaria', 'industria', 'administracao_publica', 'servicos', 'impostos', 'pib','pib_per_capita'])
        #df_dados_seade_2021.drop(df_dados_seade_2021.tail(3).index, inplace=True)
        
        # Leitura alternativo quando o site está fora do ar
        df_dados_seade_2021 = pd.read_csv(caminho2, sep=';', encoding='utf-8')
        
    else:
        print(f"Erro ao baixar arquivo: código {response2.status_code}")
        

#################################################################
#               FIM EXTRAÇÃO DADOS SEADE                        #
#################################################################


#%%    

#################################################################
#              INICIO EXTRAÇÃO DADOS CODIGO MUNICIPIOS IBGE     #
#################################################################

#IBGE Via git TCC
with tempfile.TemporaryDirectory() as temp_dir:
    filename3 = "dados_cod_mun_ibge.csv"
    filepath = os.path.join(temp_dir, filename3)
    response3 = requests.get(url3, stream=True, verify=False)
    if response3.status_code == 200:
        # Tamanho total do arquivo em bytes
        total = int(response3.headers.get('content-length', 0))
        chunk_size = 1024  # 1 0B por iteração

        # Cria uma barra de progresso
        with open(filepath, 'wb') as f, tqdm(
            desc=filename3,
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1024
        ) as bar:
            for chunk in response3.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

        print(f"\nDownload completo! Arquivo salvo em: {filepath}")
        caminho3 = filepath

        # Ler o CSV
        df_dados_cod_municipio_ibge = pd.read_csv(caminho3, sep=';', encoding='utf-8')
        df_dados_cod_municipio_ibge['Código Município Completo'] = df_dados_cod_municipio_ibge['Código Município Completo'].astype(str).str[:-1].astype('category')
    else:
        print(f"Erro ao baixar arquivo: código {response3.status_code}")


#################################################################
#               FIM EXTRAÇÃO DADOS IBGE                         #
#################################################################

#%%
#################################################################
#               INICIO EXTRAÇÃO DADOS IDH PNUD                  #
#################################################################

#PNUD IDH
#Criação do diretório temporário para guarda dos arquivos baixados
with tempfile.TemporaryDirectory() as temp_dir:
    filename4 = "dados_pnud_idh_2010.csv"
    filepath = os.path.join(temp_dir, filename4)
    response4 = requests.get(url4, stream=True)

    # Download da base de dados PNUD IDH    
    if response4.status_code == 200:
        # Tamanho total do arquivo em bytes
        total = int(response.headers.get('content-length', 0))
        chunk_size = 1  # 1024 KB por iteração

        # Cria uma barra de progresso
        with open(filepath, 'wb') as f, tqdm(
            desc=filename4,
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1
        ) as bar:
            for chunk in response4.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))

        print(f"\nDownload completo! Arquivo salvo em: {filepath}")
        caminho4 = filepath
        # Lê do CSV e guarda os dados em um Dataframe
        df_dados_pnud_2010 = pd.read_csv(caminho4, sep=';', encoding='utf-8')
    else:
        print(f"Erro ao baixar arquivo: código {response.status_code}")
    
#################################################################
#               FIM EXTRAÇÃO DADOS IDH PNUD                     #
#################################################################

#%%
################################################################
#       Extração dados PNUD sem a barra de progresso           #
################################################################
###########################################################################
#      Está comentado porque corrigi a versão com a barra de progresso    # 
###########################################################################
# with tempfile.TemporaryDirectory() as temp_dir:
#     filename4 = "dados_pnud_idh_2010.csv"
#     filepath = os.path.join(temp_dir, filename4)  # Corrigido: filename -> filename4

#     response4 = requests.get(url4)

#     # Download da base de dados PNUD IDH    
#     if response4.status_code == 200:
#         with open(filepath, 'wb') as f:
#             f.write(response4.content)

#         print(f"\nDownload completo! Arquivo salvo em: {filepath}")
#         caminho4 = filepath

#         # Lê o CSV e guarda os dados em um DataFrame
#         df_dados_pnud_2010 = pd.read_csv(caminho4, sep=';',encoding='latin1')
#     else:
#         print(f"Erro ao baixar arquivo: código {response4.status_code}")  # Corrigido: response -> response4


#%%
'''
############################################################################
#                     Ajustes Dataframe SIM DATASUS                        #
############################################################################
'''


df_dados_sim_2024_filtrado = df_dados_sim_2024[['IDADE', 'SEXO', 'RACACOR', 'CODMUNRES', 'CAUSABAS']].astype({
    'IDADE': 'int',
    'SEXO': 'category',
    'RACACOR': 'category',
    'CODMUNRES':'str',
    'CAUSABAS':'category'})



# pega o primeiro algaritimo da idade para classificar o tipo de contagem (hora, mes, ano, +100 anos)
df_dados_sim_2024_filtrado['tipo_idade'] = df_dados_sim_2024_filtrado['IDADE'].fillna('').astype(str).str[0]

# pega os dois ultimos digitos da idade para dar a idade no momento da morte (hora, mes, ano, +100 anos)
df_dados_sim_2024_filtrado['idade_corrigida']= df_dados_sim_2024_filtrado['IDADE'].fillna('').astype(str).str[1:4]
# Se a idade não estiver preenchida coloca N/A
df_dados_sim_2024_filtrado['idade_corrigida'] = pd.to_numeric(df_dados_sim_2024_filtrado['idade_corrigida'], errors='coerce').astype('Int64')
# Retira a coluna idade que vem codificada
df_dados_sim_2024_filtrado.drop(['IDADE'], axis=1, inplace=True)
# Renomeia as colunas para lower case
df_dados_sim_2024_filtrado.rename(columns={
    'SEXO': 'sexo',
    'RACACOR': 'raca_cor',
    'CODMUNRES':'cod_mun_res',
    'CAUSABAS':'causa_basica'
    }, inplace=True)


# Converte o tipo de idade para categoria 
df_dados_sim_2024_filtrado['tipo_idade'] = df_dados_sim_2024_filtrado['tipo_idade'].astype('category')

# Filtra apenas as ocorrência de óbito registradas em municípios de São Paulo 
df_dados_sim_2024_filtrado_sp = df_dados_sim_2024_filtrado[df_dados_sim_2024_filtrado['cod_mun_res'].astype(str).str.startswith('35', na=False)]

# corrige dataframe para idades acima de 100 anos
df_dados_sim_2024_filtrado_sp.loc[(df_dados_sim_2024_filtrado_sp['tipo_idade' ] == '5') & (df_dados_sim_2024_filtrado_sp['idade_corrigida' ] < 100), 'idade_corrigida'] += 100

# Pega todos os registros com o código de municipio 350000 (que não existe para o ibge) para o código 350001 (Município de São Paulo) 
df_dados_sim_2024_filtrado_sp.loc[(df_dados_sim_2024_filtrado_sp['cod_mun_res' ] == '350000'), 'cod_mun_res'] = '355030'

# Ajusta o nome do Dataframe
df_dados_sim_2024_sp_final = df_dados_sim_2024_filtrado_sp

# Troca o nome do código de municipio par cod_ibge conforme a chave os outros dataframes
df_dados_sim_2024_sp_final.rename(columns={
    'cod_mun_res': 'cod_ibge'}, inplace = True)

#%%
###########################################################################
#                  Estatisticas iniciais do dataframe                     #
###########################################################################

# Numéricas: média, std, min, max, quartis
#df_dados_sim_2024_filtrado_sp.describe()

'''
       idade_corrigida
count         333035.0
mean         68.881187
std          19.410306
min                0.0
25%               59.0
50%               72.0
75%               83.0
max              122.0
'''       

# Tipo de dados, nulos, memória
#df_dados_sim_2024_filtrado_sp.info()             
'''
<class 'pandas.core.frame.DataFrame'>
Index: 333132 entries, 272 to 1425387
Data columns (total 6 columns):
 #   Column           Non-Null Count   Dtype   
---  ------           --------------   -----   
 0   sexo             333132 non-null  category
 1   raca_cor         330960 non-null  category
 2   cod_mun_res      333132 non-null  category
 3   causa_basica     333132 non-null  category
 4   tipo_idade       333132 non-null  category
 5   idade_corrigida  333035 non-null  Int64   
dtypes: Int64(1), category(5)
memory usage: 8.0 MB

'''
# Total de valores ausentes por coluna
df_dados_sim_2024_filtrado_sp.isnull().sum()
 
'''
sexo                  0
raca_cor           2172
cod_mun_res           0
causa_basica          0
tipo_idade            0
idade_corrigida      97
dtype: int64
'''

##############################################################################
#                  Término tratamento SIM DATASUS                            #
##############################################################################


#%%

'''
##############################################################################
#                  Inicio tratamento SEADE                                   #
##############################################################################
'''
# Informações do Dataframe
#df_dados_seade_2021.info()
#df_dados_seade_2021.describe()
#df_dados_seade_2021.count()

# Troca o nome da coluna
df_dados_seade_2021.rename(columns={'municipios':'municipio'}, inplace=True)

# Converte o nome do municipio para category
df_dados_seade_2021['municipio'] = df_dados_seade_2021['municipio'].astype('category')

# Separa dos códigos do IBGE apenas aqueles de São Paulo
df_dados_cod_municipio_ibge_sp = df_dados_cod_municipio_ibge[df_dados_cod_municipio_ibge['UF'] == 35]

# Cruzar com o código de Municipios do IBGE para trazer o código do Municipio

'''
    Criar uma função para retirar caracteres especiaos
'''

def limpar_texto(texto):
    # Remover acentos
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    # Remover caracteres especiais (mantém letras, números e espaços)
    texto = re.sub(r'[^a-zA-Z0-9\s]', '', texto)
    texto = texto.lower()
    return texto

# Converte para minusculo o municipio sem caracteres especiais dos dois dataframes
df_dados_cod_municipio_ibge_sp['nome_limpo_municipio'] = df_dados_cod_municipio_ibge_sp['Nome_Município'].apply(limpar_texto)
df_dados_seade_2021['nome_limpo_municipio'] = df_dados_seade_2021['municipio'].apply(limpar_texto)

# Faz o join para pegar o codigo do municipio e levar para o dataframe SEADE
df_dados_seade_sp_ibge = pd.merge(df_dados_cod_municipio_ibge_sp, df_dados_seade_2021, on="nome_limpo_municipio")

df_dados_seade_sp_ibge.info()

# Escolher as colunas finais do dataframe SEADE
# Código Município Completo               
# municipio                             
# agropecuaria                          
# industria                             
# administracao_publica                  
# servicos                              
# impostos                              
# pib                                    
# pib_per_capita                        

df_dados_seade_sp_ibge_final = df_dados_seade_sp_ibge[['Código Município Completo', 'municipio', 
                                   'agropecuaria', 'industria', 'administracao_publica', 
                                   'servicos','impostos','pib', 'pib_per_capita']]


df_dados_seade_sp_ibge_final.rename(columns= {'Código Município Completo':'cod_ibge'}, inplace=True)

########################################################################################################
# Padronizar (Z-score) os campos relativos aos valores do PIB para facilitar a convergencia do modelo  #
######################################################################################################## 
# Agropecuaria
df_dados_seade_sp_ibge_final['agropecuaria'] = (df_dados_seade_sp_ibge_final['agropecuaria'] - df_dados_seade_sp_ibge_final['agropecuaria'].mean()) / df_dados_seade_sp_ibge_final['agropecuaria'].std()

# Indústria
df_dados_seade_sp_ibge_final['industria'] = (df_dados_seade_sp_ibge_final['industria'] - df_dados_seade_sp_ibge_final['industria'].mean()) / df_dados_seade_sp_ibge_final['industria'].std()

# Adm. Publica
df_dados_seade_sp_ibge_final['administracao_publica'] = (df_dados_seade_sp_ibge_final['administracao_publica'] - df_dados_seade_sp_ibge_final['administracao_publica'].mean()) / df_dados_seade_sp_ibge_final['administracao_publica'].std()

# Serviços
df_dados_seade_sp_ibge_final['servicos'] = (df_dados_seade_sp_ibge_final['servicos'] - df_dados_seade_sp_ibge_final['servicos'].mean()) / df_dados_seade_sp_ibge_final['servicos'].std()

# Impostos
df_dados_seade_sp_ibge_final['impostos'] = (df_dados_seade_sp_ibge_final['impostos'] - df_dados_seade_sp_ibge_final['impostos'].mean()) / df_dados_seade_sp_ibge_final['impostos'].std()

# PIB
df_dados_seade_sp_ibge_final['pib'] = (df_dados_seade_sp_ibge_final['pib'] - df_dados_seade_sp_ibge_final['pib'].mean()) / df_dados_seade_sp_ibge_final['pib'].std()

# Pib Per capita
df_dados_seade_sp_ibge_final['pib_per_capita'] = (df_dados_seade_sp_ibge_final['pib_per_capita'] - df_dados_seade_sp_ibge_final['pib_per_capita'].mean()) / df_dados_seade_sp_ibge_final['pib_per_capita'].std()


##############################################################################
#                  Término tratamento SEADE                                  #
##############################################################################



#%%


'''
##############################################################################
#                  Inicio tratamento PNUD                                    #
##############################################################################
'''

#df_dados_pnud_2010.info()

# Filtra apenas dados do estado de São Paulo
df_dados_pnud_2010_sp = df_dados_pnud_2010[df_dados_pnud_2010['Estado']=='SP']

# Cria uma coluna com o nome do municipio em lower sem acentos
df_dados_pnud_2010_sp['nome_limpo_municipio'] = df_dados_pnud_2010_sp['Município'].apply(limpar_texto)

# Acrescento o código do Municipio
df_dados_pnud_2010_ibge_sp = pd.merge(df_dados_cod_municipio_ibge_sp, df_dados_pnud_2010_sp, on="nome_limpo_municipio")

df_dados_pnud_2010_ibge_sp_final = df_dados_pnud_2010_ibge_sp[['Código Município Completo', 'IDHM 2010', 
                                   'IDHM Renda 2010', 'IDHM Longevidade 2010', 'IDHM Educação 2010']]

df_dados_pnud_2010_ibge_sp_final.rename(columns= {'Código Município Completo':'cod_ibge', 'IDHM 2010':'idhm_2010', 
                                   'IDHM Renda 2010':'idhm_renda_2010', 'IDHM Longevidade 2010':'idhm_longevidade_2010',
                                   'IDHM Educação 2010': 'idhm_educacao_2010' }, inplace=True)

##############################################################################
#                  Término tratamento PNUD                                   #
##############################################################################


#%%


'''
##############################################################################
#                  Merge Dataframes SIM, SEADE e PNUD                        #
##############################################################################
'''


# Faz a tipagem das colunas chave para string
df_dados_seade_sp_ibge_final['cod_ibge'] = df_dados_seade_sp_ibge_final['cod_ibge'].astype('str')
df_dados_pnud_2010_ibge_sp_final['cod_ibge'] = df_dados_pnud_2010_ibge_sp_final['cod_ibge'].astype('str')
df_dados_sim_2024_sp_final['cod_ibge'] = df_dados_sim_2024_sp_final['cod_ibge'].astype('str')

# Registro que podem ter ficado ausentes entre SEADE e PNUD
set1 = set(df_dados_seade_sp_ibge_final['cod_ibge'])
set2 = set(df_dados_pnud_2010_ibge_sp_final['cod_ibge'])

so_em_seade = set1 - set2
so_em_pnud = set2 - set1

'''
Estes Municípios não possuem registros de IDH no PNUD 2010

cod_ibge municipio
350660	Biritiba Mirim
351500	Embu das Artes
351610	Florínea
355000	São Luiz do Paraitinga

'''

# Merge dos três dataframes para dar início à análise
#df_dados_sim_seade_pnud_ibge = df_dados_sim_2024_sp_final.merge(df_dados_seade_sp_ibge_final, on= 'cod_ibge').merge(df_dados_pnud_2010_ibge_sp_final, on = 'cod_ibge')

# converte código ibge para category
#df_dados_sim_seade_pnud_ibge = df_dados_sim_seade_pnud_ibge['cod_ibge'].astype('category')

#df_dados_sim_seade_pnud_ibge.info()

# merge feito em duas etapas 
df_dados_seade_pnud_ibge = pd.merge(df_dados_seade_sp_ibge_final, df_dados_pnud_2010_ibge_sp_final, on='cod_ibge', how='left')
df_dados_sim_seade_pnud_ibge = pd.merge(df_dados_sim_2024_sp_final, df_dados_seade_pnud_ibge, on= 'cod_ibge', how='left')

#%%




