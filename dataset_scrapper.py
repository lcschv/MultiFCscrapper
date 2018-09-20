# the full text that appears when the claim is clicked
# the above full text contains hyperlinks. We have the full text that appears when each of those hyperlinks in clicked
# URL of the webpage where each claim originally appeared
# name of the person making the claim
# date when the claim was made
# date when the label was published by Politifact
from scrappers.Crawling import Crawling

def main():

    crawling = Crawling("C:\Lucas\PhD\CredibilityDataset\list_websites")
    crawling.start()


if __name__ == '__main__':
    main()