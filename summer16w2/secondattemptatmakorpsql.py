import pandas as pd
import psycopg2 as p2
from astropy.io import fits
import re
from fitsformatdict import resolve as rs
def charcast(s,dt):
   if s!='' and s !='nan':
      return "('{0}'::{1})".format(s,rs(dt))
   else:
      return 'NULL'
n=fits.open('makarov2.fit')
repo=re.compile(r'B-V')
mportString=repo.sub('B_V',', '.join(['{0} {1}'.format(n[1].data.names[i],rs(n[1].data.formats[i])) for i in range(len(n[1].data.columns))]))
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
#cur.execute("drop table makarov2")
#con.commit()
cur.execute("create table makarov2 ({0});".format(mportString))
con.commit()
for d in n[1].data:
   imp=[]
   s=[str(i) for i in d]
   names=repo.sub('B_V',', '.join(n[1].data.names))
   for i in range(len(s)):
      if s[i]!='' and s[i]!='nan':
         imp=imp+[s[i]]
      else:
         dt=rs(n[1].data.formats[i])
         if 'varchar' in dt:
            imp=imp+['']
         else:
            imp=imp+['NULL']
   print imp
   valueString="{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(imp[0],charcast(imp[1],n[1].data.formats[1]),imp[2],charcast(imp[3], n[1].data.formats[3]),', '.join(imp[4:15]), charcast(imp[15], n[1].data.formats[15]),', '.join(imp[16:18]), charcast(imp[18], n[1].data.formats[18]))
   cur.execute("insert into makarov2 ({0}) values ({1})".format(names, valueString))
con.commit()
