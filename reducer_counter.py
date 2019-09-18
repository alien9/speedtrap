#!/usr/bin/env python

# equipamento veiculo

import sys,re
radar_atual = ""
#data_atual = ""
#tipo_atual = ""
count_atual = 0
for line in sys.stdin:
    line = line.strip()
    a = re.split('\t', line)
    if len(a)==2:
        radar=a[0]
        n=a[1]
        if radar_atual == radar:
                count_atual+=int(n)
        else:
            if count_atual > 0:
                print "%s\t%s" % (radar_atual, str(count_atual))
            radar_atual = radar
            count_atual = int(n)
if count_atual>0:
    print "%s\t%s" % (radar_atual, str(count_atual))