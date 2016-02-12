import numpy as np
import psycopg2
from rpy2 import robjects as ro
from rpy2.robjects import numpy2ri
from matplotlib import pyplot as plt
import math
numpy2ri.activate()
r=ro.r
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()

#now to calculate the densities
def plotdistance(distance, max, bin, title):
   R=[]
   P=[]
   r=0
   while r<=(max+bin):
      R.append(r)
      count=len(np.where(np.logical_and(distance>=r, distance<(r+bin)))[0])
      print count
      area=np.pi*((r+bin)**2-r**2)
      P.append(float(count/area))
      r+=(bin)
   plt.plot(R,P,'m')
   plt.title(title)
   plt.show()

def areaDensity(counts,breaks):
   return np.array([(counts[i]/(math.pi*(breaks[i+1]**2-breaks[i]**2))) for i in range(0,len(counts))])

#ection import relevant data on the known members
cur.execute("select raj2000, dej2000, pmra, pmde ,_2mkey from alphaperprevmembers")
data=cur.fetchall()
knownra=np.array([datum[0] for datum in data])
knownde=np.array([datum[1] for datum in data])
knownpmra=np.array([datum[2] for datum in data])
knownpmde=np.array([datum[3] for datum in data])
known2masskeys=np.array([datum[4] for datum in data])

#This section import relevant data on the candidate members
cur.execute("select raj2000, dej2000, pmra, pmde ,_2mkey  from workingcatalog")
data=cur.fetchall()
catra=np.array([datum[0] for datum in data])
catde=np.array([datum[1] for datum in data])
catpmra=np.array([datum[2] for datum in data])
catpmde=np.array([datum[3] for datum in data])
cat2masskeys=np.array([datum[4] for datum in data])

demedian=r.median(knownde)[0]
print demedian
ramedian=r.median(knownra)[0]
print ramedian
knowndistance=np.sqrt(((knownra-ramedian)*np.cos(knownde))**2+(knownde-demedian)**2)
catdistance=np.sqrt(((catra-ramedian)*np.cos(catde))**2+(catde-demedian)**2)

pmramedian=r.median(knownpmra)[0]
pmdemedian=r.median(knownpmde)[0]
knownpmdistance=np.sqrt((knownpmra-pmramedian)**2+(knownpmde-pmdemedian)**2)
catpmdistance=np.sqrt((catpmra-pmramedian)**2+(catpmde-pmdemedian)**2)
print max(knowndistance)

plotdistance(knowndistance,max(knowndistance),5./60.,'Knowndistance')
plotdistance(catdistance,max(knowndistance),5./60.,'catalogdistance')
plotdistance(knownpmdistance,max(knownpmdistance),np.std(knownpmdistance),'known')
plotdistance(catpmdistance,max(knownpmdistance),np.std(knownpmdistance),'catalog')
