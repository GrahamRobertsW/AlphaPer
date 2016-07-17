import psycopg2 as p2
import matplotlib.pyplot as plt
import pandas as pd
con=p2.connect("dbname='parsec' host='localhost' user='postgres'")
cur=con.cursor()
cur.execute("select names from years_z021;")
names=[i[0] for i in cur.fetchall()]
dict={}
for name in names:
   print name
   n=name[2:].split('e')
   mts=n[0].split('_')
   age=float(mts[0]+'.'+mts[1])*10**int(n[1])
   if (age>3*10**7) and (age<1.5*10**8):
      cur.execute("select J, K from {0}_z021".format(name))
      dict[name]=pd.DataFrame(cur.fetchall(),columns=['j','k'])
maxj=0.
minj=10000000
s=6.2
#s=5.79619566627
#s=6.28
for key in dict.keys():
   df=dict[key]
   df['col']=df['j']-df['k']
   plt.plot(df['col'],df['j']+s)
   if max(df['j']+s)>maxj:
      maxj=max(df['j']+s)
   if min(df['j']+s)<minj:
      minj=min(df['j']+s)
plt.ylim([maxj,minj])
cur.close()
con.close()
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select jmag, kmag from alphaperprevmembers;")
pm=pd.DataFrame(cur.fetchall(),columns=['j','k'])
pm['col']=pm['j']-pm['k']
cur.execute("select jmag, ksmag from sheikhi;")
sh=pd.DataFrame(cur.fetchall(), columns=['j','k'])
sh['col']=sh['j']-sh['k']
cur.close()
con.close()
plt.scatter(pm['col'],pm['j'])
plt.scatter(sh['col'],sh['j'])
xmin=int(min([min(pm['col']),min(sh['col'])]))-.2
xmax=max([max(pm['col']),max(sh['col'])])
plt.xlim([xmin,xmax])
plt.xlabel('J-K color')
plt.ylabel('J magnitude')
plt.show()
print 10**(s/5.+1.)

