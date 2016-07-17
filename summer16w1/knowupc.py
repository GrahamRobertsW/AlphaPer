import psycopg2
import pandas as pd
from matchCatalog import matchCatalog
from astropy.coordinates import SkyCoord
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select raj2000, dej2000 from upc where abspi<6 and abspi>8;")
udf=pd.DataFrame(cur.fetchall(),columns=['ra','de'])
cur.execute("select raj2000, dej2000 from alphaperprevmembers")
pmdf=pd.DataFrame(cur.fetchall(),columns=['ra','de'])
usc=SkyCoord(udf['ra'],udf['de'],unit='deg')
pmsc=SkyCoord(pmdf['ra'],pmdf['de'],unit='deg')
matches, dist, = matchCatalog(pmsc,usc,3.0,0)
print len(matches)
try: 
	cur.execute('drop table temp')
	con.commit()
except:
	cur.close()
	con.close()
	con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
	cur=con.cursor()
cur.execute('create table temp (ra double precision, de double precision)')
cur.execute("update upc set ap=0;")
con.commit()
for i in matches:
	cur.execute("insert into temp (ra, de) values({0},{1})".format(udf['ra'][i],udf['de'][i]))
con.commit()
cur.execute("update upc set ap=1 where (raj2000, dej2000) in (select ra, de from temp)")
con.commit()
cur.execute('drop table temp')
con.commit()
