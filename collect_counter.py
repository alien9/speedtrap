#!/usr/bin/env python
# -*- coding: utf-8 -*-

#465520180201210	9

import sys, re, psycopg2

cstring="dbname='bigrs' user='tiago' host='localhost' port='5432'"# password='bigrs'"
conn = psycopg2.connect(cstring)
cur = conn.cursor()

n=0

for line in sys.stdin:
    line = line.strip()
    print("%s %s" % (line, str(n)), end="\r"
    n+=1
    m = re.search('(?P<local>\d{4})(?P<ano>\d{4})(?P<mes>\d{2})(?P<dia>\d{2})(?P<hora>\d{2})(?P<tipo>\d{1})\t(?P<contagem>\d+)\t(?P<autuacoes>\d+)\t(?P<placas>\d+)', line)
    try:
        cur.execute(
            "INSERT INTO radar.contagens(data_e_hora, localidade, tipo, contagem, autuacoes,placas) VALUES (%s, %s, %s, %s, %s, %s)",
            ("%s-%s-%s %s:00:00" % (m.group("ano"), m.group("mes"), m.group("dia"), m.group("hora")), m.group("local"), m.group("tipo"), m.group("contagem"), m.group("autuacoes"), m.group("placas"),)
        )
        #conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        cur.execute(
            "update radar.contagens set contagem=contagen+%s, autuacoes=autuacoes+%s, placas=placas+%s where data_e_hora=%s and localidade=%s and tipo=%s",
            (m.group("contagem"), m.group("autuacoes"),m.group("placas"), "%s-%s-%s %s:00:00" % (m.group("ano"), m.group("mes"), m.group("dia"), m.group("hora")), m.group("local"), m.group("tipo"),)
        )
        conn.commit()
    except Exception as x:
        print(str(x))
        print("registro mal formado")
        exit();
    if re.search("00000$", str(n))):
        print("\n"+str(n))
conn.commit()