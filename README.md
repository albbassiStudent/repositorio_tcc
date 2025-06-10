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
[Classificação Internacional de Doenças](http://www2.datasus.gov.br/cid10/V2008/descrcsv.htm) - DATASUS
[Portal Transparência] (https://portaldatransparencia.gov.br/transferencias/consulta?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&de=01%2F01%2F2024&ate=31%2F12%2F2024&uf=SP&funcao=10&colunasSelecionadas=linkDetalhamento%2Cuf%2Cmunicipio%2Ctipo%2CtipoFavorecido%2Cacao%2ClinguagemCidada%2CgrupoDespesa%2CelementoDespesa%2CmodalidadeDespesa%2Cvalor&ordenarPor=mesAno&direcao=desc) - Apenas dados SPO

### Variáveis ####

##### Primeiro nível ##### 

- Sexo,
- Raça/Cor,
- Idade,
- Cód. Mun. Res,
- Causa Básica - > +- por assunto / pelo menos 5 (infarto, pulmonar, trato urinario e neoplasias e outros) - Em uma ocorrêcia de morte a chance de ser uma das causas

##### Segundo Nível #####

*- PNUD 2010 IDHM,
*- PNUD 2010 IDHM Renda,
*- PNUD 2010 IDHM Longevidade,
*- PNUD 2010 IDHM Educação

Procurar variaveis de saude a nivel de municipio

#### Resultados Esperados ####

- Identificação de fatores de segundo nas principais determinantes da mortalidade por doenças crônicas;
- Efeitos contextuais mensurados e visualizados geograficamente;
- Comparação robusta entre modelos simples e multinível;

#### Hipótese #####
- H0 - As ocorrências de mortes por DCNT no estado de São Paulo *não* apresentam variação aleatória significativa entre os municípios 
- H1 - As ocorrências de mortes por DCNT no estado de São Paulo apresentam variação aleatória significativa entre os municípios.
