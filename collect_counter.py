#!/usr/bin/env python
# -*- coding: utf-8 -*-

#465520180201210	9

import os, sys, re, psycopg2, csv
from config import cstring
conn = psycopg2.connect(cstring)
cur = conn.cursor()

if not os.path.exists("contagens.csv"):
    cur.execute("select nextval('contagens_id_seq'::regclass)")
    vid=cur.fetchone()[0]
    file_contagens=open("contagens.csv", "w+", newline='')
    writer_contagens=csv.writer(file_contagens)
    n=0

    for line in sys.stdin:
        line = line.strip()

        m = re.search('(?P<local>\d{4})(?P<faixa>\d{1})(?P<ano>\d{4})(?P<mes>\d{2})(?P<dia>\d{2})(?P<hora>\d{2})(?P<tipo>\d{1})\t(?P<contagem>\d+)\t(?P<autuacoes>\d+)\t(?P<placas>\d+)', line)
        try:
            writer_contagens.writerow([
                vid,
                m.group("local"),
                m.group("faixa"),
                m.group("tipo"),
                m.group("contagem"),
                m.group("autuacoes"),
                m.group("placas"),
                "%s-%s-%s %s:00:00" % (m.group("ano"),m.group("mes"),m.group("dia"),m.group("hora"))
            ])
            vid+=1
        except Exception as x:
            print(str(x))
            print("registro mal formado")
            exit();
        if re.search("00000$", str(n)):
            print("\n"+str(n))
        n+=1


    file_contagens.close()
with open("contagens.csv", 'r') as f:
    cur.copy_from(f, 'contagens', sep=',')


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
