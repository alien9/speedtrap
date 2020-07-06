#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys,glob,os,zipfile,re
from subprocess import PIPE, Popen, check_output
from shutil import copyfile


if len(sys.argv)<2:
    print("Usage: uploader.py <data_directory>")
    exit()
path=sys.argv[1]
print("Starting The Trick")

files = [f for f in glob.glob(path+"/*.zip")]
for f in files:
    newname=re.sub('/', '_', f)
    struk=re.split('/', str(f))
    filename=os.path.basename(f)
    print(filename)
    print(struk)
    r = check_output("hdfs dfs -test -d /data; echo $?", shell=True)
    if r == b'1\n':
        os.system("hdfs dfs -mkdir /data")

    path = "/data/"
    for d in struk:
        path += (d+"/")
        print(path)
        r = check_output("hdfs dfs -test -d "+path+ "; echo $?", shell=True)
        if r==b'1\n':
            os.system("hdfs dfs -mkdir " + path)
    copyfile(f, "temp/"+newname)
    print( "temp/"+newname)
    z=zipfile.ZipFile("temp/"+newname)
    contente = z.namelist()
    for c in contente:
        # extract a specific file from zip
        r = check_output("hdfs dfs -test -e " + path + c + "; echo $?", shell=True)
        if r == b'1\n':
            f = z.open(c)
            content = f.read()
            f = open("temp/" + c, 'wb')
            f.write(content)
            f.close()
            print(path + c)
            put = Popen(["hdfs", "dfs", "-put", "temp/"+c, path+c], stdin=PIPE, bufsize=-1)
            put.communicate()
            os.unlink("temp/" + c)
        else:
            print("ja existe "+c+ " em "+path)
    os.unlink("temp/" + filename)
