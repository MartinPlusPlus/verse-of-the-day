#!/usr/bin/python3

"""
A simple program to get a verse of scripture from churchofjesuschrist.org

Copyright 2021 Martin Eldredge
Licensed under the MIT License which is included in this project
"""

import random
import requests
import csv
from bs4 import BeautifulSoup

url = "https://www.churchofjesuschrist.org/study/scriptures/bofm?lang=eng"
url_base = "https://www.churchofjesuschrist.org/study/scriptures/bofm/"

# Get html from church website
res = requests.get(url)
html = res.content
soup = BeautifulSoup(html, "html.parser")

book_list = []
exclude = [
            "Contents", "Introduction and Witnesses  ",
            "Book of Mormon Pronunciation Guide",
            "Reference Guide to the Book of Mormon"
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
with open("bom.csv") as books:
    reader = csv.reader(books, delimiter=',')
    for row in reader:
        if row[0] == chosen_book:
            chapter = random.randrange(1, int(row[2]) + 1)
            chapter_url = url_base + row[1] + "/" + row[2] + "?lang=eng"
            res = requests.get(chapter_url)
            html = res.content
            soup = BeautifulSoup(html, "html.parser")
            divs = soup.find_all("div", {"class": "body-block"})
            verses = []
            for div in divs:
                for verse in div:
                    verses.append(str(verse.get_text()))
            verse_num = random.randrange(0, len(verses))
            rand_verse = verses[verse_num]
            print(chosen_book + " " + str(chapter) + ":" + str(verse_num + 1) + "\n")
            print(rand_verse)
            print("\n" + chapter_url)
