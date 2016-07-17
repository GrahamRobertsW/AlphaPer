import psycopg2 as p2
import pandas as pd
import numpy as np
from psycoiso import apiso
from matplotlib import pyplot as plt
def chi2(val, mod, e):
   return (val-mod)**2/e

def row2dict(df, val):
   dict={}
   for col in df.columns:
      dict[col]=df[col][val]
   return dict

def staronmodel(st,iso):
   error=np.array([chi2(st['J'],iso['J'][i],st['e_J'])+chi2(st['H'],iso['H'][i],st['e_H'])+chi2(st['K'],iso['K'][i],st['e_K'])/3. for i in range(len(iso))])
   return min(error)

def shiftiso(iso, lins):
   dict={}
   for col in iso.columns:
      dict[col]=iso[col]+lins
   return pd.DataFrame(dict)

def testfitiso(ap,iso,lins):
   testiso=shiftiso(iso,lins)
   n= sum([staronmodel(row2dict(ap, i), testiso) for i in range(len(ap))])/len(ap)
   return n

def testlins(ap, isos, lins):
   n = sum([testfitiso(ap, isos[i], lins) for i in isos.keys()])/len(isos.keys())
   return n

def newmin(f, xo, h):
   def first(x):
      return (f(x+h)-f(x))/h

   def second(x):
      return(f(x-h)-2*f(x)+f(x+h))/h**2

   x0=xo
   diff=first(x0)
   x1=x0-diff/second(x0)
   while diff>h*x0:
      x0=x1
      diff=first(x0)   
      x1=x0-diff/second(x0)
   return x1

parsec=apiso()
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("select jmag, hmag, kmag, e_jmag, e_hmag, e_kmag from alphaperprevmembers where jmag>=6 and jmag<=9.25 and (jmag-kmag)<=0.31")
alpha=pd.DataFrame(cur.fetchall(),columns=['J', 'H', 'K', 'e_J', 'e_H', 'e_K'])
def funx(x):
   return testlins(alpha, parsec, x)

shifts=np.arange(5,6,.0001)
fits=np.array([funx(i) for i in shifts])
plt.scatter(shifts, fits, 'k.')
ss=np.argmin(5.+.01*fits)
print "the minimum fit occurs at a linear shift of {0}\nthis coresponds to a distance of {1} Parsecs".format(ss, 10**(ss/5.+1))

#
#n=newmin(funx, 5.8, np.sqrt(np.finfo(float).eps))
#n2=newmin(funx,6.28, np.sqrt(np.finfo(float).eps))
#print "{0}@{1} Vs {2}@{3}".format(funx(n),n,funx(n2),n2)
