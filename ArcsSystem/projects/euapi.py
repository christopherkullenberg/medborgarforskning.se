import os
import requests
import json

def api_get_projects():
    data = requests.get('https://eu-citizen.science/api/projects/')
    print("EUAPI Response code: " + str(data.status_code))
    jsondata = data.json()
    #text = json.dumps(jsondata, sort_keys=True, indent=4)
    #contentlist = []
    #for t in text:
        #contentlist.append(t)
    return jsondata
