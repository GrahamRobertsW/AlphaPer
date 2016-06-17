import numpy as np
from radecdist import radecdist
import psycopg2
import matplotlib.pyplot as plt

con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select pmra, pmde, properdist from plotdata where knownmember=1")
data=cur.fetchall()
ra=np.array([datum[0] for datum in data])
de=np.array([datum[1] for datum in data])
dist=np.array([datum[2] for datum in data])
newdist=radecdist(ra,de,np.mean(ra),np.mean(de))
plt.plot(newdist,dist,'k.')
plt.show()
