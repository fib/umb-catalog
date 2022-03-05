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
    number: str
    title: str
    credits: int


subjects = [
    "AF",
    "AFRSTY",
    "AMST",
    "ANTH",
    "ARABIC",
    "ART",
    "ASAMST",
    "ASIAN",
    "ASP",
    "BIOCHM",
    "BIOL",
    "BC",
    "CAPS",
    "CHEM",
    "CHINSE",
    "CINE",
    "CLSICS",
    "COMM",
    "CS",
    "COUNSL",
    "CSP",
    "CRW",
    "DANCE",
    "ECHD",
    "ECON",
    "EDC U",
    "ENGIN",
    "ENGL",
    "ESL",
    "ENVSCI",
    "ENVSTY",
    "EHS",
    "FRENCH",
    "SEMINR",
    "GERMAN",
    "GERON",
    "GLBAFF",
    "GREEK",
    "HLTH",
    "HIST",
    "HONORS",
    "HUMCTR",
    "HUMAN",
    "IT",
    "INTR-D",
    "ITAL",
    "JAPAN",
    "LABOR",
    "LATIN",
    "LATAM",
    "MGT",
    "MSIS",
    "MKT",
    "MATH",
    "IT",
    "MLLC",
    "MUSIC",
    "NAIS",
    "NURSNG",
    "PHIL",
    "PHILLAW",
    "PHYSIC",
    "POLSCI",
    "PORT",
    "CAS",
    "PSYCH",
    "RUSS",
    "SOCIOL",
    "SPAN",
    "SL",
    "RELSTY",
    "SCSM",
    "THRART",
    "USEA",
    "UPCD",
    "VIET",
    "WGS",
]

class_url_pattern = "https://www.umb.edu/course_catalog/courses/ugrd_{}_2022%20Spring"

classes = {}


for subject in subjects:
    s = r.get(class_url_pattern.format(subject)).text

    subject_classes = BeautifulSoup(s, features="html.parser").find_all("a")

    c = []

    for i in subject_classes:
        if a := re.findall(r"^{} \d{{3}}".format(subject), i.text):

            credits_page = r.get(i["href"]).text
            credits = BeautifulSoup(credits_page, features="html.parser")
            credits = credits.find_all("span", {"class": "class-div-info"})[5]

            c.append(
                asdict(
                    Class(
                        a[0].split(" ")[1],
                        i.contents[0].rsplit("\xa0")[-1],
                        int(credits.contents[0][0]),
                    )
                )
            )

    classes[subject] = c
    print(f"{subject} done")


pprint.pp(classes)

with open("./course_catalog.json", "w") as f:
    json.dump(classes, f)
