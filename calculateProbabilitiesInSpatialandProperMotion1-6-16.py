import psycopg2
from rpy2 import robjects as ro
from rpy2.robjects import numpy2ri
import numpy as np
import math
import matplotlib.pyplot as plt
#%matplotlib inline
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
r=ro.r
numpy2ri.activate()
def countsIncrimentor(arrayLike, breaks):
   steps=np.array([breaks[i]-breaks[i-1] for i in range(1,len(breaks))])
   breakPoint=np.mean(steps)
   counts=np.zeros(len(steps))
   index=None
   for i in arrayLike:
      index=i//breakPoint
      if index < len(counts):
         counts[index]+=1
   return counts
def areaDensity(counts,breaks):
   return np.array([(counts[i]/(math.pi*(breaks[i+1]**2-breaks[i]**2))) for i in range(0,len(counts))])
cur.execute("select raj2000, dej2000, pmra, pmde from alphaperprevmembers")
data=cur.fetchall()
ra=np.array([float(datum[0]) for datum in data])
de=np.array([float(datum[1]) for datum in data])
pmra=np.array([float(datum[2]) for datum in data])
pmde=np.array([float(datum[3]) for datum in data])
ramid=r.median(ra)[0]
demid=r.median(de)[0]
pmramid=r.median(pmra)[0]
pmdemid=r.median(pmde)[0]
distance=np.sqrt((ra-ramid)**2+(de-demid)**2)
pmdistance=np.sqrt((pmra-pmramid)**2+(de-demid)**2)
spacialhist=r.hist(distance,32,plot=False)
pmhist=r.hist(pmdistance,32,plot=False)
f=raw_input()
spacialbreaks=np.array([i for i in spacialhist.rx('breaks')[0]])
spacialcounts=np.array([i for i in spacialhist.rx('counts')[0]])
print len(spacialbreaks)
print len(spacialcounts)
pmbreaks=np.array([i for i in pmhist.rx('breaks')[0]])
pmcounts=np.array([i for i in pmhist.rx('counts')[0]])
spacialdensity=np.array([(spacialcounts[i]/(math.pi*(spacialbreaks[i+1]**2-spacialbreaks[i]**2))) for i in range(0,len(spacialcounts))])
pmdensity=np.array([(pmcounts[i]/(math.pi*(pmbreaks[i+1]**2-pmbreaks[i]**2))) for i in range(0,len(pmcounts))])
#r.par(mfrow=np.array([2,2]))
#print r.par('usr')
#raw_input()
#r.plot(np.array([spacialbreaks[i] for i in range(1,len(spacialbreaks))]),spacialdensity,xlab='distance from median [deg]', ylab='area density of stars', main='spacial density of known mebers')
#r.rect(r.par('usr')[1],r.par('usr')[3],r.par('usr')[2],r.par('usr')[3],col='blue')
#r.par(bg='yellow')
#r.plot(np.array([pmbreaks[i] for i in range(1,len(pmbreaks))]),pmdensity,xlab='differenc in magnitude of proper motion from median value',ylab='frequency of stars',main='relative frequency differences in known members')
#r.plot(ra,de,xlab='rigght ascension [deg]',ylab='declination [deg]',main='spacial plot of star locations')
#r.points(np.array([ramid]),np.array([demid]),col='yellow',add=True)
#r.legend('topright',legend=np.array(['known member','median']),col=np.array(['black','yellow']))
#r.par(bg='yellow')
#r.plot(pmra,pmde, xlab=r'proper motion right ascnsion [mas/yr]',ylab=r'Proper Motion Declination [mas/yr]', main='proper motions of known members')
#r.points(np.array([pmramid]),np.array([pmdemid]),col='yellow',add=True)
#r.legend('topright',legend=np.array(['known member', 'median']),col=np.array(['black','yellow']))
print spacialcounts
print spacialbreaks
print spacialdensity
cur.execute("select raj2000, dej2000, pmra, pmde, _2mkey from workingcatalog")
data=cur.fetchall()
#catalogdistances=np.array([ i for i in r.hist(np.array([math.sqrt((float(datum[0])-ramid)**2+(float(datum[1])-demid)**2) for datum in data]),spacialbreaks,plot=False).rx('counts')])/np.array([math.pi*(spacialbreaks[i+1]-spacialbreaks[i])**2 for i in range(0,len(spacialcounts))])
catalogpmdistances=np.array([math.sqrt((float(datum[2])-pmramid)**2+(float(datum[3])-pmdemid)**2) for datum in data])
catalogDistances=np.array([math.sqrt((float(datum[0])-ramid)**2+(float(datum[1])-demid)**2) for datum in data])
catalogra=np.array([float(datum[0]) for datum in data])
catalogde=np.array([float(datum[1]) for datum in data])
catalogpmra=np.array([float(datum[2]) for datum in data])
catalogpmde=np.array([float(datum[3]) for datum in data])
possibleKeys=[str(datum[4]) for datum in  data]
catalogCounts=countsIncrimentor(catalogDistances,spacialbreaks)
catalogpmcounts=countsIncrimentor(catalogpmdistances,pmbreaks)
catalogSpacialDensity=areaDensity(catalogCounts,spacialbreaks)
catalogPMDensity=areaDensity(catalogpmcounts,pmbreaks)
raw_input()
f, axarr=plt.subplots(2,2)
spacialXaxis=np.array([spacialbreaks[i] for i in range(1,len(spacialbreaks))])
pmXaxis=np.array([pmbreaks[i] for i in range(1,len(pmbreaks))])
axarr[0,0].scatter(spacialXaxis, spacialdensity)
axarr[0,0].scatter(spacialXaxis,catalogSpacialDensity,c='r')
axarr[0,0].set_ylabel('density')
axarr[0,0].set_xlabel('spacial distance from median')
axarr[0,0].set_title(r'spacial area density of $\alpha$ per')
axarr[0,1].scatter(pmXaxis,pmdensity,label='Known Members')
axarr[0,1].scatter(pmXaxis,catalogPMDensity,c='r', label='Catalog Stars')
axarr[0,1].set_ylabel('desity')
axarr[0,1].set_xlabel('distance from median in proper motion space')
axarr[0,1].set_title(r'area density of proper motion of $\alpha$ per')
axarr[0,1].legend('topright')
axarr[0,1].set_axis_bgcolor('grey')
axarr[1,0].scatter(catalogra,catalogde,c='r')
axarr[1,0].scatter(ra,de)
axarr[1,0].set_xlabel('ra')
axarr[1,0].set_ylabel('de')
axarr[1,0].set_title(r'spacial plot of $\alpha$ per')
axarr[1,1].scatter(catalogpmra,catalogpmde,c='r')
axarr[1,1].scatter(pmra,pmde)
axarr[1,1].set_xlabel('pmra')
axarr[1,1].set_ylabel('pmde')
axarr[1,1].set_title(r'proper motion plot of $\alpha$ per')
axarr[1,1].set_axis_bgcolor('grey')
plt.tight_layout()
plt.show()
raw_input()
acceptedKeys=[]
pmmax=np.max(pmdistance)
distmax=np.max(distance)
#cur.execute("create table possibilities (_2mkey character varying);")
#con.commit()
#for i in range(0,len(possibleKeys)):
#   if catalogpmdistances[i]<=pmmax and catalogDistances[i]<=distmax:
#      cur.execute("insert into possibilities (_2mkey) values(cast({0} as character varying));".format(possibleKeys[i]))
#con.commit()
