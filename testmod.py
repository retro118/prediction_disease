apikey='AIzaSyByksrWBWJYbWJenGuIhUZXVceTh5sNjqI'
location_string = 'Mountain View, CA'
r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address="%s"&key=%s' % (location_string, apikey))
print (r)