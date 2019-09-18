#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,re
from pyspark.sql.types import Row


def countmap(line):
    line = line.strip()
    # match = re.search('(?P<setor>.{2})(?P<data>.{8})(?P<hora>.{6})(?P<local>.{4})(?P<faixa>.{1})(?P<serial>.{7})(?P<tipo_registro>.{1})(?P<placa>.{7})(?P<tipo_veiculo>.{1})(?P<classe_veiculo>.{1})(?P<comprimento>.{3})(?P<velocidade>.{3})(?P<tempo_ocupacao>.{5})(?P<velocidade_media>.{3})$', line)
    # pega data e hora (descarta minutos e segundos)
    match = re.search(
        '(?P<setor>L\d{1})(?P<data>\d{10})(?P<hora>\d{4})(?P<local>\d{4})(?P<faixa>\d{1})(?P<xis>\d{1,2})(?P<serial>\d{7})(?P<tipo_registro>\d{1})(?P<placa>[\s|\w]{7})(?P<tipo_veiculo>[\d|\s]{1})(?P<classe_veiculo>[\d|\s]{1})(?P<comprimento>[\d|\s]{3})(?P<velocidade>[\d|\s]{3})(?P<tempo_ocupacao>[\d|\s]{5})(?P<velocidade_media>[\d|\s]{3})$',
        line)
    if match is not None:
        autuado = "0"
        if match.group("tipo_registro") == "1":
            autuado = "1"
        placa = "0"
        if match.group("placa") == "       ":
            placa = "1"
        return "%s%s%s\t%s\t%s\t%s" % (
            match.group("local"), match.group("data"), match.group("tipo_veiculo"), str(1), autuado, placa
        )

def countmap_total(line):
    line = line.strip()
    # match = re.search('(?P<setor>.{2})(?P<data>.{8})(?P<hora>.{6})(?P<local>.{4})(?P<faixa>.{1})(?P<serial>.{7})(?P<tipo_registro>.{1})(?P<placa>.{7})(?P<tipo_veiculo>.{1})(?P<classe_veiculo>.{1})(?P<comprimento>.{3})(?P<velocidade>.{3})(?P<tempo_ocupacao>.{5})(?P<velocidade_media>.{3})$', line)
    # pega data e hora (descarta minutos e segundos)
    match = re.search(
        '(?P<setor>L\d{1})(?P<data>\d{10})(?P<hora>\d{4})(?P<local>\d{4})(?P<faixa>\d{1})(?P<xis>\d{1,2})(?P<serial>\d{7})(?P<tipo_registro>\d{1})(?P<placa>[\s|\w]{7})(?P<tipo_veiculo>[\d|\s]{1})(?P<classe_veiculo>[\d|\s]{1})(?P<comprimento>[\d|\s]{3})(?P<velocidade>[\d|\s]{3})(?P<tempo_ocupacao>[\d|\s]{5})(?P<velocidade_media>[\d|\s]{3})$',
        line)
    if match is not None:
        autuado = "0"
        if match.group("tipo_registro") == "1":
            autuado = "1"
        placa = "0"
        if match.group("placa") == "       ":
            placa = "1"
        return Row(key="L%s%s%s" % (match.group("local"), match.group("data"), match.group("tipo_veiculo"),), value=1)
