import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import r 
from rpy2.robjects import pandas2ri
pandas2ri.activate()
import psycopg2
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select jmag, ksmag from sheikhi")
df=pd.DataFrame(cur.fetchall(),columns=['j','ks'])
r.png("isochroneofsheikhidata.png")
r.plot(df['j']-df['ks'],df['j'],xlim=ro.FloatVector([min(df['j']-df['ks']),max(df['j']-df['ks'])]),ylim=ro.FloatVector([max(df['j']),min(df['j'])]),xlab='color [J-Ks]', ylab='Jmag', main='cmd from Sheikhi data')
v=raw_input()
