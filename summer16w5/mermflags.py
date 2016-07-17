import pandas as pd
import psycopg2 as p2
import matplotlib.pyplot as plt
df=pd.DataFrame
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select ujmag-ukmag, ujmag from umer;")
mer=df(cur.fetchall(), columns=['col','mag'])
plt.scatter(mer['col'],mer['mag'])
plt.show()
