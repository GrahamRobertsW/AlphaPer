import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
from matchCatalog import matchCatalog
import rpy2.robjects as ro
from rpy2.robjects import r
from rpy2.robjects import pandas2ri
from rpy2.robjects import numpy2ri
pandas2ri.activate()
numpy2ri.activate
import psycopg2
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select ra, de from sheikhi")
sdf=pd.DataFrame(cur.fetchall(),columns=['ra','de'])
cur.execute("Select raj2000, dej2000 , knownmember from plotdata")
cdf=pd.DataFrame(cur.fetchall(),columns=['ra','de','km'])
ssk=SkyCoord(sdf['ra'],sdf['de'],unit='deg')
csk=SkyCoord(cdf['ra'],cdf['de'],unit='deg')
matches, dist = matchCatalog(csk,ssk,3.0,0)
print sum(cdf['km'].values[matches])
print len(matches)
