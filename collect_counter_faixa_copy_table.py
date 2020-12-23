#!/usr/bin/env python
# -*- coding: utf-8 -*-

#465520180201210	9

import sys, re, psycopg2, csv
from config import cstring
conn = psycopg2.connect(cstring)
cur = conn.cursor()
try:
    cur.execute("DROP INDEX if exists public.contagens_data;\
        DROP INDEX if exists public.contagens_data_e_hora;\
    DROP INDEX if exists public.contagens_localidade;")
except:
    print("indexes not dropped")

cur.execute("select max(id) from contagens")
vid=cur.fetchone()[0]
if vid is None:
    vid=0
vid+=1

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
        #exit();
    if re.search("00000$", str(n)):
        print("\n"+str(n))
    if re.search("000000$", str(n)):
        print("copy table "+str(n))

        file_contagens.close()
        with open("contagens.csv", 'r') as f:
            cur.copy_from(f, 'contagens', sep=',')
        file_contagens=open("contagens.csv", "w+", newline='')
        writer_contagens=csv.writer(file_contagens)
        conn.commit()
    n+=1


file_contagens.close()
with open("contagens.csv", 'r') as f:
    cur.copy_from(f, 'contagens', sep=',')


conn.commit()

cur.execute("CREATE INDEX contagens_localidade\
    ON public.contagens USING btree\
    (localidade ASC NULLS LAST)\
    TABLESPACE pg_default;\
\
CREATE INDEX contagens_data_e_hora\
    ON public.contagens USING btree\
    (data_e_hora ASC NULLS LAST)\
    TABLESPACE pg_default;\
\
CREATE INDEX contagens_data\
    ON public.contagens USING btree\
    ((timezone('GMT-3'::text, data_e_hora)::date) ASC NULLS LAST)\
    TABLESPACE pg_default;\
\
select setval(pg_get_serial_sequence ( 'contagens', 'id' ), (select max(id) from contagens), true);")
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
