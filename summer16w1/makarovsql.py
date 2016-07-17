import pandas as pd
import psycopg2 as p2
def wrapper(l):
   return l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8], l[9], l[10], l[11], l[12]
columns=['n','Identifier','Otype','ICRS_J2000','U','B','V','R','I','Sp_type', 'nref1850_2016', 'nnotes']
df=pd.read_table('~/Downloads/simbad.txt',skiprows=6,sep='|',names= columns, skipinitialspace=True)
for i in df.columns:
   for j in range(len(df)):
      if df[i][j]=='~':
         df[i][j]='NULL'
print len(df)
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
dtypes=['integer', 'character varying', 'character varying', 'character varying', 'double precision', 'double precision', 'double precision', 'double precision', 'double precision', 'character varying', 'integer', 'integer']
print len(df.values[0])

print len([', '.join(columns)]+[str(j) for j in df.values[0]])
try:
   cur.execute("drop table makarov")
   con.commit()
except:
   cur.close()
   con.close()   
   con=p2.connect("dbname='stars' user='postgres' host='localhost'")
   cur=con.cursor()
inserts=[]
for i in range(len(columns)):
   inserts=inserts+["{0} {1}".format(str(columns[i]),str(dtypes[i]))]
createString=', '.join([str(i) for i in inserts])
cur.execute("create table makarov ({0});".format(createString))
con.commit()
counts=0
for i in range(len(df)-1):
   print counts
   counts=counts+1
   l=[', '.join(columns)]+[str(j) for j in df.values[i]]
   cur.execute("insert into makarov ({0}) values ({1}, ('{2}'::varchar), ('{3}'::varchar), ('{4}'::varchar), {5}, {6}, {7}, {8}, {9}, ('{10}'::varchar), {11}, {12})".format(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8], l[9], l[10], l[11], l[12]))

con.commit()
