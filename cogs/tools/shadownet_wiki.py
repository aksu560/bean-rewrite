import urllib
from pyquery import PyQuery


def GetWikiCharacters():
    charpages = {}
    # Setting up variables for the addresses to be crawled
    address = "https://shadownet.run"
    # next page links dont give the domain in them
    addressmod = "/index.php?title=Category:Player_Characters"

    # while loop because we have an unknown amount of pages on mediawiki
    while True:
        # Load the HTML from destination
        fp = urllib.request.urlopen(str(address + addressmod))
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        pq = PyQuery(mystr)

        # Find all divs
        divs = (pq("div"))

        for div in divs:
            # filter out all that dont have the correct class
            if pq(div).has_class("mw-category-group"):
                # find all character links
                charlist = pq(div)("ul")("li")("a")

                # add all the link titles and hrefs to a dictionary
                for char in charlist:
                    charpages[char.attrib['title']] = char.attrib['href']

        # find all links that have the content "next page"
        linklist = pq("a:Contains('next page')")

        # if the list of links is empty, we are on the last page, and can break
        if linklist.length == 0:
            break
        # otherwise change the addressmod variable to the modifier in the next page link
        else:
            addressmod = linklist[0].attrib['href']

    return charpages