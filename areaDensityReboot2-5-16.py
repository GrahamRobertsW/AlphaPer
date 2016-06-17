import numpy as np
import psycopg2

con=psycopg2.connect("dbname='stars' user='postgres' host='localhost'")
cur=con.cursor()

#first we need to find the center of the cluster

