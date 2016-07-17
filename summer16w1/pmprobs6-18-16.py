import pandas as pd
from sklearn.mixture import GMM
import psycopg2 as p2
from rpy2.robjects import r
from rpy2.robjects import pandas2ri
from rpy2.robjects import FloatVector as c
import numpy as np
pandas2ri.activate()
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select pmra, pmde from alphaperprevmembers")
known=pd.DataFrame(cur.fetchall(),columns=['pmra','pmde'])
cur.execute("select pmra, pmde from sheikhi where pm =0")
df2=pd.DataFrame(cur.fetchall(), columns=['pmra','pmde'])
known=known.append(df2, ignore_index=True)
cur.execute("select pmra, pmde from workingcatalog")
cat=pd.DataFrame(cur.fetchall(),columns=['pmra','pmde'])
randy=known.append(cat.sample(len(known)),ignore_index=True)
data=np.array((randy['pmra'],randy['pmde'])).T
nModels=2
model=GMM(2,'full')
model.fit(data)
cat['c']=model.predict(cat)
#tdf=pd.DataFrame(model.predict_proba(cat),columns=list('AB'))
#cat['a']=tdf['A']
#cat['b']=tdf['B']
#r.library(scatterplot3D)
#r.scatterplot3D(cat['pmra'],cat['pmde'],cat['a']+cat['b'])
import matplotlib.pyplot as plt
plt.scatter(cat['pmra'], cat['pmde'], c=cat['c'])
plt.show()
print sum(cat['c'])
