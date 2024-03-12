import requests
import time
from bs4 import BeautifulSoup as bs


# This class encapsulates quotes as we scrape them
class Quote:
    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags

def main():
    # This is the base url that we are scraping from

    # Before you begin, look through this website and try to understand how elements are navigated
    # Inspect the html, look at each quote. How are the quotes contained? How can you identify elements by class?
    url = "https://quotes.toscrape.com"

    # Sends a GET request to the url, which replies with a response.
    # This response is what r represents
    r = requests.get(url)

    # Beautiful Soup parses the content of the response into a soup object
    # The soup object allows us to search for specific elements in the html response
    soup = bs(r.content, "html.parser")

    quotes = []  
    quote_tags = {}
    quote_authors ={}
    # iterate through each page of quotes
    while True:
        # If you followed in class, this logic was at the bottom
        # This should have been at the top, because our logic did not actually add the first page
        quotes.extend(scrape_quotes(soup,quote_tags,quote_authors))

        # use a sleep delay to ensure you are not hitting the url too quickly
        # hitting a url too quickly risks being flagged as a DDoS attack
        # This can get you blocked
        time.sleep(1)

        # The relative url is scraped from the "next" button
        relative_url = get_next_url(soup)


        # This will ensure that when there is no "next" button, the loop breaks
        if relative_url is None:
            break

        # The relative url is added to the base url to get the next page url
        next_page = url + relative_url

        # a new request is sent to the next_page and the soup is updated with the next page
        # The loop restarts
        r = requests.get(next_page)
        soup = bs(r.content, "html.parser")
    sorted_occurences = sorted(quote_tags.items(), key=lambda x: x[1], reverse=True)
    print(sorted_occurences)
    author_occurances = sorted(quote_authors.items(), key=lambda x: x[1], reverse=True)
    print(author_occurances)
    

    # After we have all of the quotes, we can figure out the longest and shortest
    get_shortest_and_longest(quotes)
    return

def get_shortest_and_longest(quotes):
    '''
        This function prints the longest and shortest quote and the length of each
    '''

    # Start by setting a longest integer to as short as possible (0)
    # And set a shortest integer to longer than the longest quote could possibly be (100,000)
    longest = 0
    shortest = 100000

    # These update when a new longest or shortest is found
    longest_quote = ""
    shortest_quote = ""
    
    for quote in quotes:
        if len(quote.text) > longest:
            longest = len(quote.text)
            longest_quote = quote.text

        if len(quote.text) < shortest:
            shortest = len(quote.text)
            shortest_quote = quote.text
    print("longest quote",longest_quote, longest)
    print("shortest quote",shortest_quote, shortest)
    return 


def get_next_url(soup: bs):
    '''
        Scrapes our soup object for the next url (from the next button)
        Returns the url
    '''
    # find the next url
    list_item = soup.find("li", {"class": "next"})
    if list_item is None:
        return None
    anchor = list_item.find("a")
    url = anchor["href"]

    return url


def scrape_quotes(soup: bs,quote_tags,quote_authors):
    '''
        Gets all of the quotes from the soup object
        Returns a list of quotes as Quote objects
    '''

    quotes = soup.find_all("div", {"class": "quote"})

    quotes_list = []
   
    

    for quote in quotes:
        text = quote.find("span", {"class": "text"}).get_text(strip=True)
        print(text)
        author = quote.find("small", {"class": "author"}).get_text(strip=True)
        print(author)
       
        if author in quote_authors:
            quote_authors[author] +=1
        else:
            quote_authors[author] = 1

        tags = quote.find_all("a", {"class": "tag"})
        tags_text = []
        for tag in tags:
            tags_text.append(tag.get_text(strip=True))
            tag_name = tag.get_text(strip=True)
            if tag_name in quote_tags:
                quote_tags[tag_name] +=1
            else:
                quote_tags[tag_name] = 1
        print(tags_text)
    
        

        quotes_list.append(Quote(text, author, tags_text))
    

    return quotes_list




if __name__ == "__main__":
    main()

