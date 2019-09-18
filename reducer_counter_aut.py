#!/usr/bin/env python

# equipamento veiculo

import sys,re
radar_atual = ""
#data_atual = ""
#tipo_atual = ""
count_atual = 0
autuacoes_atual=0
for line in sys.stdin:
    line = line.strip()
    a = re.split('\t', line)
    if len(a)==3:
        radar=a[0]
        n=a[1]
        autuacoes=a[2]
        if radar_atual == radar:
                count_atual+=int(n)
                autuacoes_atual+=int(autuacoes)
        else:
            if count_atual > 0:
                print "%s\t%s\t%s" % (radar_atual, str(count_atual), str(autuacoes_atual))
            radar_atual = radar
            count_atual = int(n)
            autuacoes_atual = int(autuacoes)
if count_atual>0:
    print "%s\t%s\t%s" % (radar_atual, str(count_atual), str(autuacoes_atual))