import numpy as np
import matplotlib.pyplot as plt
import psycopg2
con=psycopg2.connect("dbname='stars' host='localhost' user='postgres'")
cur=con.cursor()
num=697

def probHist(ll):
   bw=np.std(ll)
   bins=np.zeros(len(ll)/bw+1)
   for l in ll:
      bins[l/bw]+=1
   ta=bw*len(ll)
   probs=bins/ta
   return probs

def rdist(x,y,xm,ym):
   return np.sqrt((x-xm)**2+(y-ym)**2)

def rdistc(x,y,xm,ym):
   return np.sqrt(((x-xm)*np.cos(y))**2+(y-ym)**2)

def probGrad(ph, r, bw):
   return ph[r/bw]

def psycout(ra ,de, pmra, pmde, pgr, pgpm, _2mkey):
   cur.execute("create table nconditionals (raj2000 double precision, dej2000 double precision, pmra double precision, pmde double precision, pgr double precision, pgpm double precision, _2mkey character varying)")
   con.commit()
   for i in range(len(ra)):
      cur.execute("insert into nconditionals (raj2000, dej2000, pmra, pmde, pgr, pgpm, _2mkey) values ({0},{1},{2},{3},{4},{5},cast({6} as character varying));".format(ra[i],de[i],pmra[i],pmde[i],pgr[i],pgpm[i],_2mkey[i]))
   con.commit()
   return()

cur.execute("select raj2000, dej2000, pmra, pmde, _2mkey from alphaperprevmembers")
kdata=cur.fetchall()
kra=np.array([datum[0] for datum in kdata])
ram=np.mean(kra)
kde=np.array([datum[1] for datum in kdata])
dem=np.mean(kde)
kpmra=np.array([datum[2] for datum in kdata])
pmram=np.mean(kpmra)
kpmde=np.array([datum[3] for datum in kdata])
pmdem=np.mean(kpmde)
ksh=probHist(rdistc(kra,kde,ram,dem))
kpmh=probHist(rdist(kpmra,kpmde,pmram,pmdem))

cur.execute("select raj2000, dej2000, pmra, pmde, _2mkey from workingcatalog where sqrt((raj2000-{0})^2+(dej2000-{1})^2)<5".format(ram,dem))
cdata=cur.fetchall()
data=kdata+cdata
PofM=num/len(data)
ra=np.array([datum[0] for datum in data])
de=np.array([datum[1] for datum in data])
pmra=np.array([datum[2] for datum in data])
pmde=np.array([datum[3] for datum in data])
key=np.array([datum[4] for datum in data])
dist=rdistc(ra,de,ram,dem)
pmdist=rdist(pmra,pmde,pmram,pmdem)
hist=probHist(dist)
pmhist=probHist(pmdist)
binw=np.std(dist)
pmbinw=np.std(pmdist)
pgr=np.array([probGrad(hist, i, binw) for i in dist])
pgpm=np.array([probGrad(pmhist, j, pmbinw) for j in pmdist])
psycout(ra,de,pmra,pmde,pgr,pgpm,key)
