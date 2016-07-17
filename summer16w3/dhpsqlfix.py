import fitsql as fs
from astropy.io import fits
import psycopg2 as p2
con=p2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()
fs.upfile('/home/groberts/astro/DeaconHamblydata/DeaconHambly2004.PrevMemb.fit','stars')
fs.upfile('/home/groberts/astro/DeaconHamblydata/DeaconHambly2004.HighProb.fit','stars')
fs.upfile('/home/groberts/astro/Prosserdata/Prosser1992.Table4.fit','stars')
fs.upfile('/home/groberts/astro/Prosserdata/Prosser1992.Table6.fit','stars')
fs.upfile('/home/groberts/astro/Prosserdata/Prosser1992.Table10.fit','stars')
