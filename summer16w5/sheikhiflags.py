import pandas as pd
import psycopg2 as p2
import matplotlib.pyplot as plt
import numpy as np
df=pd.DataFrame
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select jmag-ksmag, jmag from usheikhi;")
sh=df(cur.fetchall(),columns=['col','mag'])
plt.scatter(sh['col'],sh['mag'])
x=np.arange(0,1.2,.01)
y=[5.*i+4 for i in x]
plt.plot(x,y)
cur.execute("select jmag-ksmag, jmag, uurat1 from usheikhi where jmag<(5*(jmag-ksmag)+4);")
shg=df(cur.fetchall(),columns=['col','mag','key'])
plt.scatter(shg['col'],shg['mag'],color='red')
plt.show()
print shg['key']
