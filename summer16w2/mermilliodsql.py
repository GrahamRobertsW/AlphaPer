import pandas as pd
from astropy.io import fits
import psycopg2 as p2
infile=fits.open('mermilliod.fit')
names=infile[1].data.names
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("drop table mermilliod;")
con.commit()
cur.execute("create table mermilliod (No integer, m_No character varying, HJD double precision, RV double precision, e_RV double precision, SimbadName varchar, _RA double precision, _DE double precision)")
con.commit()
for i in range(len(infile[1].data)):
   val=0;
   vals=[]
   for val in infile[1].data[i]:
      if val!='':
         vals=vals+[str(val)]
      else:
         vals=vals+['NULL']
   insertion="{0}, ('{1}'::varchar), {2}, {3}, {4}, ('{5}'::varchar), {6}, {7}".format(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],vals[7])
   cur.execute("insert into mermilliod ({0}) values ({1});".format(', '.join(infile[1].data.names),insertion))
con.commit()
