#!/usr/bin/env python3

# This script will attempt to scrape all classes from the catalog URL provided.
# It is not guaranteed to generate correct data, but it should at least generate
# a good starting point, which can then be corrected manually.

from dataclasses import dataclass, asdict
import re

from bs4 import BeautifulSoup
import requests as r

import json
import pprint


@dataclass
class Class:
    n: str  # number
    t: str  # title
    c: int  # credits


subject_listings_url = "https://www.umb.edu/course_catalog/listing/ugrd"
course_listings_url = "https://www.umb.edu/course_catalog/courses/ugrd_{subject}_all"
course_info_url = "https://www.umb.edu/course_catalog/course_info/ugrd_{subject}_all_{number}"

courses = {}

subjects_page = r.get(subject_listings_url).text
subjects = BeautifulSoup(subjects_page, 'html.parser').find('div', {'id': 'content'}).find_all('li')
subjects = [ s.text.split(' |')[0].strip() for s in subjects ]

print(f"{len(subjects)} subjects found ({subjects})")


for subject in subjects:
    s = r.get(course_listings_url.format(subject=subject)).text

    subject_courses = BeautifulSoup(s, features="html.parser").find("ul", {"class": "showHideList"}).find_all("li")

    # current subject being processed
    subject_list = []

    for course in subject_courses:
        if h := course.find("h4"):
            course_number = h.text.split("\xa0\xa0")[0].rsplit(' ')[1]
            course_title = h.text.split("\xa0\xa0")[1].replace(" + ", "")

            course_page = r.get(course_info_url.format(subject=subject, number=course_number)).text

            # attempting to retrieve the course credits
            try:
                course_credits = BeautifulSoup(course_page, features="html.parser")
                course_credits = course_credits.find_all("span", {"class": "class-div-info"})[5]
                course_credits = course_credits.contents[0][0]
            except:
                course_credits = "N/A"

            print(f"{subject}{course_number}\t\t({course_credits})\t\t{course_title}")

            subject_list.append(
                asdict(
                    Class(
                        course_number,
                        course_title,
                        course_credits,
                    )
                )
            )

    courses[subject] = subject_list
    print(f"{subject} done")


pprint.pp(courses)

with open("../course_catalog.json", "w") as f:
    json.dump(courses, f)
