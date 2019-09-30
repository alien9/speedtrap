#!/usr/bin/env python

from roteirize import *
import sys,re,datetime,psycopg2

cstring="dbname='bigrs' user='tiago' host='localhost' port='5432'"# password='bigrs'"
conn = psycopg2.connect(cstring)
cursor = conn.cursor()

def set_point(p):
    s=p.split('_')
    return {'eq':s[0],'ts':datetime.datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S')}

def get_local(codigo):
    cursor.execute("select st_x(e.geom), st_y(e.geom),s.codigo from equipamentos e join sensor s on s.equipamento_id=e.gid where s.codigo=%s",
               (codigo,))
    return cursor.fetchone()

for line in sys.stdin:
    placa_trip = line.strip().split('\t')
    if len(placa_trip)>1:
        pontos = map(set_point, placa_trip[1][:-1].split('|'))
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
