import pandas as pd
import psycopg2 as p2
from  rpy2.robjects import r
from rpy2.robjects import pandas2ri
from rpy2.robjects import FloatVector as c  
import numpy as np
r.library('ggplot2')
pandas2ri.activate()
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select jmag, kmag, e_jmag, e_kmag from alphaperprevmembers")
pm=pd.DataFrame(cur.fetchall(), columns=['j','k','e_j','e_k'])
cur.execute("select jmag, ksmag, e_j, e_ks from sheikhi where pm=0;")
sh=pd.DataFrame(cur.fetchall(), columns=['j','ks','e_j','e_ks'])
pm['col']=pm['j']-pm['k']
pm['e_col']=np.sqrt(pm['e_j']**2+pm['e_k']**2)
sh['col']=sh['j']-sh['ks']
sh['e_col']=np.sqrt(sh['e_j']**2+sh['e_ks']**2)
import matplotlib.pyplot as plt
plt.errorbar(pm['col'],pm['j'], xerr=pm['e_col'], yerr=pm['e_j'], alpha=.5,  linestyle='')
plt.ylim(max(max(pm['j']),max(sh['j'])),min(min(pm['j']),min(sh['j'])))
plt.errorbar(sh['col'],sh['j'], xerr=sh['e_col'], yerr=sh['e_j'], alpha=.5,  linestyle='')
plt.show()
