#### Repositório do TCC em Data Science and Analytics a ser entregue como parte das disciplinas do MBA da USP ESALQ ####


#### Título ######

- Fatores Individuais e Contextuais Associados à Mortalidade por Doenças Crônicas em Adultos no Brasil: Uma Abordagem com Regressão Logística Multinível"

#### Área de Concentração ####

Data Science and Analytics – Estatística Aplicada à Demografia e Saúde Pública

#### Justificativa ####

Doenças crônicas não transmissíveis (DCNTs), como doenças cardiovasculares, diabetes e câncer, são responsáveis pela maioria das mortes em adultos no Brasil. A mortalidade por essas causas varia significativamente de acordo com fatores individuais e fatores contextuais. A modelagem multinível obtém êxito onde modelos estatísticos convencionais falham pois consegue capturar os efeitos da estrutura hierárquica dos dados, como pacientes inseridos em municípios ou regiões. Sendo assim, este tipo de modelagem é ideal para entender como esses fatores interagem em diferentes níveis, permitindo uma análise mais precisa e direcionada.

#### Objetivos ####

##### Objetivo Geral #####

Investigar os determinantes individuais e contextuais da mortalidade por doenças crônicas em adultos brasileiros por meio da regressão logística multinível.

##### Objetivos Específicos #####

Integrar e preparar uma base de dados sobre mortalidade por DCNTs com estrutura multinível;
Estimar modelos de regressão logística multinível com variáveis em níveis individual e municipal;
Avaliar a influência de desigualdades de PIB e IDH nas ocorrências;
Comparar os resultados com um modelo logístico tradicional.

#### Bases de Dados ####

- SIM dados 2024 
- PNUD dados de 2010
- SEADE dados de 2024

### Variáveis ####

##### Primeiro nível ##### 

- Sexo,
- Raça/Cor,
- Idade,
- Cód. Mun. Res,
- Causa Básica

##### Segundo Nível #####

- Total agropecuária,                          
- Total indústria,                             
- Total Administração pública,                  
- Total Serviços,                              
- Total impostos,                              
- PIB Total,                                    
- PIB Per capita,  
- IDHM 2010,
- IDHM Renda 2010,
- IDHM Longevidade 2010,
- IDHM Educação 2010


#### Resultados Esperados ####

Identificação de fatores de segundo nas principais determinantes da mortalidade por doenças crônicas;
Efeitos contextuais mensurados e visualizados geograficamente;
Comparação robusta entre modelos simples e multinível;

#### Hipótese #####
- H0 - As ocorrências de mortes por DCNT no estado de São Paulo *não* apresentam variação aleatória significativa entre os municípios 
- H1 - As ocorrências de mortes por DCNT no estado de São Paulo apresentam variação aleatória significativa entre os municípios.
