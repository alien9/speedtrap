#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, psycopg2,datetime,csv
from config import cstring

next_viagem=1
next_trajeto=1


conn = psycopg2.connect(cstring)
cur = conn.cursor()

cur.execute("DROP INDEX if exists public.trajetos_data_final_idx;\
    DROP INDEX if exists public.trajetos_data_inicio_idx;\
    DROP INDEX if exists public.trajetos_destino_idx;\
    DROP INDEX if exists public.trajetos_origem_idx;\
    DROP INDEX if exists public.trajetos_viagens_idx;\
")
conn.commit()
cur.execute("select max(id) from trajetos")
next_trajeto=cur.fetchone()[0]
if next_trajeto is None:
    next_trajeto=0
cur.execute("select max(id) from viagens")
next_viagem=cur.fetchone()[0]
if next_viagem is None:
    next_viagem=0
next_trajeto+=1
next_viagem+=1
file_viagens=open("viagens.csv", "w+", newline='')
file_trajetos=open("trajetos.csv", "w+", newline='')
writer_trajetos=csv.writer(file_trajetos)
writer_viagens=csv.writer(file_viagens)

def ponto(t):
    m = re.search('(?P<local>\d{4})(?P<ano>\d{4})(?P<mes>\d{2})(?P<dia>\d{2})(?P<hora>\d{2})(?P<minuto>\d{2})(?P<segundo>\d{2})(?P<tipo>\d{1})(?P<velocidade>\d{3})', t)
    try:
        return {
            'local': m.group('local'),
            'data_e_hora': datetime.datetime.strptime('%s-%s-%s %s:%s:%s' % (m.group('ano'), m.group('mes'), m.group('dia'), m.group('hora'), m.group('minuto'), m.group('segundo'),),'%Y-%m-%d %H:%M:%S'),
            'tipo': m.group('tipo'),
            'velocidade': m.group('velocidade'),
        }
    except:
        return None

def data_e_hora(t):
    return t['data_e_hora']

p=0
trs=0
def viaja(pts):
    global trs
    global p
    trs+=1
    p+=len(pts)
    trips=[[pts[0]]]
    local=pts[0]['local']
    tipo=pts[0]['tipo']
    data_e_hora=pts[0]['data_e_hora']
    i=1;
    while i<len(pts):
        delta = pts[i]['data_e_hora'] - pts[i - 1]['data_e_hora']
        data_e_hora=pts[i]['data_e_hora']
        local=pts[i]['local']
        # vamos considerar apenas os trajetos de menos de 30 minutos:
        if delta.total_seconds() < 1800 and pts[i - 1]['local'] != pts[i]['local']:
            trips[len(trips)-1].append(pts[i])
        else:
            trips.append([pts[i]])
            trs+=1
        i+=1
    return list(filter(lambda x: len(x) > 1, trips))

def filtro(p):
    return p!=None
n=0
nv=0
total=0
for line in sys.stdin:
    total+=1
    line = line.strip()
    if re.match('\w+\t\w+', line):
        nv+=1
        placa, trip = re.split('\t', line)
        #print(placa, end="\r")
        pontos = list(filter(filtro, re.split('\|', trip)))
        pts=list(filter(filtro, map(ponto, pontos)))
        pts.sort(key=data_e_hora)
        if len(pts)>1:
            trips=viaja(pts)
            if len(trips)>0:
                #print(trips)
                n+=len(trips)
                for trip in trips:
                    writer_viagens.writerow([
                        next_viagem,
                        trip[0]['local'],
                        trip[0]['data_e_hora'].isoformat(),
                        trip[len(trip)-1]['local'],
                        trip[len(trip)-1]['data_e_hora'].isoformat(),
                        trip[0]['tipo']
                    ])
                    i=1
                    while i<len(trip):
                        writer_trajetos.writerow([
                            next_trajeto,
                            trip[i - 1]['tipo'],
                            trip[i - 1]['data_e_hora'].isoformat(),
                            trip[i]['data_e_hora'].isoformat(),
                            trip[i - 1]['local'],
                            trip[i]['local'],
                            trip[i - 1]['velocidade'],
                            trip[i]['velocidade'],
                            next_viagem,
                            
                        ])
                        next_trajeto+=1
                        #print(trip[i])
                        i+=1
                    next_viagem+=1
    if re.search("00000$", str(total)):
        print("linhas %s, viagens %s, trajetos %s " % (str(total), n, i)
    if re.search("000000$", str(total)):
        print("copy table "+str(total))
        file_trajetos.close()
        file_viagens.close()
        with open("trajetos.csv", 'r') as f:
            cur.copy_from(f, 'trajetos', sep=',')
        with open("viagens.csv", 'r') as f:
            cur.copy_from(f, 'viagens', sep=',')
        conn.commit()
        file_viagens=open("viagens.csv", "w+", newline='')
        file_trajetos=open("trajetos.csv", "w+", newline='')
        writer_trajetos=csv.writer(file_trajetos)
        writer_viagens=csv.writer(file_viagens)
        

#conn.commit()
print("%s veículos encontrados." % (nv,))
print("%s pontos detectados em %s viagens." % (p,trs))
print("%s viagens válidas encontradas." % (n,))
file_trajetos.close()
file_viagens.close()

with open("trajetos.csv", 'r') as f:
    cur.copy_from(f, 'trajetos', sep=',')
with open("viagens.csv", 'r') as f:
    cur.copy_from(f, 'viagens', sep=',')

cur.execute("CREATE INDEX trajetos_data_final_idx\
    ON public.trajetos USING btree\
    (data_final ASC NULLS LAST)\
    TABLESPACE pg_default;\
CREATE INDEX trajetos_data_inicio_idx\
    ON public.trajetos USING btree\
    (data_inicio ASC NULLS LAST)\
    TABLESPACE pg_default;\
CREATE INDEX trajetos_destino_idx\
    ON public.trajetos USING btree\
    (destino ASC NULLS LAST)\
    TABLESPACE pg_default;\
CREATE INDEX trajetos_origem_idx\
    ON public.trajetos USING btree\
    (origem ASC NULLS LAST)\
    TABLESPACE pg_default;\
CREATE INDEX trajetos_viagens_idx\
    ON public.trajetos USING btree\
    (viagem_id ASC NULLS LAST)\
    TABLESPACE pg_default;\
        select setval(pg_get_serial_sequence ( 'trajetos', 'id' ), (select max(id) from trajetos), true);\
            select setval(pg_get_serial_sequence ( 'viagens', 'id' ), (select max(id) from viagens), true);")
conn.commit()

""" viagens 
 id          | integer                  |           | not null | nextval('radar.viagens_id_seq'::regclass)
 inicio      | integer                  |           |          | 
 data_inicio | timestamp with time zone |           |          | 
 final       | integer                  |           |          | 
 data_final  | timestamp with time zone |           |          | 
 tipo  


trajetos
 id          | integer                     |           | not null | nextval('radar.trajetos_id_seq'::regclass)
 tipo        | integer                     |           |          | 
 data_inicio | timestamp without time zone |           |          | 
 data_final  | timestamp without time zone |           |          | 
 origem      | integer                     |           |          | 
 destino     | integer                     |           |          | 
 viagem      | integer                     |           |          | 
 v0          | integer                     |           |          | 
 v1          | integer   
"""
