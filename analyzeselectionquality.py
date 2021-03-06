import psycopg2
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects import numpy2ri
from matplotlib import pyplot as plt
r=ro.r
numpy2ri.activate()
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()

def rdist(x,y,xm,ym):
   return np.sqrt((x-xm)**2+(y-ym)**2)

cur.execute("select raj2000, dej2000, pmra, pmde, pp from conditionals where _2mkey not in (select _2mkey from alphaperprevmembers);")
data=cur.fetchall()
cra=np.array([datum[0] for datum in data])
cde=np.array([datum[1] for datum in data])
cpmra=np.array([datum[2] for datum in data])
cpmde=np.array([datum[3] for datum in data])
cpp=np.array([datum[4] for datum in data])
cur.execute("select raj2000, dej2000, pmra, pmde, pp from conditionals where _2mkey in (select _2mkey from alphaperprevmembers);")
data=cur.fetchall()
kra=np.array([datum[0] for datum in data])
kde=np.array([datum[1] for datum in data])
kpmra=np.array([datum[2] for datum in data])
kpmde=np.array([datum[3] for datum in data])
kpp=np.array([datum[4] for datum in data])
ram=np.mean(kra)
dem=np.mean(kde)
pmram=np.mean(kpmra)
pmdem=np.mean(kpmde)
ksdist=rdist(kra,kde,ram,dem)
kpdist=rdist(kpmra,kpmde,pmram,pmdem)
csdist=rdist(cra,cde,ram,dem)
cpdist=rdist(cpmra,cpmde,pmram,pmdem)
#r.png('spacialdist.png', height=480, width=480)
#r.plot(csdist,cpp,xlab='radial distance',main='',ylab='probability')
#r.points(ksdist,kpp,col='magenta')
#r.legend('topright', legend=np.array(['catalog', 'known member']), pch='o', col=np.array(['black','magenta']))
#n=raw_input()
#r.png('pmdist.png', height=480, width=480)
#r.plot(cpdist,cpp,xlab='proper motion distance',main='',ylab='probability')
#r.points(kpdist,kpp,col='magenta')
#r.legend('topright', legend=np.array(['catalog', 'known member']), pch='o', col=np.array(['black','magenta']))

#m=raw_input()
#r.hist(cpp,type='h',main='', xlab='', log='y', ylab='',freq=False)
#n=raw_input()
plt.hist(cpp, bins=12, log=True, normed=True, alpha=0.5)
plt.title('catalog members')
plt.xlabel('probability')
plt.ylabel('')
plt.show()
plt.hist(kpp, bins=12, log=True, normed=True, alpha=0.5, color='red')
plt.title('known members')
plt.xlabel('probability')
plt.show()
