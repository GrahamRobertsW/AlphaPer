import psycopg2
con=psycopg2.connect("dbname='stars' host='localhost' user='postgres'")
cur=con.cursor()
inf=open('Table3_Members.tsv')
lines=inf.read().split('\n')
ra=[]
de=[]
Jmag=[]
Ksmag=[]
e_J=[]
e_Ks=[]
pmra=[]
pmde=[]
e_pmra=[]
e_pmde=[]
Mu=[]
alsof=[]
for line in lines[19:len(lines)-1]:
	print line
	d=line.split()
	ra=ra+[float(d[0])]
	de=de+[float(d[1])]
	Jmag=Jmag+[float(d[2])]
	Ksmag=Ksmag+[float(d[3])]
	e_J=e_J+[float(d[4])]
	e_Ks=e_Ks+[float(d[5])]
	pmra=pmra+[float(d[6])]
	pmde=pmde+[float(d[7])]
	e_pmra=e_pmra+[float(d[8])]
	e_pmde=e_pmde+[float(d[9])]
	Mu=Mu+[float(d[10])]
	if str(d[11])!='-':
		alsof=alsof+[str(d[11])]
	else: 
		alsof=alsof+[None]
cur.execute("create table sheikhi (ra double precision, de double precision, Jmag double precision, Ksmag double precision, e_j double precision, e_ks double precision, pmra double precision, pmde double precision, e_pmra double precision, e_pmde double precision, mu double precision, alsof character varying);")
con.commit()
for i in range(len(ra)):
	cur.execute("insert into sheikhi (ra, de, jmag, ksmag, e_j, e_ks, pmra, pmde, e_pmra, e_pmde, mu, alsof) values ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},('{11}'::character varying));".format(ra[i],de[i],Jmag[i], Ksmag[i],e_J[i],e_Ks[i],pmra[i],pmde[i],e_pmra[i],e_pmde[i],Mu[i],alsof[i]))
con.commit()


