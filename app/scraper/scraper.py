import requests
from bs4 import BeautifulSoup
import time
import random
import urllib3
from course import Course
from phone import Phone

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TODO Clean Up / Add more exception handling

class Scraper():

    def __init__(self, proxy: str = None):
        self.__courses = []

        if proxy:
            self.__proxy = {"http": proxy}
        else:
            self.__proxy = None
    
    def addCourses(self, *courses : Course):
        for course in courses:
            self.__courses.append(course)

    def __getPageContents(self, course: Course) -> str:
        try:
            if self.__proxy:
                return requests.get(course.url, proxies=self.__proxy, verify=False).content
            return requests.get(course.url).content
        except requests.exceptions.ConnectionError:
            Exception(f"Course URL is not valid: {course.url}")
    
    def __getSeatData(self, course: Course) -> str:
        soup = BeautifulSoup(self.__getPageContents(course), 'html.parser')
        portalTable = soup.findAll('table')[3]

        return portalTable.findAll('td')[5].getText()

    def __hasOpenSeat(self, course: Course) -> bool:
        seatsAvailable = self.__getSeatData(course)
        return len(seatsAvailable) > 1 or ord(seatsAvailable) != 160
    
    def __scrapeAllCourses(self, phone: Phone = None) -> None:
        for course in self.__courses:
            if self.__hasOpenSeat(course):
                phone.sendSMS("Has Open Spot")
                self.__courses.remove(course)
                print(self.__getSeatData(course))

            time.sleep(random.uniform(10, 15))
        time.sleep(random.uniform(30, 60)) # These might be an issue later idk

    def start(self, phone: Phone = None) -> None:
        phone.sendSMS("Starting...")
        while self.__courses:
            self.__scrapeAllCourses(phone)
        print("Done")
        phone.sendSMS("No courses left")