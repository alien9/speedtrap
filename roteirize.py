#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,psycopg2



def reverse_geocode(x,y,cursor):
    cursor.execute(
        "select a.gid, a.source, a.target, a.linha from (select gid,source,target,st_linemerge(geom) as linha from segmento_viario order by geom <-> st_transform(ST_GeomFromEWKt(%s),31983) limit 1) as a",
        ("SRID=4326;POINT(%s %s)"%(x,y),))
    #print(cursor.mogrify(
    #    "select a.gid, a.source, a.target, a.linha from (select gid,source,target,st_linemerge(geom) as linha from segmento_viario order by geom <-> st_transform(ST_GeomFromEWKt(%s),31983) limit 1) as a",
    #    ("SRID=4326;POINT(%s %s)"%(x,y),))
    #)

    return cursor.fetchone()

def roteirize(p,q, cursor):
    origem = reverse_geocode(p[0],p[1],cursor)
    #print(origem)
    destino=reverse_geocode(q[0],q[1],cursor)
    #print(destino)
    cursor.execute(
        "select case when st_geometrytype(g)='ST_MultiLineString' then st_geometryn(g, 1) else g end from (select st_linemerge(st_union(s.geom)) as g from "
        "(select seq,path_seq,node,edge,cost,agg_cost from pgr_dijkstra('SELECT gid as id,source, target, st_length(geom) as cost, st_length(geom) as reverse_cost FROM segmento_viario', %s,%s))"
        " a left join segmento_viario s on s.id=a.edge) e",
        (origem[1], destino[2],)
    )
    #print(cursor.mogrify("select * from pgr_dijkstra('SELECT gid as id,source, target, st_length(geom) as cost, st_length(geom) as reverse_cost FROM segmento_viario', %s,%s)",
    #    (origem[1], destino[2],)
    #))
    res = cursor.fetchone();
    g=res[0]
    #print((res[0], "SRID=4326;POINT(%s %s)" % (p[0], p[1],),res[0],"SRID=4326;POINT(%s %s)" % (q[0],q[1],)))
    cursor.execute("select st_linelocatepoint(st_geomfromwkb(%s::geometry),st_transform(st_geomfromewkt(%s), 31983)) as ini, st_linelocatepoint(st_geomfromwkb(%s::geometry),st_transform(st_geomfromewkt(%s), 31983)) as fim",
                   (res[0], "SRID=4326;POINT(%s %s)" % (p[0], p[1],),res[0],"SRID=4326;POINT(%s %s)" % (q[0],q[1],)),
                   )
    ps=list(cursor.fetchone())
    ps.sort()
    cursor.execute("select g, st_geometrytype(g) from (select g from (select st_linesubstring(st_geomfromwkb(%s::geometry), %s, %s) as g) h)o", (res[0], ps[0], ps[1]))

    #for r in res:
    #    cursor.execute("select geom from segmento_viario where gid=%s", r[3])
    res=cursor.fetchone()
    print res
    if not res[1]=='ST_LineString':
        return None
    return res[0]

if __name__ == "__main__":
    if len(sys.argv)==5:
        cstring = "dbname='bigrs' user='tiago' host='localhost' port='5432'"  # password='bigrs'"
        conn = psycopg2.connect(cstring)
        cursor = conn.cursor()
        print roteirize(
            [sys.argv[1],sys.argv[2]],[sys.argv[3],sys.argv[4]],cursor
        )
    else:
        print "Faltam parâmetos"