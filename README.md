![USP ESALQ](img/usp.jpeg)


#### Repositório do TCC em Data Science and Analytics a ser entregue como parte das disciplinas do MBA da USP ESALQ ####

**Orientado: Alex de Lima Bassi** <BR>
**Orientador: Gustavo Dantas Lobo**


#### Título ######

- Fatores Individuais e Contextuais Associados à Mortalidade por Doenças Crônicas em Adultos no Brasil: Uma Abordagem com Regressão Logística Multinomial Multinível"

#### Área de Concentração ####

Data Science and Analytics – Estatística Aplicada à Demografia e Saúde Pública

#### Justificativa ####

Doenças crônicas não transmissíveis (DCNTs), como doenças cardiovasculares, diabetes e câncer, são responsáveis pela maioria das mortes em adultos no Brasil. A mortalidade por essas causas varia significativamente de acordo com fatores individuais e fatores contextuais. A modelagem multinível obtém êxito onde modelos estatísticos convencionais falham pois consegue capturar os efeitos da estrutura hierárquica dos dados, como pacientes inseridos em municípios ou regiões. Sendo assim, este tipo de modelagem é ideal para entender como esses fatores interagem em diferentes níveis, permitindo uma análise mais precisa e direcionada.

#### Objetivos ####

##### Objetivo Geral #####

Investigar os determinantes individuais e contextuais da mortalidade por doenças crônicas em adultos brasileiros por meio da regressão logística multinível.

##### Objetivos Específicos #####

- Integrar e preparar uma base de dados sobre mortalidade por DCNTs com estrutura multinível;
- Estimar modelos de regressão logística multinível com variáveis em níveis individual e municipal;
- Avaliar a influência de desigualdades de PIB e IDH nas ocorrências;
- Comparar os resultados com um modelo logístico tradicional.

#### Bases de Dados ####

[Sistema de Informações sobre Mortalidade](http://sim.saude.gov.br/default.asp) - 2024 <br>
[Programa das Nações Unidas para o Desenvolvimento](https://www.undp.org/pt/brazil/pnud-no-brasil) - 2010 <br>
[Sistema Estadual de Análise de Dados -SP](https://www.seade.gov.br/institucional/fundacao-seade) - 2021 <br>
[Classificação Internacional de Doenças](http://www2.datasus.gov.br/cid10/V2008/descrcsv.htm) - DATASUS <br>
[Portal Transparência](https://portaldatransparencia.gov.br/) - Consulta Recursos transferidos Saúde Municípios São Paulo 2024 <br>
[Estatisticas IBGE](https://www.ibge.gov.br/estatisticas/todos-os-produtos-estatisticas.html) <br>
[Cadastro Nacional de Estabelecimentos de Saúde](https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/CNES/cnes_estabelecimentos.zip) -  Open DATASUS (Arquivo Zip) <br>
[API Dados Abertos DATASUS](https://apidadosabertos.saude.gov.br/v1/#) <br>
[População Municipios IBGE](https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html) - 2024
[Qualidade do ar](https://energiaeambiente.org.br/qualidadedoar/)

### Variáveis ####

##### Primeiro nível ##### 

- Sexo,
- Raça/Cor,
- Idade,
- Cód. Mun. Res,
- Causa Básica

##### Segundo Nível #####

- PNUD 2010 IDHM, <br>
- PNUD 2010 IDHM Renda, <br>
- PNUD 2010 IDHM Longevidade, <br>
- PNUD 2010 IDHM Educação <br>
- Indice de GINI 2010 <br>
- Nº de Leitos 2024 <br>
- Transferências da União 2024  


Procurar variaveis de saude a nivel de municipio

#### Resultados Esperados ####

- Identificação de fatores de segundo nas principais determinantes da mortalidade por doenças crônicas;
- Efeitos contextuais mensurados e visualizados geograficamente;
- Comparação robusta entre modelos simples e multinível;

#### Hipótese #####
- H0 - As ocorrências de mortes por DCNT no estado de São Paulo *não* apresentam variação aleatória significativa entre os municípios 
- H1 - As ocorrências de mortes por DCNT no estado de São Paulo apresentam variação aleatória significativa entre os municípios.
