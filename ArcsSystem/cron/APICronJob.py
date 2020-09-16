import requests
from json import loads
from django.conf import settings
from django_cron import CronJobBase, Schedule

class APICronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # Run every 1 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'ArcsSystem.APICronTask'    # A unique code

    def do(self):
        APIKey = settings.SCISTARTER_API_KEY # Get API key defined in settings file
        page = 0
        failedTries = 0 # Number of failed tries for API request
        url = f"https://scistarter.org/p/finder?format=json&key={APIKey}" # Generate URL for API call
        for searchKey in settings.API_SEARCH_QUERY_DICT: # Iterate in search query dict and add them to URL
            url += f"&{searchKey}={settings.API_SEARCH_QUERY_DICT[searchKey]}"
        while True:
            page += 1
            api_url = f"{url}&page={page}" # Add page to URL for API call
            response = requests.get(api_url) # Make an API call
            if response.status_code == 200: # If request is successful
                data = loads(response.content.decode('utf-8')) # Convert response to JSON
                if len(data["entities"]) == 0: # If there are no entities, there will be no more pages, so we can quit the loop
                    break
                for entity in data["entities"]: # Get each entry fetched from API
                    print(entity["id"]) # Just and example for now to make sure it works correctly
            else: # If request failed
                failedTries += 1 # Increase failed tries by one
                if failedTries > 10: # If it has been at least 10 times for failed tries, exit the loop to avoid infinite loop
                    break
