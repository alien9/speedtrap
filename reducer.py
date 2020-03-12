#!/usr/bin/env python

# placa equipamento date_e_hora

import sys,re
placa_atual = ""
track_atual = ""
for line in sys.stdin:
    line = line.strip()
    if len(line)>3:
        placa, track = re.split('\t',line)
        if placa and track:
            if placa==placa_atual:
                track_atual=track=track_atual+track
            else:
                print "%s\t%s" % (placa_atual, track_atual)
                placa_atual=placa
                track_atual=track
print "%s\t%s" % (placa_atual, track_atual)