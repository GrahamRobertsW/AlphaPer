import pandas as pd
import matplotlib.pyplot as plt
import psycopg2 as p2
df=pd.DataFrame
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
flagsl=['691_083185','689_082967','689_085302','692_089161','704_103276','700_098103','688_086675','696_095967','702_104296','698_107638','698_101101','691_095768']
ors=["uurat1='{0}'".format(i) for i in flagsl]
cur.execute("select ujmag-ukmag, ujmag, b_v, vmag from upt4 where {0};".format(' or '.join(ors)))
flags=df(cur.fetchall(), columns=['j-k','j','b-v','v'])
cur.execute("select ujmag-ukmag, ujmag, b_v, vmag from upt4;")
pt4=df(cur.fetchall(),columns=['j-k','j','b-v','v'])
cur.close()
con.close()
con=p2.connect("dbname='parsec' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select names from years_z021")
mods=cur.fetchall()
print mods
d={}
for i in mods:
   j=i[0]
   cur.execute("select j-k, j, b-v, v from {0};".format(j+'_z021'))
   d[j]=df(cur.fetchall(),columns=['j-k','j','b-v','v'])
for i in d.keys():
   plt.plot(d[i]['j-k'],d[i]['j']+6.2,color='blue',alpha=0.2)
plt.scatter(pt4['j-k'],pt4['j'])
plt.scatter(flags['j-k'],flags['j'],color='red')
plt.ylim([20,-5])
plt.ylabel('J magnitude')
plt.xlabel('J-K')
#plt.title('Prosser Table 4 outliers J-K')
plt.show()

for i in d.keys():
   plt.plot(d[i]['b-v'],d[i]['v']+6.2,alpha=0.2,color='blue')
plt.scatter(pt4['b-v'],pt4['v'])
plt.scatter(flags['b-v'],flags['v'],color='red')
plt.ylabel('v magnitude')
plt.xlabel('b-v')
plt.ylim([25,-5])
plt.show()
#for i in flagsl:
#   cur.execute("select ujmag-ukmag, ujmag from upt4 where uurat1='{0}';".format(i))
#   tdf=df(cur.fetchall(),columns=['col','mag'])
#   plt.scatter(pt4['col'],pt4['mag'])
#   plt.scatter(tdf['col'],tdf['mag'],color='red')
#   plt.ylim([12,0])
#   plt.ylabel('J magnitude')
#   plt.xlabel('J-K')
#   plt.title(i)
#   plt.show()
