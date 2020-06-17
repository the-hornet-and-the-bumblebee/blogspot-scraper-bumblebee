"""
This script scrapes a Blogspot blog by iterating back in its history.
Usage:
    1. Set url variable to the Blogspot URL you want as point of departure.
    2. Press CTRL-C when you want to stop it.
Note:  IP-number may be temporarily banned from the Blogger service if over-used.
"""

import requests
import io
import re
import string
from bs4 import BeautifulSoup
import dateparser
from datetime import datetime

# URL to scrap
url = 'http://myblogtoscrap.blogspot.com/'

headers = {"User-Agent" : 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0'}

def FormattingString(MyStringToFormat):
    exclude = set(string.punctuation)
    return ''.join(ch for ch in MyStringToFormat if ch not in exclude)

while True:
    page = requests.get(url, headers=headers)
    html_soup = BeautifulSoup(page.text, 'html.parser')
    AllPosts = html_soup.find_all('div', class_="date-outer") # Retrieving all posts on the current page

    # Turns the requested output into a file like objet
    file_like_obj = io.StringIO(page.text)
    lines = file_like_obj.read()
    # Retrieves each post's unique ID-number
    ListPostID = re.findall(r'post-body-(.*)\' itemprop', lines)

    PostIndex = 0

    for EachPost in AllPosts:
        # Retrieving and formatting the publication date
        NotFormattedPostDatee = EachPost.h2.span.text
        FormattedPostDate = datetime.strftime(dateparser.parse(NotFormattedPostDatee), '%Y%m%d')

        # Title cleaning
        FormattedPostTitle = FormattingString(EachPost.h3.a.text.replace('\n', ''))

        # Retrieving blog post content
        PostContent = html_soup.find(id="post-body-" + ListPostID[PostIndex])
        # File creation
        with open(str(FormattedPostDate) + " " + FormattedPostTitle + ".html", "w", encoding="utf-8") as outputfile:
            outputfile.write(str(PostContent))

        PostIndex += 1

    # Search for "Older Items"
    matchObj = re.findall(r'blog-pager-older-link\' href=\'(.*)\' id', lines)
    # Retrieve the 1st occurrence found
    next_url = matchObj[0]
    print("####### Next URL to be scrapped: " + next_url)
    url = next_url # Initialization of the next URL to be scrapped