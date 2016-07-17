import psycopg2 as p2
import pandas as pd
import matplotlib.pyplot as plt
df=pd.DataFrame
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select ujmag-ukmag, ujmag from udhhp;")
hd=df(cur.fetchall(), columns=['col','mag'])
plt.scatter(hd['col'],hd['mag'])
plt.show()
