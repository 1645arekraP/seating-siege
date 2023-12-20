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
            if self.__hasValidURL(course):
                self.__courses.append(course)

    def __hasValidURL(self, course: Course) -> bool:
        try:
            self.__scrapeCourse(course)
            return True
        except IndexError:
            print(f"Could not find index value that is associated with the course. Try checking if you entered course info correctly. CRN: {course.crn}")
        except requests.exceptions.InvalidURL:
            print(f"Invalid URL, make sure your university portal uses the same scheme as described. If not, change the base URL of the course. CRN: {course.crn}")
        except requests.exceptions.ConnectionError:
            print(f"Connection Timeout")
        return False

    def __getPageContents(self, course: Course) -> str:
        if self.__proxy:
            return requests.get(course.url, proxies=self.__proxy, verify=False).content
        return requests.get(course.url).content
    
    def __scrapeCourse(self, course: Course) -> str:
        # Probably a better way of getting the number of seats available
        soup = BeautifulSoup(self.__getPageContents(course), 'html.parser')
        portalTable = soup.findAll('table')[3]

        return portalTable.findAll('td')[5].getText()

    def __hasOpenSeat(self, course: Course) -> bool:
        seatsAvailable = self.__scrapeCourse(course)
        return len(seatsAvailable) > 1 or ord(seatsAvailable) != 160
    
    def __scrapeAllCourses(self, phone: Phone) -> None:
        for course in self.__courses:
            if self.__hasOpenSeat(course):
                if phone:
                    phone.sendSMS("Has Open Spot")
                self.__courses.remove(course)
                print(self.__scrapeCourse(course))

            time.sleep(random.uniform(10, 15))
        time.sleep(random.uniform(30, 60)) # These might be an issue later idk

    def start(self, phone: Phone = None) -> None:
        if phone:
            phone.sendSMS("Starting...")
        while self.__courses:
            self.__scrapeAllCourses(phone)
        print("Done")
        if phone:
            phone.sendSMS("No courses left")