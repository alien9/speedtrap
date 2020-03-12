#!/usr/bin/env python
# -*- coding: utf-8 -*-

#465520180201210	9

import sys, re, psycopg2

cstring="dbname=radartona user='smt_user' user='smt_user' host='10.35.200.226' port='5432' password='smt_user'"
conn = psycopg2.connect(cstring)
cur = conn.cursor()

#cur.execute("select nextval('contagens_id_seq'::regclass)")
#vid=cur.fetchone()[0]
#print(vid)
#exit()

n=0

for line in sys.stdin:
    line = line.strip()
    n += 1
    m = re.search('(?P<local>\d{4})(?P<faixa>\d{1})(?P<ano>\d{4})(?P<mes>\d{2})(?P<dia>\d{2})(?P<hora>\d{2})(?P<tipo>\d{1})\t(?P<contagem>\d+)\t(?P<autuacoes>\d+)\t(?P<placas>\d+)', line)
    try:
        cur.execute(
            "INSERT INTO contagens(data_e_hora, localidade, faixa, tipo, contagem, autuacoes,placas) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            ("%s-%s-%s %s:00:00" % (m.group("ano"), m.group("mes"), m.group("dia"), m.group("hora")), m.group("local"), m.grooup("faixa"),m.group("tipo"), m.group("contagem"), m.group("autuacoes"), m.group("placas"),)
        )
        #conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        cur.execute(
            "update contagens set contagem=contagen+%s, autuacoes=autuacoes+%s, placas=placas+%s where data_e_hora=%s and localidade=%s and tipo=%s and faixa=%s",
            (m.group("contagem"), m.group("autuacoes"),m.group("placas"), "%s-%s-%s %s:00:00" % (m.group("ano"), m.group("mes"), m.group("dia"), m.group("hora")), m.group("local"), m.group("tipo"),m.group("faixa"))
        )
        conn.commit()
    except Exception as x:
        print(str(x))
        print("registro mal formado")
        exit();
    if re.search("00000$", str(n)):
        print("\n"+str(n))
conn.commit()


"""
                                       Table "public.contagens"
   Column    |           Type           | Collation | Nullable |                Default
-------------+--------------------------+-----------+----------+---------------------------------------
 id          | integer                  |           | not null | nextval('contagens_id_seq'::regclass)
 localidade  | integer                  |           |          |
 faixa       | integer                  |           |          |
 tipo        | integer                  |           |          |
 contagem    | integer                  |           |          |
 autuacoes   | integer                  |           |          |
 placas      | integer                  |           |          |
 data_e_hora | timestamp with time zone |           |          |
Indexes:
    "contagens_pkey" PRIMARY KEY, btree (id)


"""
