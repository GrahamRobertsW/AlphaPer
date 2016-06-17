import numpy as np
import psycopg2
import rpy2.robjects as ro
r=ro.r
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
from astropy.io import fits
from astropy.coordinates import SkyCoord
from matchCatalog import matchCatalog
import matplotlib.pyplot as plt
from radecdist import radecdist

outfiel=open("dhc.txt", "w")
#dhc DEACON HAMBKY COMPARISON
#considering the membership probabilities I have computed
#We match stars to the deacon\hambly survey
#they also compute membership probabilities
#we use the mathCatalog algorithm with J'Niel's modification to pair stars
#we then create a plot of D&H probability with mine

#part one is importing the probabilities that I computed from my sql database
#I have them saved in the btable called plotdata I used to make my poster
#raj2000, and dej2000 are coordinates used to match stars
#spacial prob is the probability based off spacial distance
#properprob is the probability based off proper motion
#I used the product D&H only used pm computation
#So I will compare both the validity of using both, and the accuracy of my pm comp
cur.execute("select raj2000, dej2000, spacialprob, properprob from plotdata where knownmember=1")
data=cur.fetchall()
kra=np.array([datum[0] for datum in data])
kde=np.array([datum[1] for datum in data])
kp=np.array([datum[2]*datum[3] for datum in data])
kpmp=np.array([datum[3] for datum in data])

#now we open the fit file of hihg membership stars from the Deacon&Hambly
dhf=fits.open("../DeaconHamblydata/DeaconHambly2004.HighProb.fit")
dhra=dhf[1].data.field('RAJ2000')
dhde=dhf[1].data.field('DEJ2000')
dhp=dhf[1].data.field('Prob')

mycoords=SkyCoord(kra,kde,unit='deg')
dhcoords=SkyCoord(dhra,dhde,unit='deg')

matches, dist = matchCatalog(dhcoords,mycoords,1.0,0)
print matches
pp=[]
ppm=[]
for i in matches:
	nm, na = matchCatalog(SkyCoord(np.array(kra[i]),np.array(kde[i]),unit='deg'),dhcoords,1.0,0)
#	print nm
	if nm.size>0:
		pp=pp+[(kp[i],dhp[nm])]
		ppm=ppm+[(kpmp[i],dhp[nm])]
		outfiel.write("kra{0}\tkde{1}\thgra{2}\tdhde{3}\tkp{4}\tdhp{5}\n".format(kra[i],kde[i],dhra[nm],dhde[nm],kp[i],dhp[nm]))
print len(pp)
kpp=[i[0] for i in ppm]
dhpp=[i[1] for i in ppm]
plt.plot(kpp, dhpp, 'm.')
plt.show()
dha=radecdist(dhra,dhde,np.mean(dhra),np.mean(dhde))
#print dha
#print dhpp
plt.plot(dha,dhp,'k.')
plt.show()
