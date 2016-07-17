import pandas as pd
import psycopg2 as p2
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord as sc
import isotools as it
from matchCatalog import matchCatalog as mc
import re
import numpy as np
df=pd.DataFrame
con=p2.connect("dbname='parsec' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select names from years_z021;")
outfile=open('fitlist','w')
mes=cur.fetchall()
d={}
for i in mes:
   cur.execute("select J, H, K from {0}_z021;".format(i[0]))
   d[i[0]]=df(cur.fetchall(),columns=['J','H','K'])
##   if i[0] == "yr8_1285e07":
##      print i[0]
##models=df(d, index=d.get)
##print d['yr8_1285e07']
##d=None   
##print models[0]
cur.close()
con.close()
ucoldefs=['ra','de','urat1', 'J','e_J','K','e_K','H','e_H']
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select ra, dec, mem from alejandroslist where mem > 50")
ajl=df(cur.fetchall(), columns=['ra','de','mem'])
cur.execute("select raj2000, dej2000, urat1, jmag, e_jmag, kmag, e_kmag, hmag, e_hmag from urat where jmag-kmag<0.6")
urat=df(cur.fetchall(),columns=ucoldefs)
usc=sc(urat['ra'],urat['de'],unit='deg')
asc=sc(ajl['ra'],ajl['de'],unit='deg')
matches, dist = mc(asc, usc, 3.0, 0)
match_df=df(columns=ucoldefs+['mem','col'])
for m in matches:
   tmp=sc(urat['ra'][m],urat['de'][m],unit='deg')
   temp_match,na=mc(tmp, asc, 3.0, 0)
   if temp_match and len(temp_match)>0:
      tdf=df([urat[ucoldefs].values[m]],columns=ucoldefs)
      mem=ajl['mem'].values[temp_match[0]]
      col=['#%02x%02x%02x' % (0,int(255*(.01*mem)),0)]
      tdf['mem']=mem
      tdf['col']=col
      match_df=match_df.append(tdf)
match_df=match_df.set_index('urat1',drop = False)
yrsplit=re.compile(r'yr(\d)_(\d{4})e(\d{2})')
models=df(mes,columns=['name']).set_index('name', drop=False) 
models['age']=0
for m in models['name'].values:
   sp=yrsplit.search(m).groups(0)
   models['age'][m]=(int(sp[0])+(float(sp[1])/10000.))*10**int(sp[2])
maxage= float(max(models['age'].values))
minage= float(min(models['age'].values))
diffage=float(maxage-minage)
###print models['age']
modelcolors=['#%02x%02x%02x' % (int(255*(1-(i-minage)/diffage)),0,int(255 * ((i-minage)/diffage))) for i in models['age'].values]
models['col']=modelcolors
models['a']=0
match_df['x']=match_df['J']-match_df['K']
match_df['ex']=np.sqrt(match_df['e_J']**2+match_df['e_K']**2)
#plt.errorbar(match_df['x'],match_df['J']-6.2,fmt=None,ecolor='k',xerr=match_df['ex'],yerr=match_df['e_J'])
alphaarray=['']*len(models.index.values)
for j in range(len(alphaarray)):
   i=models.index.values[j]
   ff=it.testfitiso(match_df,d[i],6.2)
   alphaarray[j]=1-2*ff
models['a']=alphaarray
   #print 1-2*ff
   #print models['a'][i]
print models['a']
for i in models.index.values:
   plt.plot(d[i]['J']-d[i]['K'],d[i]['J'],color=models['col'][i],alpha=models['a'][i])
   outfile.write('{0}\t{1}\ta={2}\n'.format(models['age'][i],ff,models['a'][i]))
plt.scatter(match_df['x'],match_df['J']-6.2,color=match_df['col'],marker='o')
xmin=float('inf')
xmax=-float('inf')
ymin=float('inf')
ymax=-float('inf')
for i in models.index.values:
   color_of_model=d[i]['J']-d[i]['K']
   if min(color_of_model)<xmin:
      xmin=min(color_of_model)
   if max(color_of_model)>xmax:
      xmax=max(color_of_model)
   if min(d[i]['J'])<ymin:
      ymin=min(d[i]['J'])
   if max(d[i]['J'])>ymax:
      ymax=max(d[i]['J'])
plt.ylim([max(max(match_df['J']-6.2),ymax),min(min(match_df['J']-6.2),ymin)])
plt.xlim([min(min(match_df['x']),xmin),max(max(match_df['x']),xmax)])
plt.ylabel('J-K Magnitude')
plt.xlabel('J magnitude')
plt.show()
outfile.close()
outfile2=open('plotpointdata','w')
for i in match_df.index.values:
   outfile2.write("{0}\t{1}\tC={2}\n".format(i,str(match_df['mem'][i]),str(match_df['col'][i])))
outfile2.close()

