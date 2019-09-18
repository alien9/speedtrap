#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MAPPER INDIVIDUALIZANDO POR PLACA
L1 2014 11 12 00 40 50 6600 2 0000153 0 FFE8349 1 0 024 142 00000 000
L1 2014 11 12 00 40 54 6600 2 0000154 0         1 0 024 142 00000 000

L1 2014 11 01 23:58:11 6660 2 0000855 0 GDM2010 1 0 024 156 00000 000
L1 2014 11 01 23:58:28 6660 2 0000856 0         1 0 024 186 00000 000

Código da empresa 2 AN 1 2 (1)
2 Data 8 N 3 10 AAAAMMDD (1)

3 Hora 6 N 11 16 HHMMSS (1)
 4 Código do local 4 N 17 20 (1)
5 Faixa 1 N 21 21 (1)
6 Número do registro no equipamento

7 N 22 28 (1) e (3)
7 Tipo de registro 1 N 29 29 (1) e (4)
8 Placa do veículo 7 AN 30 36 AAA9999 (1) alterar **
9 Tipo/espécie do veículo 1 N 37 37 (1) e (5)
10 Classificação do tipo de
veículo 1 N 38 38 (1) e (6)
11 Comprimento medido do
veículo 3 N 39 41 Em decímetros (2)
12 Velocidade Pontual 3 N 42 44 Em décimos de metros
por segundo (1)
13 Tempo ocupação 5 N 45 49 Em milissegundos (2)
14 Velocidade Média 3 N 50 52 Em décimos de metros
por segundo (7)
A tabela já está alterada para a versão utilizada no contrato. O documento original (da
licitação) continha tabela diferente

(1) Obrigatório em todos os registros.
(2) Obrigatório apenas se a tecnologia utilizada permitir a sua medição.
(3) Número sequencial exclusivo para cada registro de um mesmo local, gravado no
equipamento no campo, reiniciado todo dia 1º de cada mês.
(4) Tipo do registro gravado no equipamento no campo: 0 = comum = registro de
veículo não infrator; 1 = infrator = registro de veículo infrator; 2 = s/registro =
registro em branco em caso de não passagem de veículo sendo, obrigatórios,
neste caso, os campos de 1 a 7, sendo que os demais campos não deverão ser
informados.
(5) Tipo ou espécie do veículo: moto = 0, passeio = 1, ônibus = 2 ou caminhão = 3.
(6) Classificação de tipo de veículo: leve = 0 ou pesado = 1.
(7) Velocidade média com a qual o veículo percorreu o trecho compreendido entre o
primeiro equipamento, definido como início do trecho de fiscalização da velocidade
média, e o equipamento seguinte.

"""
import sys,re
import csv
for line in sys.stdin:
    line = line.strip()
    match = re.search(
        '(?P<setor>\w{2})(?P<data>\d{8})(?P<hora>\d{6})(?P<local>\d{4})(?P<faixa>\d{1})(?P<xis>\d{1})(?P<serial>\d{7})(?P<tipo_registro>\d{1})(?P<placa>\w{7})(?P<tipo_veiculo>[\d|\s]{1})(?P<classe_veiculo>[\d|\s]{1})(?P<comprimento>[\d|\s]{3})(?P<velocidade>[\d|\s]{3})(?P<tempo_ocupacao>[\d|\s]{5})(?P<velocidade_media>[\d|\s]{3})$',
        line)
    if match is not None:
        print "%s\t%s%s%s%s%s|" % (
            match.group("placa"),match.group("local").zfill(4),match.group("data"),match.group("hora"),match.group("tipo_veiculo"),match.group("velocidade")
        )