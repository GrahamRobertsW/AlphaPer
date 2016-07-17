import psycopg2 as p2
infile=open('../resources/PARSECmodels.dat','r')
con=p2.connect("dbname='parsec' user='postgres' host='localhost'")
cur=con.cursor()
names=[]
end=False
cur.execute("create table years (names varchar);")
con.commit()
for i in range(13):
   line=infile.readline()
while line!='':
   if line[0]=='#':
      temp=line.split()[16].split('.')
      n='yr'+temp[0]+'_'+temp[1].split('+')[0]+temp[1].split('+')[1]
      names=names+[n]
      infile.readline()
      cur.execute("create table {0} (Z double precision, log_age_yr double precision, M_ini double precision, M_act double precision, logL_lo double precision, logTe double precision, logG double precision, mbol double precision, U double precision, B double precision, V double precision, R double precision, I double precision, J double precision, H double precision, K double precision, int_IMF double precision, stage integer);".format(names[-1]))
      con.commit()
      cur.execute("insert into years (names) values ('{0}'::varchar)".format(names[-1]))
   else:
      vals=line.split()
      cur.execute("insert into {0} (Z, log_age_yr, M_ini, M_act, logL_Lo, logTe, logG, mbol, U, B, V, R, I, J, H, K, int_IMF, stage) values ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18});".format(names[-1],vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],vals[7],vals[8],vals[9],vals[10],vals[11],vals[12],vals[13],vals[14],vals[15],vals[16],vals[17]))
   line=infile.readline()

