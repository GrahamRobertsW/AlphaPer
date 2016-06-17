import numpy as np
import psycopg2
import rpy2.robjects as ro
r=ro.r
from rpy2.robjects import numpy2ri
from scipy import integrate as integ
numpy2ri.activate()
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
def rdist(x,y,xm,ym):
    return np.sqrt((x-xm)**2+(y-ym)**2)
def rdistc(x,y,xm,ym):
    return np.sqrt(((x-xm)*np.cos(y*np.pi/180))**2+(y-ym)**2)
def gaussian(data):
    stdev=float(np.std(data))
    M=float(np.mean(data))
    norm=1/(np.sqrt(2*np.pi)*stdev)
    denom=2*stdev**2
    def func(x):
        expo=float(-((x-M)**int(2))/denom)
        return norm*np.e**expo
   # norm=norm/numerical_integral(func,0,100,max_points=1000)[0]
    p, i = cumulativeTrap(func)
    norn=norm/i[len(i)-1]
    def func2(x):
         expo=float(-((x-M)**int(2))/denom)
         return norm*np.e**expo
    return func2
def cumulativeTrap(func):
   points = np.linspace(0,5,1000)
   w=float(max(points))/float(len(points))
   print w
   samples = [func(i) for i in points]
   traps = [(samples[i]+samples[i+1])*float(w/2) for i in range(len(samples)-1)]
   intes=[0]*len(points)
   for i in range(1,len(points)):
       intes[i]=intes[i-1]+traps[i-1]
   return points, intes
cur.execute("select raj2000, dej2000, pmra, pmde, _2mkey from alphaperprevmembers;")
kdata=cur.fetchall()
kra=np.array([datum[0] for datum in kdata])
kde=np.array([datum[1] for datum in kdata])
kpmra=np.array([datum[2] for datum in kdata])
kpmde=np.array([datum[3] for datum in kdata])
kkey=np.array([datum[4] for datum in kdata])
ram=np.mean(kra)
dem=np.mean(kde)
pmram=np.mean(kpmra)
pmdem=np.mean(kpmde)
ksdist=rdistc(kra,kde,ram,dem)
kpdist=rdist(kpmra,kpmde,pmram,pmdem)
f=gaussian(ksdist)
g=gaussian(kpdist)
cur.execute("select raj2000, dej2000, pmra, pmde, _2mkey from workingcatalog")
data=cur.fetchall()
cra=np.array([datum[0] for datum in data])
cde=np.array([datum[1] for datum in data])
cpmra=np.array([datum[2] for datum in data])
cpmde=np.array([datum[3] for datum in data])
ckey=np.array([datum[4] for datum in data])
csdist=rdistc(cra,cde,ram,dem)
cpdist=rdist(cpmra,cpmde,pmram,pmdem)
print "creating radial probability Gaussians"
spaRP=gaussian(csdist)
proRP=gaussian(cpdist)
spap=np.array([float(1.-integ.quad(f,0,i)[0]) for i in ksdist])
print "k spacial {0}".format(max(spap))
prap=np.array([float(1.-integ.quad(g,0,i)[0]) for i in kpdist])
print "k Proper{0}".format(max(prap))
cpap=np.array([float(1.-integ.quad(f,0,i)[0]) for i in csdist])
print "c spacial{0}".format(max(cpap))
crap=np.array([float(1.-integ.quad(g,0,i)[0]) for i in cpdist])
print "c proper{0}".format(max(crap))
KSRP=np.array([float(1.-integ.quad(spaRP,int(0),float(i))[0]) for i in ksdist])
print "k s rad{0}".format(max(KSRP))
KPRP=np.array([float(1.-integ.quad(proRP,int(0),float(i))[0]) for i in kpdist])
print "k p rad{0}".format(max(KPRP))
CSRP=np.array([float(1.-integ.quad(spaRP,int(0),float(i))[0]) for i in csdist])
print "c r rad{0}".format(max(CSRP))
CPRP=np.array([float(1.-integ.quad(proRP,int(0),float(i))[0]) for i in cpdist])
print "c p rad{0}".format(max(CPRP))
knownSpatialProbs=(spap/KSRP)
knownProperProbs=(prap/KPRP)
catSpatialProbs=(cpap/CSRP)
catProperProbs=(crap/CPRP)
knownSpatialProbs=knownSpatialProbs*(1./np.sum(knownSpatialProbs))
knownProperProbs=knownProperProbs*(1./np.sum(knownProperProbs))
catSpatialProbs=knownSpatialProbs*(1./np.sum(catSpatialProbs))
catProperProbs=catProperProbs*(1./np.sum(catProperProbs))
pm=700./len(csdist)
knownSpatialProbs=knownSpatialProbs*pm
knownProperProbs=knownSpatialProbs*pm
catSpatialProbs=catProperProbs*pm
catProperProbs=catProperProbs*pm
#knownSpatialProbs=knownSpatialProbs*(700./np.sum(knownSpatialProbs))
#knownProperProbs=knownProperProbs*(700./np.sum(knownProperProbs))
#catSpatialProbs=catSpatialProbs*(700./np.sum(catSpatialProbs))
#catProperProbs=catProperProbs*(700./np.sum(catProperProbs))
print np.sum(knownSpatialProbs)
print np.sum(knownProperProbs)
print np.sum(catProperProbs)
print np.sum(catSpatialProbs)

print "dropping old table"
cur.execute("drop table plotdata")
con.commit()

#
print "creating table"
cur.execute("create table plotdata (raj2000 double precision, dej2000 double precision, pmra double precision, pmde double precision, spacialDist double precision, properDist double precision, spacialProb double precision, properProb double precision, _2mkey character varying, knownmember integer)")
con.commit()
print "populating table"
for i in range(len(kra)):
   cur.execute("insert into plotdata (raj2000, dej2000, pmra, pmde, spacialDist, properDist, spacialProb, properProb, _2mkey, knownmember) values ({0},{1},{2},{3},{4},{5},{6},{7},cast({8} as character varying),1);".format(kra[i],kde[i],kpmra[i],kpmde[i],ksdist[i],kpdist[i],knownSpatialProbs[i],knownProperProbs[i],kkey[i]))
for i in range(len(cra)):
       cur.execute("insert into plotdata (raj2000, dej2000, pmra, pmde, spacialDist, properDist, spacialProb, properProb, _2mkey, knownmember) values ({0},{1},{2},{3},{4},{5},{6},{7},cast({8} as character varying),0);".format(cra[i],cde[i],cpmra[i],cpmde[i],csdist[i],cpdist[i],catSpatialProbs[i],catProperProbs[i],ckey[i]))
con.commit()
print "done"
