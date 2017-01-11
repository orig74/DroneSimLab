# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import numpy as np
RE=6378.137*1000

#conversion from 
#https://en.wikipedia.org/wiki/Geographic_coordinate_system
from numpy import cos,sin

def latlon_rad_dist_meters(lat1,lon1,lat2,lon2):
    phi=(lat1+lat2 )/2.0
    m_per_deg_lat = 111132.92 - 559.82 * cos( 2 * phi ) + 1.175 * cos( 4 * phi) - 0.0023*cos(6*phi);
    m_per_deg_lon = 111412.84 * cos ( phi ) - 93.5*cos(3*phi)+0.118*cos(5*phi);
    dlat=(lat2-lat1)*180/np.pi*m_per_deg_lat 
    dlon=(lon2-lon1)*180/np.pi*m_per_deg_lon
    return dlat,dlon

if __name__=="__main__":
    dx,dy=latlon_rad_dist_meters(np.radians(35),np.radians(32),np.radians(35.1),np.radians(32.1))
    print(np.sqrt(dx**2+dy**2))

