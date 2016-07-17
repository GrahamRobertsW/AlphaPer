import fitsql as fs
import pandas as pd
import psycopg2 as p2
from astropy.io import fits
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
filepath='/home/groberts/astro/uratdata'
fs.uptemp(filepath+'/AlphaPer.urat0.fit','stars')
cur.execute("drop table urat")
con.commit()
cur.execute("create table urat as select * from temp;")
con.commit
cur.execute("drop table temp")
con.commit()
for i in range(1,65):
   if i != 36:
      fs.uptemp('{0}/AlphaPer.urat{1}.fit'.format(filepath,str(i)),'stars')
      cur.execute("insert into urat (select * from temp where urat1 not in (Select urat1 from urat))")
      con.commit()
      cur.execute("drop table temp")
      con.commit()
