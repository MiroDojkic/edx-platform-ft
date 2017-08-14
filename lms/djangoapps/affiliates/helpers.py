from django.conf import settings
import requests

def get_affiliate_coordinates(affiliate):
    geocoding_api_key = settings.GEOCODING_API_KEY
    params = affiliate.address + ',' + affiliate.zipcode + ',' + affiliate.city
    if affiliate.state != 'NA':
        params = params + ',' + affiliate.state

    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + params + ',&key=' + geocoding_api_key
    json_response = requests.get(url).json()

    if len(json_response['results']) < 1:
        return None, None

    location = json_response['results'][0]['geometry']['location']

    return location['lat'], location['lng']
