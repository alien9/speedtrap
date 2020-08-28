#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, psycopg2, datetime, csv
from config import cstring

conn = psycopg2.connect(cstring)
cur = conn.cursor()

with open("trajetos.csv", 'r') as f:
    cur.copy_from(f, 'trajetos', sep=',')
with open("viagens.csv", 'r') as f:
    cur.copy_from(f, 'viagens', sep=',')


conn.commit()