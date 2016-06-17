import numpy as np
from radecdist import radecdist
import psycopg2
import matplotlib.pyplot as plt

con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select raj2000, dej2000, pmra, pmde, spacialdist, properdist from plotdata where knownmember=1")
data=cur.fetchall()
ra=np.array([datum[0] for datum in data])
de=np.array([datum[1] for datum in data])
pmra=np.array([datum[2] for datum in data])/(3.6*10**6)
pmde=np.array([datum[3] for datum in data])/(3.6*10**6)
sdist=np.array([datum[4] for datum in data])
pdist=np.array([datum[5] for datum in data])
newsdist=radecdist(ra,de,np.mean(ra),np.mean(de))
newpdist=radecdist(pmra,pmde,np.mean(pmra),np.mean(pmde))*(3.6*10**6)
plt.plot(newsdist,sdist,'k.')
plt.xlabel("angular distance [deg]")
plt.ylabel("angular distance [deg] from poster")
plt.title("spatial distance")
plt.show()
plt.plot(newpdist,pdist,'k.')
plt.xlabel("angular distance proper motion space [mas/yr]")
plt.ylabel("angular distance proper motion space [mas/yr] from poster")
plt.title("proper motion distance")
plt.show()
