import matplotlib.pyplot as plt
import pandas as pd
import psycopg2 as p2
con=p2.connect("dbname='parsec' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select u, b, v, r, i, j, h, k from yr8_1285e07_z021;")
iso=pd.DataFrame(cur.fetchall(),columns=['u','b','v','r','i','j','h','k'])
cur.close()
con.close()
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select vmag, b_v from makarov2;")
df=pd.DataFrame(cur.fetchall(),columns=['mag','col'])
plt.plot(iso['b']-iso['v'],iso['v'],'m-')
plt.title('Makarov, z=0.021, age=81Myr')
plt.xlabel('B-V')
plt.ylabel('V magnitude')
plt.ylim([max(iso['v'])+1,min(iso['v'])-1])
plt.scatter(df['col'],df['mag']-6.2,color='c')
plt.show()
cur.execute("select vmag, b_v from prosser1992.table4;")
df=pd.DataFrame(cur.fetchall(),columns=['mag','col'])
plt.plot(iso['b']-iso['v'],iso['v'],'m-')
plt.title('Prosser 1992 Table4,, z=0.021, age=81Myr')
plt.xlabel('B-V')
plt.ylabel('V magnitude')
plt.ylim([max(iso['v'])+1,min(iso['v'])-1])
plt.scatter(df['col'],df['mag']-6.2,color='c')
plt.show()
