import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
pandas2ri.activate()
r=ro.r
c=ro.FloatVector
import psycopg2
con=psycopg2.connect("dbname='stars' host='localhost' user='postgres'")
cur=con.cursor()
cur.execute("select raj2000, dej2000, srcpi from upc where ap =1;")
df=pd.DataFrame(cur.fetchall(),columns=['ra','de','pi'])
r.plot(df['ra'],df['de'],xlim=c([min(df['ra']),max(df['ra'])]),ylim=c([min(df['de']),max(df['ra'])]),xlab='ra',ylab='de',main='')
raw=raw_input()
r.hist(1./(df['pi']/1000.),18,xlab='parallax',ylab='count',main='')

raw=raw_input()
