#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spark_functions import *

df=sc.textFile("L2/*.txt").filter(lambda x: len(x)>1).map(countmap_total).filter(lambda x: x is not None).toDF().groupBy("key").sum()
