# the full text that appears when the claim is clicked
# the above full text contains hyperlinks. We have the full text that appears when each of those hyperlinks in clicked
# URL of the webpage where each claim originally appeared
# name of the person making the claim
# date when the claim was made
# date when the label was published by Politifact
from scrappers.Scrapper import Scrappers

def main():

    scrapper = Scrappers()
    scrapper.start()


if __name__ == '__main__':
    main()