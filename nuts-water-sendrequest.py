import requests
import json

#r = requests.get('http://www.grootwassink.nl/nuts/api/v1/api.php/water',verify=False, json={"value": 3})

head = {'Content-type': 'application/json'}
payload = {"registrationdate":"2017-01-26 22:36:00","value":"1"}
r = requests.get('http://www.grootwassink.nl/nuts/api/v1/api.php/water', data=json.dumps(payload), headers=head)
print(r.status_code)
      
