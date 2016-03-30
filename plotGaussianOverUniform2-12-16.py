#PlotGaussianOverUniform
#with regards to the AlphaPersei open cluster
#We'd expect the rea density of the field stars to follow an approximate uniform distriution give or take.
#The one notable exception is where the cluster lays, we expect a small increase in density
# I will begin by approximating the area density of frieldtars,although only the ones within about 5 degrees of the median of the cluster to avoid edge effects
import numpy as np
import psycopg2
#import analyze_spacial_distribution.py
from matplotlib import pyplot as plt
def calculateAreaRadialDensity(distances,step,maximum):
   r=0
   counts=[]
   radii=[]
   while(r<maximum):
     count=len(np.where(np.logical_and(distances<r+step, distances>=r))[0])
     outerarea=np.pi*(r+step)**2
     innerarea=np.pi*r**2
     area=outerarea-innerarea
     density=float(count)/float(area)
     counts.append(density)
     r=r+step
     radii.append(r)
   return radii, counts

def radialDistance(x,y,Xvector,Yvector):
      xdistance=Xvector-x
      ydistance=Yvector-y
      dist=np.sqrt(xdistance**2+ydistance**2)
      return dist

#def Poisson(data):
#   mu = np.mean(data);
 
def gaussian(xdata,ydata,distribution):
   xmean=np.mean(xdata);
   ymean=np.mean(ydata);
   distances=radialDistance(xmean,ymean,xdata,ydata)
   mean=np.mean(distances)
   std=np.std(distances,ddof=1)
   norm=1/(std*np.sqrt(2*np.pi))
   numerator=-((distribution-mean)**2)
   denominator=2*std**2
   exponent=numerator/denominator
   return norm*np.exp(exponent)
     
   

con=psycopg2.connect("dbname='stars' host='localhost' user='postgres'")
cur=con.cursor()
cur.execute("select raj2000, dej2000 from alphaperprevmembers")
data=cur.fetchall()
ra=[datum[0] for datum in data]
de=[datum[1] for datum in data]
ramid=np.median(ra)
demid=np.median(de)
cur.execute("select raj2000, dej2000 from workingcatalog where sqrt((raj2000-{0})^2+(dej2000-{1})^2) < 5".format(ramid, demid))
data=cur.fetchall()
cra=[datum[0] for datum in data]
cde=[datum[1] for datum in data]

print "calculating radial distances of known members"
knowndistance=radialDistance(ramid,demid,ra,de)
print "%d\ncalculating radial distances of catalog members".format(len(knowndistance))
print len(knowndistance)
catdistance=radialDistance(ramid,demid,cra,cde)
print "%d\nradial distances calculated".format(len(catdistance))
print len(catdistance)
#combra=np.array(r+cra)
#combde=np.array(de+cde)
#distance=np.array([np.sqrt((ra[i]-ramid)**2+(de[i]-demid*2) for i in range (0,len(ra)))])
#catdistance=np.array([np.sqrt((ra[i]-ramid)**2+(de[i]-demid)**2) for i in range(0,len(catra))])
#catPDF is the probability of something having a radius is it is the set of catalog stars
catPDF=1./(np.max(catdistance)-np.min(catdistance))
catDens=len(cra)/(np.pi*25)
print np.max(catdistance)
totaldistance=np.concatenate((catdistance,knowndistance))


x,D = calculateAreaRadialDensity(totaldistance, 5./60., 5)
#plt.scatter(x,y)
y=np.array(D)
y=y-catDens
plt.scatter(x,y)
plt.show()
   

totra=np.concatenate((ra,cra))
totde=np.concatenate((de,cde))
distro=np.linspace(0,max(totaldistance),1000000)
gaussHauss=gaussian(totra,totde,distro)
plt.plot(distro,gaussHauss)
plt.show()
print gaussHauss
