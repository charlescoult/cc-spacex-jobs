from requests_html import HTMLSession
from bs4 import BeautifulSoup
from pprint import pprint
import re
import csv
import sys


# Gets job details from the greenhouse link
def getDetails( href ):
    session = HTMLSession()

    r = session.get( href )
    if r.status_code != 200:
        print( 'Error' )
        return ''

    soup = BeautifulSoup( r.html.html, 'html.parser' )
    content = soup.find( id = "content" )
    if content:
        return content.prettify()
    else:
        return ''

async def writeRow( writer, row ):
    pass

def main():
    URL = "https://www.spacex.com/careers/index.html?department="

    session = HTMLSession()

    # Retrieve page
    r = session.get( URL )
    if ( r.status_code != 200 ):
        print( 'Error getting jobs' )
        return -1

    # Use requests_html (that uses puppeteer) to run the Javascript and render the HTML
    # Be sure to wait for the Javascript to finish loading the resources
    r.html.render( sleep = 1  )

    # Use BeatifulSoup's HTML parser (even though requests has already parsed it and
    # BeatutifulSoup isn't really necessary, I wanted to learn it)
    soup = BeautifulSoup( r.html.html, 'html.parser' )

    with open( 'data.csv', 'w' ) as f:
        writer = csv.writer( f )

        # Write header
        writer.writerow( [
            "Job Title",
            "Link",
            "Location",
            "Employment Type",
            "Job ID",
            "Details",
        ] )

        # Pull and write all rows
        for row in soup.find_all( 'tr' ):
            # Pull each column from the row
            cols = row.find_all( 'td' )
            # Filters out header row
            if ( len( cols ) == 3 ):
                href = cols[ 0 ].find( 'a' ).attrs[ 'href' ]
                title = cols[ 0 ].text
                location = cols[ 1 ].text
                empl_type = cols[ 2 ].text
                jid = re.search( "(?<=[?&]gh_jid=)" + "([^&]+).*$", href ).group( 0 )
                details = getDetails( href )

                writer.writerow( [
                    title,
                    href,
                    location,
                    empl_type,
                    jid,
                    details,
                ] )

    print( 'done' )


if __name__ == '__main__':
    sys.exit( main() )
