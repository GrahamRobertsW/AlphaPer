import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.io import fits
import psycopg2
con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
cur.execute("create table UPC (upc integer, raj2000 double precision, dej2000 double precision, Name varchar(30), f_mag double precision, relpi double precision, picor double precision, corflg varchar, abspi double precision, e_abspi double precision, pmRA double precision, e_pmra double precision, pmde double precision, e_pmde double precision, ne integer, nr integer, espan double precision, elo double precision, fsig1 double precision, fsig2 double precision, srcflg double precision, srcpi double precision, e_srcpi double precision, simbadname varchar(30));")
con.commit()
infile=fits.open('../resources/UPC.fit')
names=infile[1].data.columns.names
for row in infile[1].data:
	cur.execute("insert into upc ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},{22},{23}) values ({24},{25},{26},('{27}'::varchar(30)),{28},{29},{30},({31}::varchar),{32},{33},{34},{35},{36},{37},{38},{39},{40},{41},{42},{43},{44},{45},{46},('{47}'::varchar(30)))".format(names[0],names[1],names[2],names[3],names[4],names[5],names[6],names[7],names[8],names[9],names[10],names[11],names[12],names[13],names[14],names[15],names[16],names[17],names[18],names[19],names[20],names[21],names[22],names[23],row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23]))
con.commit()
