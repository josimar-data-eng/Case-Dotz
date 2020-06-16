# Case-Dotz

Abaixo segue a explicação sobre como foi desenvolvido o teste solicitado, a criação da Arquitetura e do Modelo Conceitual.

### Modelo Conceitual

Pra definir o modelo conceitual, optei por trabalhar com os 3 arquivos do caso transformando-os em tabela e fazendo a ligação entre elas.

Apesar de perceber que os arquivos não estavam normalizados para serem representados diretamente como tabelas, dado que haviam problema relacionados às chaves, optei dessa forma pois a especificação estava um pouco geral, faltando algumas informações que pudessem otimizar o modelo conceitual, e o tempo curto.

O arquivo 'Modelo Conceitual.PNG' representa o fluxo do modelo conceitual.

### Arquitetura Cloud

Para definir a melhor arquitetura, tínhamos, inicialmente, 6 ferramentas que poderiam ser escolhidas, mas cada uma com suas peculiaridades, sejam relacionadas à preço, à estrutura dos dados ou a aceitação de grande volumes de dados.

Dado que a ideia é um processo end-to-end, a primeira ponta da cadeia precisa de uma Storage Solution, que pelo GCP, temos 7 opções, mas para o nosso caso escolhi a Cloud Storage por ser a mais barata, totalmente gerenciável e foi desenvolvida para dados não estruturados, que nosso caso seria o CSV (que também é visto como um dado semi-estruturado). Este será nosso Datalake.

Tínhamos a opção da Cloud Spanner ou Cloud Sql para trabalhar com sistema transacional, mas, creio que a linha analítica é uma boa opção para este caso. Sem contar que teríamos problemas relacionados à preço (Cloud Spanner) e processamento de grandes volumes de dados(Cloud Sql)

Como processo de ETL usamos o Dataflow, como soliticado no requisito, que lê os 3 arquivos do Cloud Storage e cria 3 tabelas no BigQuery com alguns tratamentos de Data e limpeza de campos.

O Bigquery foi escolhido como nosso Datawarehouse, pois essa é a forte indicação da google e realmente é a melhor opção que temos para ambiente analítico, sendo totalmente gerenciável e processando grande volume de dados.

Como opção de ferramente de BI, usaremos o Data Studio, onde serão criados relatórios gerenciais para acompanhamento de vendas e aceita fontes de dados como Mysql, BigQuery, Cloud Sql, Google Sheets e Google Analytics.

O arquivo 'Arquitetura Cloud.PNG' representa o desenho da arquitetura.


### Ingestão dos Dados

O programa é dividido em 2 etapas , a primeira se refere ao módulo 'IngestData.py' e a segunda ao módulo 'CleanData.py'.

O módulo 'IngestData.py' realiza todas os imports necessários e passa os argumentos que o Dataflow necessita para execução.

Há a criação de uma função que lê o arquivo CSV e o separada através do delimitador ',' e cria a linha a ser processada junto com o head que também é passado na função.

O Pipeline nesse caso é simples, onde ele lê o arquivo CSV, faz a separação das colunas através do delimitador e grava uma tabela no BigQuery. Faz esse processo para os 3 arquivos.

O módulo 'CleanData.py' executa via Datafow 3 queries (1 para cada tabela) fazendo o tratamento dos campos e deixando as tabelas prontas para serem analisadas.

As queries se encontram no repositório: query_normatiza_component.sql , query_normatiza_price_quote.sql e query_normatiza_bill_material.sql

### Painel Data Studio

Através da query 'query_insumo_data_studio.sql' executada no BigQuery é criada uma visão dos custos de cotação versus o período, para assim conseguirmos identificar, inicialmente, quais são os períodos que os custos estão alta e tentar, de alguma forma, diminuir esses valores caso não esteja ocorrendo venda por conta do alto custo, ou fomentar as vendas nesse período, caso o resultado seja positivo.

O painel está no arquivo 'Relatório Case Dotz.PNG' .


### Executando o programa

A execução está divida em 3 etapas:

1 - Instalação das dependências do Dataflow, através da execução dos comandos abaixo:
```
- pip install apache-beam
- pip install apache-beam[gcp]
```
2 - Executar o step de ingestão de dados IngestData.py
* O arquivo 'IngestProcessDataFlow.PNG' representa os pipes do Dataflow dessa etapa

3 - Executar o step de limpeza dos dados CleanData.py
* O arquivo 'CleanProcessDataFlow.PNG' representa os pipes do Dataflow dessa etapa

4 - Executar a query 'query_insumo_data_studio.sql' que dará insumo ao painél que atualizará automaticamente
* Sobre esse step, não vi a necessidade de inserir no Dataflow ou outra opção, dada a simplicadade.


### Melhorias

Vejo muitas possibilidades de melhorias nesse processo de ingestão, desde o modelo conceitual até o painel no Data Studio, mas com o tempo curto, não foi possível!

Creio que seria mais interessante "destrinchar" o modelo conceitual, entender mais das regras, e com certeza criar mais tabelas para que o entendimento do negócio ficasse mais estruturado.

Poderíamos criar um processo transacional via Cloud Sql e armazenar as tabelas lá dentro, criando conexão diretas com Dataflow e  BigQuery , deixando o fluxo mais limpo e estruturado, saindo de um ambiente transacional para o Analítico.

Sobre o programa do Dataflow, poderíamos parametrizar mais, deixando o código menor e mais limpo.

Pra finalizar, informo que optei por não focar 100% em apenas um step do processo, e sim fazê-lo por completo (de ponta a ponta) para mostrar que há o conhecimento em todas as camadas.
