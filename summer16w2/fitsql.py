import re
from astropy.io import fits
import psycopg2 as p2
types={'B':'bytea','I':'integer','A':'varchar','D':'double precision','E':'double precision'}
varchar=re.compile(r'(\d*)([a-zA-Z])')
inval=re.compile(r'[+=\-\.\ ~]')
numstars=re.compile(r'^\d')
filefind=re.compile(r'(.*\/)?(.*).fit(s)?')
def resolve(string):
   if len(string)>1:
      gs=varchar.search(string).groups()
      return ('{0}({1})'.format(types[gs[1]],gs[0]))
   else:
      return types[string]

def charcast(s,dt):
   if s!='' and s !='nan':
      return "('{0}'::{1})".format(s,resolve(dt))
   else:
      return 'NULL'

def condition(names):
   c=[inval.sub('_',i) for i in names]
   for i in c:
      if numstars.search(i):
         i='_'+i
   return c
   
def creationvals(names, types):
   c=condition(names)
   pairs=['{0} {1}'.format(c[i], resolve(types[i])) for i in range(len(names))]
   vals=', '.join(pairs)
   return vals

def importline(names, types, values, **kwargs):
   if kwargs:
      if 'n_values' not in kwargs:
         kwargs['n_values']=['nan', 'Nan', None, 'None', 'none', 'NULL', 'null', 'Null', 'Nil', 'NIL', 'nil', 'NONE', 'NAN', 'NaN', '']
   else:

      kwargs['n_values']=['nan', 'Nan', None, 'None', 'none', 'NULL', 'null', 'Null', 'Nil', 'NIL', 'nil', 'NONE', 'NAN', 'NaN', '']
   s=len(names)
   assert len(names)==s and len(names)==s and len(types)==s, "Input arrays must have same dimension"
   c=condition(names)
   name_string=', '.join(c)
   b=['NULL']*s
   for i in range(len(values)):
      if str(values[i]) not in kwargs['n_values']:
         t=resolve(types[i])
         if 'varchar' in t or 'bytea' in t:
            b[i]=charcast(b[i], types[i])
         else:
            b[i]=str(values[i])
   val_string=', '.join(b)
   return '({0}) values ({1})'.format(name_string, val_string)

def upfile(path, dbname):
   n=fits.open(path)
   names=n[1].data.names
   fmts=n[1].data.formats
   tname=condition([filefind.search(path).group(2)])[0]
   new_string=creationvals(names, fmts)
   con=p2.connect("dbname='{0}' user='postgres' host='localhost'".format(dbname))
   cur=con.cursor()
   cur.execute("create table {0} ({1})".format(tname, new_string))
   con.commit()
   for i in n[1].data:
      line=importline(names, fmts, i)
      cur.execute("insert into {0} {1};".format(tname, line))
   con.commit()
   
   

