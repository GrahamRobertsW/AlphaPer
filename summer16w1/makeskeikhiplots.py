import pandas as pd
from rpy2 import robjects as ro
r=ro.r
from rpy2.robjects import pandas2ri
pandas2ri.activate()
import psycopg2
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select ra, de, pmra, pmde from sheikhi")
sdf=pd.DataFrame(cur.fetchall(),columns=['ra', 'de', 'pmra','pmde'])
print min(sdf['pmra'])
print max(sdf['pmra'])
v=raw_input()
r.png('sheikhiProperMotions.png')
r.plot(sdf['pmra'],sdf['pmde'],data=sdf,xlim=ro.FloatVector([min(sdf['pmra']),max(sdf['pmra'])]),ylim=ro.FloatVector([min(sdf['pmde']),max(sdf['pmde'])]),xlab='pmra',ylab='pmde',main='Sheikhi Proper Motion of alpha persei members')

v=raw_input()
#r.plot(rsdf.pmra,rsdf.pmde,data=rsdf, xlim=ro.FloatVector([min(sdf['pmra']),max(sdf['pmra'])]),ylim=ro.FloatVector([min(sdf['pmde']),max(sdf['pmde'])]))

v=raw_input()
