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

# Instalação dos pacotes a serem utilizados

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



#%%
##############################################################################
##############################################################################
#                ESTIMAÇÃO DE MODELOS HIERÁRQUICOS LINEARES                  #
#                    DE DOIS NÍVEIS COM DADOS AGRUPADOS                      #
##############################################################################
##############################################################################

##############################################################################
#        DESCRIÇÃO E EXPLORAÇÃO DO DATASET 'SIM_INDICADORES_MUNICIPAIS'      #
##############################################################################

'''
##### Nível 1 – **Indivíduo (registro de óbito)**

 Idade
 Sexo
 Escolaridade
 Raça/cor
 Local de ocorrência do óbito
 CID-10 (grupo de causa)


##### Nível 2 – **Município ou Região**
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
Função para imprimir as bibliotecas utilizadas no código inclusive R
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
     Imprime a versão das bibliotecas utilizadas apenas do PYTHON e informações do sistema operacional 
'''
#Registrar os pacotes e versões utilizados
%load_ext watermark

#informações do Sistema operacional, compilador e implementação do Python
%watermark -v -m

# Imprime a versão das bibliotecas do python   
%watermark --iversions   

 
#%%
'''
    Criação de variáveis para guarda das url de download dos arquivos

'''
# DATASUS
url = "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SIM/DO24OPEN.csv"

#SEADE
url2 = "https://repositorio.seade.gov.br/dataset/1bd90672-72a8-47cb-a34d-ab9eb703735d/resource/c2eb14df-60e0-44d6-9e7a-9fcdc339c4ad/download/pib-municipios-2021_site.xlsx"

#Código Municípios IBGE
url3 = "https://github.com/albbassiStudent/repositorio_tcc/raw/refs/heads/main/RELATORIO_DTB_BRASIL_2024_DISTRITOS.xls"

#PNUD IDH
url4 = "https://github.com/albbassiStudent/repositorio_tcc/raw/refs/heads/main/idh_municipios_2010_atlas_desenvolvimento_humano.csv" 


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
        df_dados_sim_2024 = pd.read_csv(caminho)
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
        chunk_size = 10  # 1 0B por iteração

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
        df_dados_seade_2021 = pd.read_excel(caminho2, usecols='A:E,G:H, I', skiprows=12, header=None, names=['municipios', 'agropecuaria', 'industria', 'administracao_publica', 'servicos', 'impostos', 'pib','pib_per_capita'])
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
    filename3 = "dados_cod_mun_ibge.xls"
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

        # Ler o XLS
        df_dados_cod_municipio_ibge = pd.read_excel(caminho3, engine='xlrd')
    else:
        print(f"Erro ao baixar arquivo: código {response3.status_code}")

#################################################################
#               FIM EXTRAÇÃO DADOS RFB                          #
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
        df_dados_pnud_2010 = pd.read_csv(caminho4)
    else:
        print(f"Erro ao baixar arquivo: código {response.status_code}")
    
#################################################################
#               FIM EXTRAÇÃO DADOS IDH PNUD                     #
#################################################################



#%%
with tempfile.TemporaryDirectory() as temp_dir:
    filename4 = "dados_pnud_idh_2010.csv"
    filepath = os.path.join(temp_dir, filename4)  # Corrigido: filename -> filename4

    response4 = requests.get(url4)

    # Download da base de dados PNUD IDH    
    if response4.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response4.content)

        print(f"\nDownload completo! Arquivo salvo em: {filepath}")
        caminho4 = filepath

        # Lê o CSV e guarda os dados em um DataFrame
        df_dados_pnud_2010 = pd.read_csv(caminho4, sep=';',encoding='latin1')
    else:
        print(f"Erro ao baixar arquivo: código {response4.status_code}")  # Corrigido: response -> response4



#%%
# Dataframe SIM
df_dados_sim_2024.keys()


#%%
# Ajuste nos nomes das colunas do Dataframe PNUD

df_dados_pnud_2010.rename(columns={
    'Município': 'municipio',
    'IDHM 2010': 'idhm',
    'IDHM\nRenda\n2010':'idhm_renda',
    'IDHM Longevidade 2010':'idhm_longevidade',
    'IDHM Educação 2010': 'idhm_educacao',
    'Estado':'estado'
}, inplace=True)

# filtrar apenas os registro do estado de São Paulo
df_dados_pnud_2010_sp = df_dados_pnud_2010[df_dados_pnud_2010['estado'] == 'SP']

#%%

df_dados_pnud_2010_sp.head()

