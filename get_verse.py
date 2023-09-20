#!/usr/bin/python3

"""
A simple program to get a verse of scripture from churchofjesuschrist.org

Copyright 2021 Martin Eldredge
Licensed under the MIT License which is included in this project
"""

import random
import requests
import csv
import os
from bs4 import BeautifulSoup

scriptures = {
    "bom": "/scriptures/bom.csv",
    "ot": "/scriptures/oldt.csv",
    "nt": "/scriptures/newt.csv"
}

csv_file = ""
scrip_route = ""
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

scrip_num = random.randrange(3)
if scrip_num == 0:
    csv_file = dname + scriptures["bom"]
    scrip_route = "bofm"
elif scrip_num == 1:
    csv_file = dname + scriptures["nt"]
    scrip_route = "nt"
else:
    csv_file = dname + scriptures["ot"]
    scrip_route = "ot"

url = "https://www.churchofjesuschrist.org/study/scriptures/" + \
    scrip_route + "?lang=eng"
url_base = "https://www.churchofjesuschrist.org/study/scriptures/" + scrip_route + "/"

# Get html from church website
res = requests.get(url)
html = res.content
soup = BeautifulSoup(html, "html.parser")

book_list = []
exclude = [
    "Contents",
    "Introduction and Witnesses  ",
    "Book of Mormon Pronunciation Guide",
    "Reference Guide to the Book of Mormon",
    "Title Page"
]

# Replace non-breaking space with space
for li in soup.ul:
    if (li.get_text() not in exclude):
        book_list.append(li.get_text().replace("\xa0", " "))

book_amnt = len(book_list)

# Choose a random book
random.seed()
randnum = random.randrange(1, book_amnt + 1)
chosen_book = book_list[randnum - 1]
chosen_book = chosen_book.strip()

# Parse the url and get the verse
with open(csv_file) as books:
    reader = csv.reader(books, delimiter=',')
    for row in reader:  # Find the chosen book and pick a verse
        if row[0] == chosen_book:
            chapter = random.randrange(1, int(row[2]) + 1)
            chapter_url = url_base + row[1] + "/" + str(chapter) + "?lang=eng"

            # Get the requested chapter
            res = requests.get(chapter_url)
            html = res.content
            soup = BeautifulSoup(html, "html.parser")
            divs = soup.find_all("div", {"class": "body-block"})
            verses = []

            # Get all the verses
            for p in divs:
                for verse in p:
                    if verse.get_text() not in ("", "\n"):
                        verses.append(str(verse.get_text()))

            # Pick a random verse
            verse_num = random.randrange(1, len(verses) + 1)
            rand_verse = verses[verse_num - 1]

            # Remove verse number
            rand_verse = " ".join(rand_verse.split()[1:])

            verse_num = str(verse_num)

            # Print the random verse to the screen
            print(f"{chosen_book} {chapter}:{verse_num}\n")
            print(f"\"{rand_verse}\"")
            print(f"\n{chapter_url}&id=p{verse_num}#p{verse_num}")
