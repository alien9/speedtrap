#!/usr/bin/env python

from roteirize import *
import sys,re,datetime,psycopg2

from config import cstring
conn = psycopg2.connect(cstring)
cursor = conn.cursor()

def set_point(p):
    s=p.split('_')
    return {'eq':s[0],'ts':datetime.datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S')}

def get_local(codigo):
    #cursor.execute("select st_x(e.geom), st_y(e.geom),s.codigo from equipamentos e join sensor s on s.equipamento_id=e.gid where s.codigo=%s",
    #           (codigo,))
    cursor.execute("select  st_x(geom), st_y(geom),codigo from base_radares where position(%s in codigo) > 0;",
               (str(codigo),))
    return cursor.fetchone()

cursor.execute("select t.origem, t.destino, t.tipo, r.id from trajetos t left join radar_route r on r.origem=t.origem and r.destino=t.destino where r.id is null")
r=cursor.fetchall()
for line in r:
    print(line)
    tipo=line[2]
    o=line[0]
    d=line[1]
    origem = get_local(o)
    destino = get_local(d)
    if origem is not None and destino is not None:
        cursor.execute("select * from radar_route where origem=%s and destino=%s",
                       (o, d,))
        existent = cursor.fetchall()
        if len(existent) == 0:
            rot = roteirize([origem[0], origem[1]], [destino[0], destino[1]], cursor)
            print("roteiro")
            print(rot)
            if rot is not None:
                cu = conn.cursor()
                cu.execute(
                    "insert into radar_route (origem, destino, the_geom) VALUES (%s, %s, st_geomfromwkb(%s::geometry))",
                    (o, d, rot))
                cu.close()
                conn.commit()

    #(9059301, 1, datetime.datetime(2018, 2, 1, 19, 18, 48), datetime.datetime(2018, 2, 1, 19, 24, 52), 5424, 5497)
"""    
    placa_trip = line.strip().split('\t')
    if len(placa_trip)>1:pontos = map(set_point, placa_trip[1][:-1].split('|'))
        print(placa_trip)
        #print(placa_trip[1][:-1])
        pontos = map(set_point, placa_trip[1][:-1].split('|'))
        pontos.sort(key=lambda x: x['ts'])
        if len(pontos)>1:
            print(pontos)
            for i in range(1,len(pontos)):
                print(str(pontos[i-1]['eq'])+" "+str(pontos[i]['eq']))
                if pontos[i-1]['eq'] != pontos[i]['eq']:
                    cursor.execute("select * from radar_route where origem=%s and destino=%s", (pontos[i-1]['eq'], pontos[i]['eq'],))
                    existent = cursor.fetchall()
                    if len(existent) == 0:
                        origem = get_local(pontos[i - 1]['eq'])
                        print("ORIGEM:")
                        print(origem)
                        destino = get_local(pontos[i]['eq'])
                        print("DESTINO:")
                        print(destino)
                        if origem is not None and destino is not None:
                            rot=roteirize([origem[0],origem[1]],[destino[0],destino[1]],cursor)
                            print(rot)
cu = conn.cursor()
cu.execute("insert into radar_route (origem, destino, the_geom) VALUES (%s, %s, st_geomfromwkb(%s::geometry))", (pontos[i-1]['eq'], pontos[i]['eq'], rot))
cu.close()

conn.commit()
"""