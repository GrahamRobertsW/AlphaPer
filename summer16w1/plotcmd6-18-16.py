import pandas as pd
from rpy2 import robjects as ro
from rpy2.robjects import r
from rpy2.robjects import pandas2ri
from rpy2.robjects import FloatVector as c
import psycopg2
pandas2ri.activate()
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select Jmag, kmag from alphaperprevmembers")
cur.execute("select jmag, ksmag from sheikhi where pm=0")
df=pd.DataFrame(cur.fetchall(),columns=['j','k'])
r.plot(df['j']-df['k'],df['j'],xlim=c([min(df['j']-df['k']),max(df['j']-df['k'])]), ylim=c([max(df['j']), min(df['j'])]), xlab='color J-K', ylab='J_mag', main='')
rW=raw_input()
