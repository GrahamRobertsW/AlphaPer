import numpy as np
import psycopg2
import rpy2.robjects as ro
from rpy2.robjects import numpy2ri
numpy2ri.activate()
r=ro.r
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
def rdist(x,y,xm,ym):
    return (np.sqrt((x-xm)**2+(y-ym)**2))
cur.execute("select raj2000, dej2000, pmra, pmde, pgr, pgpm, _2mkey from nconditionals")
data=cur.fetchall()
ra=np.array([datum[0] for datum in data])
de=np.array([datum[1] for datum in data])
pmra=np.array([datum[2] for datum in data])
pmde=np.array([datum[3] for datum in data])
pgr=np.array([datum[4] for datum in data])
pgpm=np.array([datum[5] for datum in  data])
key=np.array([datum[6] for datum in data])
cur.execute("Select raj2000, dej2000, pmra, pmde from alphaperprevmembers")
knowns=cur.fetchall()
ram=np.mean([datum[0] for datum in data])
dem=np.mean([datum[1] for datum in data])
pmram=np.mean([datum[2] for datum in data])
pmdem=np.mean([datum[3] for datum in data])
sidst=rdist(ra,de,ram,dem)
pidst=rdist(pmra,pmde,pmram,pmdem)
r.png('~/astro/AlphaPer/SpacialDistribution.png',height=int(480),width=int(480))
r.plot(sidst,pgr,xlab='Spacial Radial Distance [Deg]',ylab='Probability (not normalized)', color='purple',main='')
r.png('~/astro/AlphaPer/PMDistribution.png',height=int(480),width=int(480))

r.plot(pidst,pgpm,xlab='Proper Motion Radial Distance [mas/y]',ylab='Probability (not normalized)', color='purple',main='')

