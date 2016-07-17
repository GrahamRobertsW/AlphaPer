import pandas as pd
import re
n=re.compile(r'(yr\d_\d+e\d+).*(\d+\.\d*)')
infile=open('bestiso.txt', 'r')
d={}
for r in infile.readlines():
   i = n.search(r).groups()
   d[i[0]]=[1]
print min(d, key=d.get)
