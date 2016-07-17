import pandas as pd
import psycopg2 as p2
import re
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select icrs_j2000 from makarov")
data=pd.DataFrame(cur.fetchall(),columns=['icrs'])
icrs=re.compile(r'(\d{2}).*(\d{2}).*(\d{2}.\d{4}).*(.)(\d{2}).*(\d{2}).*(\d{2}.\d{4})')
#icrs=re.compile(r'\d{2}')
g=icrs.search(data['icrs'][0]).groups()
ra=((1./3600.)*float(g[2])+(1./60.)*int(g[1])+int(g[0]))*360./24.
de=((1./3600.)*float(g[6])+(1./60.)*int(g[5])+int(g[4]))*(1-2*int(g[3]=='-'))
print ra
print de
