import numpy as np
def radecdist(ra,de,ramid,demid):
	ram=ramid*np.pi/180
	dem=demid*np.pi/180
	s=len(ra)
	rar=ra*np.pi/180
	der=de*np.pi/180
	x=np.cos(der)*np.sin(rar)
	y=np.sin(der)
	z=np.cos(der)*np.cos(rar)
	xm=np.cos(dem)*np.sin(ram)
	ym=np.sin(dem)
	zm=np.cos(dem)*np.cos(ram)
	d=np.sqrt((x-xm)**2+(y-ym)**2+(z-zm)**2)
	a=(2*np.arcsin(d/2))*180/np.pi
#	print x-xm
#	print y-ym
#	print z-zm
	return a
	
