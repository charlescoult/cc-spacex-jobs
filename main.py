from requests_html import HTMLSession
from bs4 import BeautifulSoup
from pprint import pprint
import csv

URL = "https://www.spacex.com/careers/index.html?department="

session = HTMLSession()

# Retrieve page
r = session.get( URL )

# Use requests_html (that uses puppeteer) to run the Javascript and render the HTML
# Be sure to wait for the Javascript to finish loading the resources
r.html.render( sleep = 2  )

# Use BeatifulSoup's HTML parser (even though requests has already parsed it and
# BeatutifulSoup isn't really necessary, I wanted to learn it)
soup = BeautifulSoup( r.html.html, 'html.parser' )

# intermediate data list to store each job
# CSV could be written in parellel with pulling the rows
# making the data list unnecessary, but I'm lazy and I don't need to worry
# about running out of memory right now
data = []

# Pull all rows
for row in soup.find_all( 'tr' ):
    # Pull each column from the row
    cols = row.find_all( 'td' )
    # Filters out header row
    if ( len( cols ) == 3 ):
        href = cols[ 0 ].find( 'a' ).attrs[ 'href' ]
        title = cols[ 0 ].text
        location = cols[ 1 ].text
        empl_type = cols[ 2 ].text
        data.append( [
            title,
            href,
            location,
            empl_type,
        ] )

with open( 'data.csv', 'w' ) as f:
    writer = csv.writer( f )

    # Write header
    writer.writerow( [
        "Job Title",
        "Link",
        "Location",
        "Employment Type",
    ] )

    # write each row's data
    for row in data:
        writer.writerow( row )

pprint( 'done' )
