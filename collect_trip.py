#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, psycopg2,datetime

cstring="dbname='radartona' user='smt_user' host='10.35.200.226' port='5432' password='smt_user'"
conn = psycopg2.connect(cstring)
cur = conn.cursor()

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

def viaja(pts):
    local=pts[0]['local']
    tipo=pts[0]['tipo']
    data_e_hora=pts[0]['data_e_hora']
    cur.execute(
        "INSERT INTO viagens(data_inicio, inicio, tipo) VALUES (%s,%s,%s) returning id",
        (data_e_hora, local, tipo)
    )
    viagem_id = cur.fetchone()[0]
    i=1;
    while i<len(pts):
        delta = pts[i]['data_e_hora'] - pts[i - 1]['data_e_hora']
        data_e_hora=pts[i]['data_e_hora']
        local=pts[i]['local']
        # vamos considerar apenas os trajetos de menos de duas horas:
        if delta.total_seconds() < 7200 and pts[i - 1]['local'] != pts[i]['local']:
            cur.execute(
                "INSERT INTO trajetos(viagem_id,data_inicio, data_final, origem, destino, tipo, v0, v1) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (viagem_id, pts[i - 1]['data_e_hora'], pts[i]['data_e_hora'], pts[i - 1]['local'], pts[i]['local'],
                 pts[i]['tipo'],pts[i-1]['velocidade'],pts[i]['velocidade'])
                )
        else:
            cur.execute(
                "update viagens  set data_final=%s, final=%s where id=%s",
                (pts[i - 1]['data_e_hora'], pts[i - 1]['local'], pts[i - 1]['vigem_id'])
            )
            #viaja(pts[i:len(pts)])
            cur.execute(
                "update viagens set data_final=%s, final=%s where id=%s",
                (pts[i-1]['data_e_hora'], pts[i-1]['local'], viagem_id)
            )
            cur.execute(
                "INSERT INTO viagens(data_inicio, inicio, tipo) VALUES (%s,%s,%s) returning id",
                (pts[i]['data_e_hora'], pts[i]['local'], pts[i]['tipo'])
            )
            viagem_id = cur.fetchone()[0]
        i+=1

    cur.execute(
        "update viagens  set data_final=%s, final=%s where id=%s",
        (data_e_hora, local, viagem_id)
    )
    conn.commit()


def filtro(p):
    return p!=None
n=0
for line in sys.stdin:
    line = line.strip()
    n+=1
    if re.match('\w+\t\w+', line):
        placa, trip = re.split('\t', line)
        print(placa, end="\r")
        pontos = list(filter(filtro, re.split('\|', trip)))
        pts=list(filter(filtro, map(ponto, pontos)))
        pts.sort(key=data_e_hora)
        viaja(pts)
    if re.search("00000$", str(n)):
        print("\n"+str(n))
conn.commit()
