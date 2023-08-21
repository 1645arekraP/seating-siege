# Scraper is currently in a privated repository
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import time
import random

"""
School has started, and I have very little time to continue this project. My complete web scraper code is within a private repository,
but I plan to implement it here very soon. In the meantime, I have left what works and stripped it of keys as I set everything up.
"""

# For Proxy
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def sendMsg(message: str) -> None:
    client.messages.create(
        to="number",
        from_="number",
        body=message)


def formatURL(subject: str, crse: str, crn: str) -> str:
    return (
'university link here'
.format(subj_in=subject, crse_in=crse, crn_in=crn))


account_sid = 'Twilio SID'
auth_token = 'Twilio Key'
client = Client(account_sid, auth_token)

sendMsg("Starting...")

urls = {}

proxies = {"http": "http://scraperapi:{apiKey}@proxy-server.scraperapi.com:8001".format(apiKey='apiKey')}

noSpots = False
while noSpots:
    for crn, url in urls.items():
        reqs = requests.get(url, proxies=proxies, verify=False)
        soup = BeautifulSoup(reqs.content, 'html.parser')

        try:
            desired_table = soup.findAll('table')[3]
            availableSpots = desired_table.findAll('td')[5]

            if len(availableSpots.getText()) > 1 or ord(availableSpots.getText()) != 160:
                sendMsg("Seat opened up for CRN: {openCRN}!".format(openCRN=crn))
                print("Found a spot spot in CRN: {openCRN}!".format(openCRN=crn))
                noSpots = False

        except Exception as e:
            print("Error: {exception} with course: {crn}".format(crn=crn, exception=e))
            print(url)
        time.sleep(random.uniform(10, 15))

    time.sleep(random.uniform(30, 60))