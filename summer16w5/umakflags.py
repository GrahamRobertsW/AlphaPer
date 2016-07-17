import psycopg2 as p2
import pandas as pd
import matplotlib.pyplot as plt
df=pd.DataFrame
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select b_v, vmag from umak;")
mk=df(cur.fetchall(),columns=['col','mag'])
plt.scatter(mk['col'],mk['mag'])
plt.show()
