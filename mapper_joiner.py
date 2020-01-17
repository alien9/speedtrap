#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys,re
import csv
for line in sys.stdin:
    line = line.strip()
    match = re.search(
        '(?P<setor>\w{2})(?P<data>\d{8})(?P<hora>\d{6})(?P<local>\d{4})(?P<faixa>\d{1})(?P<xis>\d{1})(?P<serial>\d{7})(?P<tipo_registro>\d{1})(?P<placa>\w{7})(?P<tipo_veiculo>[\d|\s]{1})(?P<classe_veiculo>[\d|\s]{1})(?P<comprimento>[\d|\s]{3})(?P<velocidade>[\d|\s]{3})(?P<tempo_ocupacao>[\d|\s]{5})(?P<velocidade_media>[\d|\s]{3})$',
        line)
    if match is not None:
        print "%s\t%s" % (
            line, "1"
        )