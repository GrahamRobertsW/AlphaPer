import numpy as np
import matplotlib.pyplot as plt
import psycopg2
con=psycopg2.connect("dbname='stars' host='localhost' user='postgres'")
cur=con.cursor()

def radialdistances(data):
   x=np.array([datum[0] for datum in data])
   y=np.array([datum[1] for datum in data])
   xm=np.mean(x)
   ym=np.mean(y)
   print "{0}:{1}".format(xm,ym)
   dist=np.sqrt([(datum[0]-xm)**2+(datum[1]-ym)**2 for datum in data])
   return dist, xm, ym

def sa(bw,i):
   A=np.pi*bw**2
   outer=(i+1)**2
   inner=i**2
   return A*(outer-inner)

def radialDensities(dist):
   bw=.5
   counts=np.arange(0,max(dist)/bw+1,1)
   A=np.pi*bw**2
   for d in dist:
      counts[d/bw]+=1
   den=np.array([counts[i]/sa(bw,i) for i in range(len(counts))])
   return den

def CountsFromDensities(dens):
   bw=0.5
   counts=np.array([max(0,dens[i])*sa(bw,i) for i in range(len(dens))])
   return counts
cur.execute("select raj2000, dej2000 from alphaperprevmembers")
kdata=cur.fetchall()
D, x, y = radialdistances(kdata)
cur.execute("select raj2000, dej2000 from workingcatalog where (sqrt((raj2000-{0})^2+(dej2000-{1})^2)<5)".format(x,y))
cdata=cur.fetchall()
dist=radialdistances(cdata)[0]
print dist
dens = radialDensities(dist)
print len(dens)
uni=np.mean([dens[i] for i in range(len(dens)-2)])
print dens-uni
print "uniform distribution{0}".format(uni)
#plt.scatter([datum[0] for datum in data], [datum[1] for datum in data])
#plt.show()
print len(kdata)+len(cdata)
print len(cdata+kdata)
data=cdata+kdata
dist=radialdistances(data)[0]
dens=radialDensities(dist)
print len(dens)
excess=dens-uni
print excess
E=CountsFromDensities(excess)
total=np.sum(E)
print "total excess of stars were expecting is {0}".format(total)
