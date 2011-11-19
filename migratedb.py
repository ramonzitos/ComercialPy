#!/usr/bin/env python
# coding: iso-8859-1
import kinterbasdb
import sys
from pysqlite2 import dbapi2 as sqlite
import os

# Conectando DBs
confb = kinterbasdb.connect(dsn=str(sys.argv[1]), user="SYSDBA", password="sysdba")
consqlite = sqlite.connect(str(sys.argv[2]))

# Cursores
cursorfb = confb.cursor()
cursorsql = consqlite.cursor()

cursorfb.execute("select * from fmaprodutos;")
cursorsql.execute("create table produtos(id integer primary key, nome text, codigo text, quantidade integer, preco real);")
j = 1
for i in cursorfb:
  t = (i[1].rstrip().decode("iso-8859-1"), i[2].rstrip(), i[15], i[11])
  cursorsql.execute("insert into produtos (nome, codigo, quantidade, preco) values (?, ?, ?, ?)", t)
  if j % 100 == 0: print("%i produtos migrados" % j)
  j = j + 1
print("Dando commit...")
consqlite.commit()
print("--- Fim ---")
print("")
print("%i produtos migrados" % j)
raw_input("Pressione ENTER para continuar...")
