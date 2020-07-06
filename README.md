 
 # HDFSCameraData
 


## Introdução
O sistema de monitoramento de tränsito de São Paulo conta com detectores e câmeras para registrar a passagem dos veículos. São medidas as velocidades instantâneas dos veículos e as placas são interpretadas. O registro resultante é arquivado num formato de campos delimitados por tamanho em formato texto.
O HDFSCameraData consiste em uma base de dados em HDFS (Hadoop File System). Este formato é empregado para consultas agregadas de dados, permitindo extrair informações em um contexto amplo a partir dos dados gerados pelas câmeras e detectores de velocidade. Tais informações estão demonstradas no âmbito deste projeto com a extração dos dados para a API criada no decorrer das Radartona. Esta base de dados relacional foi projetada para utilização pelo front-end da API que for desenvolvida.  

As vantagens da utilização do HDFS são bem aproveitadas neste projeto, que permite explorar os dados de forma a empregar computação distribuída, com um número arbitrário de instâncias contendo os arquivos gerados. Esta forma de armazenamento combina o uso adequado de compactação nos dados  com a redundância de armazenamento dos mesmos, permitindo um uso racional do sistema de arquivos para backup e armazenamento de dados, não somente os gerados pelo sistema de monitoramento de tränsito de São Paulo mas também para qualquer base de dados não relacionais. 

## Objetivos do Procedimento
A execução dos scripts deve gerar um banco de dados relacional contendo dois modelos de dados:
1) Contagem de veículos por hora por equipamento
Neste formato, as contagens de veículos são agregadas por hora, identificador de equipamento, pista e tipo de veículo. São contabilizadas as placas lidas no conjunto de veículos detectados, isto é, dentre todos os veículos contados para uma hora e local temos a contagem de placas detectadas.
2) Viagens de menos de trinta minutos entre detectores
Este formato contabiliza as viagens detectadas para um mesmo veículo entre os diversos detectores do sistema. O registro contém, além da placa, o tipo de veículo detectado e um conjunto associado ded pontos que fazem parte dos trajetos desenvolvidos pelo veículo.
O embasamento para a criação deste formato de saída é o emprego em simuladores empregados pela CET. 

## Dados Relacionais
Os dados no formato relacional não contêm informação sensível. Criamos registro de viagens por tipo de veículo, e portanto não é possível, a partir da base de dados relacional, rastrear determinado veiculo. 
São criadas trës tabelas, assim descritas:

                                       Table "public.contagens"
| Column       | Type                     |
| ------------ |:------------------------:|
| id           | integer                  |
| localidade   | integer                  |
| faixa        | integer                  |
| tipo         | integer                  |
| contagem     | integer                  |
| autuacoes    | integer                  |
| placas       | integer                  |
| data_e_hora  | timestamp with time zone |


                                       Table "public.viagens"
| Column      | Type                     |
| ----------- |:------------------------:|
| id          | integer                  |
| inicio      | integer                  | 
| data_inicio | timestamp with time zone | 
| final       | integer                  | 
| data_final  | timestamp with time zone | 
| tipo  


                                       Table "public.trajetos"
| Column      | Type                     |
| ----------- |:------------------------:|
| id          | integer                  |
| tipo        | integer                  | 
| data_inicio | timestamp with time zone | 
| data_final  | timestamp with time zone | 
| origem      | integer                  | 
| destino     | integer                  | 
| v0          | integer                  | 
| v1          | integer                  |


Para as viagens, as localidades são identificadas por meio do identificador de cada equipamento.

O Processamento
Os dados são inseridos na base HDFS pela execução de um script. Os arquivos de entrada deverão ser disponibilizados em um mountpoint no sistema de arquivos. O upload é realizado pelo protocolo hdfs executado no bash shell:

`python upload.py <diretorio_arquivos>`

Este script está preparado para receber a localização de um ou mais arquivos .zip. Estes são fornecidos no formato padrão da PRODAM, com  campos delimitados por tamanho fixo. Os arquivos, como são fornecidos pela PRODAM, precisam ser concatenados para gerar um único arquivo para cada um dos quatro setores ou consórcios do sistenma de fiscalização. Esta entrada deve ter o nome de arquivo correspondente à data de geração do mesmo, em formato YYYYMMDD. Após a execução da linha, o arquivo zip deve ser excluído.

`rm -rf< diretorio_arquivos>/*.zip` 

O HDFS é configurado com 10 instâncias rodando Debian 10.0, com 4GB de RAM e 500GB de SSD.  É necessário utilizar o Java 8 (OpenJDK), configurado como padrão em cada uma das instâncias.
O cluster pode ser controlado a partir do console ssh de uma das instâncias.

Geração de Base Relacional

Após fazer o upload podemos ler os arquivos por meio do streaming. Podemos executar o procedimento para totalização dos veículos:

`hduser@node_00:/usr/local/hadoop$ nohup bin/hadoop jar contrib/streaming/hadoop-*streaming*.jar \
-file mapper_counter.py    -mapper mapper_counter.py \
-file reducer_counter.py   -reducer reducer_counter.py \
-input /data/* -output /contagens &`

e para recuperar as viagens de cada veículo:

`hduser@node_00:/usr/local/hadoop$ nohup bin/hadoop jar contrib/streaming/hadoop-*streaming*.jar \
-file mapper.py    -mapper mapper.py \
-file reducer.py   -reducer reducer.py \
-input /data/* -output /viagens &`

Após a execução dsstas rotinas será necessário importar o conjunto resultante. 
Os scripts collect_counter.py e collect_trip.py recebem como oentrada uma varredura nos arquivos CSV gerados na saída do mapreduce.

`Hdfs dfs cat viagens/part00000 | ./collect_trip.py
Hdfs dfs cat contagens/part00000 | ./collect_counter.py`

Após a execução deste procedimento a base estará disponível no PostgreSQL para ser acessada pelas aplicações front-end. 


