#!/usr/bin/env python
# -*- coding: utf-8 -*-
#L1 2014 11 12 00 40 50 6600 2 0000153 0 FFE8349 1 0 024 142 00000 000

import sys,re
import csv

h=[{},{},{},{}]

with open("placas.txt", "r") as fu:
    for line in fu:
        placa, tipo, pseudoplaca = re.split('\t', line.strip())
        h[int(tipo)][placa]=pseudoplaca

for line in sys.stdin:
    d=re.split('(.{29})(.{7})(.{1})', line.strip())
    placa = d[2]
    tipo = int(d[3])
    pseudoplaca = "       "
    if not re.match('\s+', placa):
        if not placa in h[tipo]:
            h[tipo][placa]=len(h[tipo].keys())
            pseudoplaca = h[tipo][placa]
            f = open("placas.txt", "a")
            f.write("%s\t%s\t%s\n" % (placa,tipo, pseudoplaca))
            f.close()
        else:
            pseudoplaca = h[tipo][placa]
    print "%s%s%s%s" % (d[1], str(pseudoplaca).zfill(7), d[3], d[4])