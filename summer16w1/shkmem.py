#This program matched stars that I had in my working catalog to stars in the sheikhi survey 
#It updated the sql database
#Hopefully I never run it again



import psycopg2
from matchCatalog import matchCatalog
from astropy.coordinates import SkyCoord
import pandas as pd
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select ra, de from sheikhi")
sheikhi=pd.DataFrame(cur.fetchall(), columns=['ra','de'])
cur.execute("select raj2000, dej2000, _2mkey from workingcatalog")
wc=pd.DataFrame(cur.fetchall(),columns=['ra','de','key'])
shc= SkyCoord(sheikhi['ra'],sheikhi['de'],unit='deg')
wcoord=SkyCoord(wc['ra'],wc['de'],unit='deg')
matches, dist = matchCatalog(shc,wcoord,3.0,0)
print max(matches)
mm=[i for i in matches]
try:
	cur.execute("drop table temp")
except:
	cur.close()
	con.close()
	con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
	cur=con.cursor()
cur.execute("create table temp (key character varying)")
con.commit()
keys=wc['key'].values[mm]
for k in keys:
	cur.execute("insert into temp (key) values (('{0}'::character varying))".format(k))
con.commit()
cur.execute("insert into alphaperprevmembers select * from workingcatalog where _2mkey in (select key from temp);")
cur.execute("delete from workingcatalog where _2mkey in (select key from temp)")
con.commit()
cur.execute("drop table temp;")
con.commit()
