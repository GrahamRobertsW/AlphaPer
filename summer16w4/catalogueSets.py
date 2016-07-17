import pandas as pd
import psycopg2 as p2
from matchCatalog import matchCatalog as mc
from astropy.coordinates import SkyCoord as sc
import fitsql as fs
df=pd.DataFrame
fmts={'INT64':'bigint','INT32':'integer','float64':'double precision','float32':'real','O':'varchar'}
def sql2pddf(tbname):
   con=p2.connect("dbname='{0}' user='postgres' host='localhost'".format(dbname))
   cur=con.cursor()
   cur.execute("select * from {0};".format(tbname))
   ucoldefs=[desc[0] for desc in cur.description]
   dframe=df(cur.fetchall(),columns=ucoldefs)
   cur.close()
   con.close()   
   return dframe

def resolve(arr):
   return[fmts[i] for i in arr]
   
def matchdf(df1, df2, ra1, de1, ra2, de2):
   if len(df1)<len(df2):
      prim=df1
      primname=[ra1,de1]
      sec=df2
      secname=[ra2,de2]
   else:
      prim=df2
      primname=[ra2,de2]
      sec=df1
      secname=[ra1,de1]
   colnames=prim.columns.values.tolist()+sec.columns.values.tolist()
   new_df=df(columns=colnames)
   coord=sc(prim[primname[0]], prim[primname[1]], unit='deg')
   for i in sec.index.values:
      t=sc(sec[secname[0]].values[i],sec[secname[1]].values[i], unit='deg')
      matches, dist = mc(t,coord,3.0,0)
      print matches
      if matches and len(matches)>0:
         tempdf=df([prim.values[int(matches[0])].tolist()+sec.values[i].tolist()],columns=colnames)
         #print tempdf[[ra1,de1,ra2,de2]]
         matches=None
         new_df=new_df.append(tempdf,ignore_index=True)
   return new_df

def pddf2sql(df, name, dbname):
   formats=pddf
   
def 7_19_16_alpha_per_inner_join():
prossT4=sql2pddf('Prosser1992_Table4')
prossT6=sql2pddf('Prosser1992_Table6')
prossT10=sq;pddf('Prosser1992_Table10')
sheikhi=sql2pddf('sheikhi')
mak=sql2pddf('makarov2')
mer=sql2pddf('mermilliod')
dhpm=sql2pddf('deaconhambly2004_PrevMemb')
dhhp=sql2pddf('deaconhambly2004_highprob')
urat=sql2pddf('urat')
aljl=sql2pddf('alejandroslist')
mdf=matchdf(sheikhi, prossT4, 'ra', 'de', '_raj2000', '_dej2000')
#print mdf

