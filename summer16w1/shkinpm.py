#This program looks through my catalog of known members, as well as the sheikhi catalog.  It flags the data in the sheikhi catalog that is shared so that I can avoid using it. if need be.
import psycopg2
import pandas as pd
from matchCatalog import matchCatalog
from astropy.coordinates import SkyCoord
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select ra, de from sheikhi;")
sdf=pd.DataFrame(cur.fetchall(), columns=['ra','de'])
cur.execute("select raj2000, dej2000 from alphaperprevmembers")
pmdf=pd.DataFrame(cur.fetchall(),columns=['ra','de'])
ssk=SkyCoord(sdf['ra'],sdf['de'],unit='deg')
ask=SkyCoord(pmdf['ra'],pmdf['de'],unit='deg')
matches, dist= matchCatalog(ask, ssk, 3.0, 0)
om, od = matchCatalog(ssk, ask, 3.0, 0)
print max(matches)
print max(om)
try:
	cur.execute("drop table temp")
	con.commit()
except:
	cur.close()
	con.close()
	con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
	cur=con.cursor()
cur.execute("create table temp (ra double precision, de double precision);")
con.commit()
for m in matches:
	cur.execute("insert into temp (ra, de) values ({0},{1})".format(sdf['ra'][m],sdf['de'][m]))
con.commit()
cur.execute("update sheikhi set pm = 1 where (ra, de) in (select ra, de from temp);")
con.commit()
