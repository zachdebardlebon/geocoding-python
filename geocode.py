import json
import boto3
from math import sin, cos, sqrt, atan2, radians
from botocore.vendored import requests

def geocode():
    location = sys.argv[1]
    lat = sys.argv[2]
    lon = sys.argv[3]
    rad = sys.argv[4]

    if location == "current":
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table("###########")
        locs = table.scan()["Items"]
        
	#used for calculating distance
        earthRadius = 6371
        
	#values need to be in radians for this to work
        userLat = radians(float(lat))
        userLon = radians(float(lon))
        
        locationsInRange = []
        
        for i in range(0, len(locs)):
            curLat = radians(float(locs[i]["lat"]))
            curLon = radians(float(locs[i]["long"]))
            
            dlat = curLat - userLat
            dlon = curLon - userLon
            
            a = sin(dlat / 2)**2 + cos(userLat) * cos(curLat) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            
            distance = earthRadius * c
            
            if distance <= float(rad):
                locationsInRange.append(locs[i])
                
        return locationsInRange
    elif location == "search":
        #geocode
        # geo = geocoder.google(address)
        # lat-long = geo.latlng
        return []
    else:
        #reverse geocode
        #preferably 7 decimal places for accuracy
        baseURL = "http://maps.googleapis.com/maps/api/geocode/json?"
        locationParams = "latlng={lat},{lon}&sensor={sen}".format(
            lat=lat,
            lon=lon,
            sen="true"
        )
        url = "{baseURL}{locationParams}".format(baseURL=baseURL, locationParams=locationParams)
        response = requests.get(url)
        return response.json()["results"][0]["formatted_address"]

geocode()
