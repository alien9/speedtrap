#!/usr/bin/env python
# -*- coding: utf-8 -*-

q="select distinct id, codigo from (\
select gid as id, substring(___prodam,'[0-9]{4}')::integer as codigo \
from equipamentos union select \
 gid as id, substring(___prodam,'[0-9]{4}\s?\W\s?([0-9]{4})')::integer as codigo \
from equipamentos union select \
gid as id, substring(___prodam,'[0-9]{4}\s?\W\s?[0-9]{4}\s?\W\s?([0-9]{4})')::integer as codigo \
from equipamentos union select \
 gid as id, substring(___prodam,'[0-9]{4}\s?\W\s?[0-9]{4}\s?\W\s?[0-9]{4}\s?\W\s?([0-9]{4})') ::integer as codigo \
from equipamentos ) c \
where codigo is not null"


q="select gid, ___c__digos from equipamentos"# where ___c__digos ~ '4227'"

q="select gid, ___prodam from equipamentos"

import sys, re, psycopg2

cstring="dbname='bigrs' user='tiago' host='localhost' port='5432'"# password='bigrs'"
conn = psycopg2.connect(cstring)
cur = conn.cursor()

cur.execute(q)
r=cur.fetchall()
for l in r:
    print l
    if l[1] is not None:
        m=re.findall('[0-9]{4}', l[1])
        for codigo in m:
            print codigo
            try:
                conn = psycopg2.connect(cstring)
                cur = conn.cursor()
                cur.execute("insert into sensor(equipamento_id, codigo) values (%s,%s)",  (l[0], codigo))
                conn.commit()
            except:
                print "repetido?"