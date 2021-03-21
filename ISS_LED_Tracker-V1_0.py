import ephem
import time
import math
from datetime import datetime
import requests
import ISS_Info

degrees_per_radian = 180.0 / math.pi # convert radians to degrees

# function to see if ISS is over observer's horizon
def issOverHorizon():
    # use requests module to extract text file from URL
    response = requests.get("https://www.celestrak.com/NORAD/elements/stations.txt")
    data = response.text
    
    # use string splitting to extract relevant ISS data.
    # this was done by trial and error and may not be accurate when the TLE updates every few weeks
    iss = ephem.readtle(data[:11],
                        data[20:97],
                        data[97:167])
    
    # set home location using ephem Observer function
    home = ephem.Observer()
    home.lon, home.lat = '-2.14857', '51.53511'
    home.elevation = 63 # meters
    
    # check if ISS is over 10 degrees above horizon
    home.date = datetime.utcnow()
    iss.compute(home)
    altitude = iss.alt * degrees_per_radian
    if altitude > 10:
        return True
    else:
        return False

# function to check is ISS is in daylight
def issDaylight():
    # current ISS latitude and longitude from ISS_info module
    issLong = ISS_Info.iss_current_loc()["iss_position"]["longitude"]
    issLat = ISS_Info.iss_current_loc()["iss_position"]["latitude"]
    
    # set the ISS current location as ephem observer to be used in sunrise/set calcs later
    issCurrent = ephem.Observer()
    issCurrent.lat = issLat
    issCurrent.long = issLong
    issCurrent.elevation = 408000 # 408km above surface
    
    # use ephem module to get next sunrise/set times for ISS current location
    next_sunrise_datetime = issCurrent.next_rising(ephem.Sun()).datetime()
    next_sunset_datetime = issCurrent.next_setting(ephem.Sun()).datetime()
    
    # it is day if the next sunset is before the next sunrise
    it_is_day = next_sunset_datetime < next_sunrise_datetime
    
    # should change this to return True/False when integrate neopixel LEDs.
    print("Orange LED" if it_is_day else "Blue LED")

while True:
    if issOverHorizon():
        print("Bright White LED")
    else:
        issDaylight()
    time.sleep(1)