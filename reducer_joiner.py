#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys,re
import csv

key_atual=""
origem_atual=""
line_atual=""
for line in sys.stdin:
    line = line.strip()
    if len(line)>3:
        match = re.search(
            '(?P<key>\d{19})\t(?P<line>[^\t]+)\t(?P<origem>\d{1})',
            line)
        if match is not None:
            key=match.group("key")
            line=match.group("line")
            origem=match.group("origem")
            if key==key_atual:
                print "%s\t%s\t%s\t%s" % (
                    key, line_atual, origem_atual, line, origem,
                )
            origem_atual=origem
            line_atual=line
            key_atual=key
