import pandas as pd
import psycopg2 as p2
import matplotlib.pyplot as plt
import isotools as iso
df=pd.DataFrame
con=p2.connect("dbname='stars'  host='localhost' user='postgres'")
cur=con.cursor()
cur.execute("select jmag, e_jmag, hmag, e_hmag, kmag, e_kmag from alphaperprevmembers where jmag-kmag<0.6")
ap=df(cur.fetchall(), columns=['J', 'e_J', 'H', 'e_H', 'K', 'e_K'])
cur.close()
con.close()
con=p2.connect("dbname='parsec' host='localhost' user='postgres'")
cur=con.cursor()
cur.execute("select names from years_z021")
N=cur.fetchall()
d={}
for n in N:
   cur.execute("select j, h, k from {0}_z021;".format(n[0]))
   d[n]=df(cur.fetchall(),columns=['J','H','K'])
   d[n]['fit']=iso.testfitiso(ap,d[n],6.2)
outfile=open('bestiso.txt', 'w')
for k in d.keys():
   outfile.write("{0}\t{1}\n".format(k,d[k]['fit'][0]))
cur.close()
con.close()
outfile.close()
