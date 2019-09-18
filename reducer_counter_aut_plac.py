#!/usr/bin/env python

# equipamento veiculo

import sys,re
radar_atual = ""
#data_atual = ""
#tipo_atual = ""
count_atual = 0
autuacoes_atual=0
placas_atual=0
for line in sys.stdin:
    line = line.strip()
    a = re.split('\t', line)
    if len(a)==4:
        radar=a[0]
        n=a[1]
        autuacoes=a[2]
        placas=a[3]
        if radar_atual == radar:
                count_atual+=int(n)
                autuacoes_atual+=int(autuacoes)
                placas_atual+=int(placas)
        else:
            if count_atual > 0:
                print "%s\t%s\t%s\t%s" % (radar_atual, str(count_atual), str(autuacoes_atual), str(placas_atual))
            placas_atual = int(placas)
            radar_atual = radar
            count_atual = int(n)
            autuacoes_atual = int(autuacoes)
if count_atual>0:
    print "%s\t%s\t%s\t%s" % (radar_atual, str(count_atual), str(autuacoes_atual), str(placas_atual))