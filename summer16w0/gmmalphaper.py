import numpy as np
import pandas as pd
import psycopg2
from matplotlib import pyplot as plt
from sklearn.mixture import GMM
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select raj2000, dej2000, pmra, pmde, _2mkey from workingcatalog")
df=pd.DataFrame(cur.fetchall(),columns=['ra','de','pmra', 'pmde', 'key'])
data=np.array((df['ra'],df['de'],df['pmra'],df['pmde'])).T
model=GMM(n_components=2, covariance_type='spherical')
model.fit(data)
df['clabel']=pd.Series(model.predict(data),index=df.index)
print df
print len(np.where(df['clabel']==1)[0])
plt.scatter(df['pmra'],df['pmde'],c=df['clabel'],alpha=0.3)
plt.show()
