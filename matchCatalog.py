
# coding: utf-8

# In[156]:

#imports
import numpy as np
import astropy 
from astropy.io import ascii
import matplotlib.pyplot as plt
import matplotlib
from astropy import units as u
from astropy.coordinates import SkyCoord
#get_ipython().magic(u'matplotlib inline')


# In[136]:

#matches one catalog to another, finding the nearest neighbors. 
#runs through the nearest neighbors finding the neighbors within the given radius
#returns a list of indices from the second catalog of the objects that are within the radius
#of objects within the first catalog, and a list of indices of the distances between 'matches'
#in arcseconds.
#Parameters: 
#coords1: SkyCoord array for smaller catalog
#coords2: SkyCoord array for larger catalog
#radius: float for the matching radius **in arcseconds**
#selfmatch: boolean indicating if the matching between a catalog and itself

def matchCatalog(coords1, coords2, radius, selfmatch):
    if selfmatch:
        #if self matching the returned index array be the same size as coords1, the value
        #at a given index is the index of the closest match to the course at that index
        #the dist array with have the same distance for each index in the pair

        indx, dist2d, dist3d = coords1.match_to_catalog_sky(coords2, 2)
        if indx.size==1:
            if dist2d <=radius*u.arcsecond:
                matches = indx
                dist = dist2d.arcsecond
        else:
            matches = []
            dist = []
            indexMatches = (dist2d <= radius*u.arcsecond).nonzero()
            matches = indx[indexMatches]
            dist = dist2d[indexMatches].arcsecond
    
    
    else:
        indx, dist2d, dist3d = coords1.match_to_catalog_sky(coords2, 1)
        if indx.size==1:
            if dist2d <=radius*u.arcsecond:
                matches = indx
                dist = dist2d.arcsecond
        else:
            matches = []
            dist = []
            indexMatches = (dist2d <= radius*u.arcsecond).nonzero()
            matches = indx[indexMatches]
            dist = dist2d[indexMatches].arcsecond
            
    return matches, dist,



