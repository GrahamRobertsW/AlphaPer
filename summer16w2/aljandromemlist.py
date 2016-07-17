import pandas as pd
import psycopg2 as p2
#df=pd.read_table('memlist.txt',skiprows=1,names=['ra','dec','radius','SpT','DM','PMra','PMde','SPM','mem','mem+','mem-'])
#print df
infile=open('memlist.txt','r')
names=infile.readline().split()
dict={}
for i in names:
   dict[i]=[]
line=infile.readline()
while line!='':
   j=line.split()
   for k in range(len(j)):
      dict[names[k]]=dict[names[k]]+[str(j[k])]
   line=infile.readline()
df=pd.DataFrame(dict)
headers=', '.join(df.columns.values)
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("drop table alejandroslist")
con.commit()
cur.execute("create table alejandroslist (ra double precision, dec double precision, radius double precision, SpT double precision, DM double precision, PMra double precision, PMdec double precision, SPM double precision, mem double precision, memp double precision, mem1 double precision);")
con.commit()
for i in range(len(df)):
   st=', '.join([str(j) for j in df.values[i]])
   print st
   cur.execute("insert into alejandroslist ({1}) values ({0})".format(st, headers))
con.commit()
