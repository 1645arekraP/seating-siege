#from scraper import Scraper
from course import Course
from scraper import Scraper
from phone import Phone

import os
from dotenv import load_dotenv 

if __name__ == "__main__":
    load_dotenv()

    #phone = Phone(os.getenv("MY_NUMBER"), os.getenv("TWILIO_NUMBER"), os.getenv("ACC_SID"), os.getenv("AUTH_TOKEN"))
    scraper = Scraper(os.getenv("PROXY"))
    scraper.addCourses(Course(os.getenv("UNI_ONE"), crse_in="3262", term_in="202401", subj_in="MATH", crn_in="14359"))
    scraper.start()
