import pandas as pd
import psycopg2 as p2
import re
from matchCatalog import matchCatalog
from astropy.coordinates import SkyCoord
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
imp={'deaconhambly2004_highprob':['raj2000','dej2000'], 'makarov2':['raj2000','dej2000'],'mermilliod':['_ra','_de'],'prosser1992_table4':['_raj2000','_dej2000'],'prosser1992_table6':['_ra_icrs','_de_icrs'],'prosser1992_table10':['_ra_icrs','_de_icrs'],'sheikhi':['ra','de']}
sk=[]
count=0
for name in imp.keys():
   cs=imp[name]
   cur.execute("select {0} from {1}".format(', '.join(cs), str(name)))
   imp[name]=pd.DataFrame(cur.fetchall(), columns=['ra', 'de'])
   count=count+len(imp[name]['ra'])
cur.execute("select ra, dec from alejandroslist where mem > 50;")
imp['alejandros']=pd.DataFrame(cur.fetchall(),columns=['ra','de'])
count=count+len(imp['alejandros']['ra'])
print 'count={0}'.format(count)
masterra=imp['sheikhi']['ra'].tolist()
masterde=imp['sheikhi']['de'].tolist()
for name in imp.keys():
   if name!='sheikhi':
      master=SkyCoord(masterra,masterde,unit='deg')
      print 'ehllo wolrd!'
      temp=SkyCoord(imp[name]['ra'],imp[name]['de'],unit='deg')
      matches, dist = matchCatalog(master,temp,30.0,0)
      print "For catalog {0} there were {1} matches out of {2} members".format(name,len(matches),len(temp))
      vals=[]
      for i in range(len(temp)):
         if i not in matches:
            vals=vals+[i]
      masterra=masterra+((imp[name]['ra'].values[vals]).tolist())
      masterde=masterde+((imp[name]['de'].values[vals]).tolist())
      
print len(masterra)
import matplotlib.pyplot as plt
plt.plot(masterra,masterde,'k.')
plt.show()
