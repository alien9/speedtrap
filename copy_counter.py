#!/usr/bin/env python
# -*- coding: utf-8 -*-

#465520180201210	9

import sys, re, psycopg2, csv
from config import cstring
conn = psycopg2.connect(cstring)
cur = conn.cursor()

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
