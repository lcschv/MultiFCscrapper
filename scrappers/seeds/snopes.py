from scrappers.Commons import *
import os
from bs4 import BeautifulSoup
import re
from bs4.element import NavigableString
import string

class Snopes(Commons):
    def __init__(self, seed_id, seed_url, drive_path="scrappers\seeds\chromedriver.exe"):
        Commons.__init__(self, drive_path)
        self.destination_folder = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\1\html_claims\\"
        self.seed_id = seed_id
        self.seed_url = seed_url
        self.dict_claims_urls = {}
        self.dict_unique_urls = {}
        self.claim_num = 1

    def get_claim(self, soup, url):
        pTag = ""
        div_tag = soup.find_all("div",{"class": "article-text-inner"})
        try:
            for tag in div_tag:
                pTag = soup.find("p").text.strip()
        except Exception as e:
            print ("Could not get claim for url: ",url)
            pTag = "wrong claim"
        return pTag

    def get_claim_label(self, soup, url):
        label = ""
        div_tag = soup.find_all("div",{"class":"rating-wrapper"})
        try:
            for tag in div_tag:
                aTags = tag.find_all("a")
                for a_tag in aTags:
                    label = a_tag.find("span").text.strip()
        except Exception as e:
            # self.cont_errors += 1
            print(str(e), "wrong label at url: ", url)
            label = "wrong label"
        return label


    def article_info(self, soup, url):
        author, publish_date = "", ""
        publish_date = soup.find("span",{"class":"date-wrapper"}).text.strip()
        pTags = soup.findAll("p",{"class":"author-box"})
        for tag in pTags:
            author = tag.find("a",{"class":"author-link"}).text.strip()
        return author, publish_date

    def get_claim_date(self):
        pass

    def get_article_title(self, soup, url):
        title=""
        try:
            title = soup.find("h1",{"class":"article-title"}).text.strip()
        except Exception as e:
            print ("Was not able to get the article-title for this url: ", url)
            title = "wrong article title"
        return title


    def parse_claim_url(self):
        for claim_id, claim_url in self.dict_claims_urls.items():
            html = self._get_full_doc_(claim_url)
            soup = BeautifulSoup(html, 'html.parser')
            self.clean_soup(soup)
            article_title = self.get_article_title(soup, claim_url)
            claim = self.get_claim(soup, claim_url)
            label = self.get_claim_label(soup, claim_url)
            author, publish_date =self.article_info(soup,claim_url)
            # print (claim_id, claim, label, article_title, author, publish_date)
            print (claim_id, label, claim)

    def get_list_claims_url(self, soup):
        div_tag = soup.find_all("div", {"class": "list-wrapper"})
        for tag in div_tag:
            articleTags = tag.find_all("article")
            for article_tag in articleTags:
                aTags = article_tag.find_all("a")
                for a_tag in aTags:
                    url_claim = str(a_tag.get('href'))
                    if url_claim not in self.dict_unique_urls:
                        self.dict_unique_urls[url_claim] = self.claim_num
                        self.dict_claims_urls[self.claim_num] = url_claim
                        # print("ClaimID:", self.claim_num, "Url:", url_claim)
                        # self.parse_claim_url(url_claim)
                        self.claim_num+=1
    def clean_soup(self, soup):
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]

    def start(self):
        for i in range(0,10):
            url = self.seed_url+str(i)
            html = self._get_full_doc_(url)
            soup = BeautifulSoup(html, 'html.parser')
            self.clean_soup(soup)
            self.get_list_claims_url(soup)
        self.parse_claim_url()

            # filepath = self.destination_folder + str(i)+".txt"
            # self.write_webpage_content_tofile(html, filepath)
        self.driver.close()


if __name__ == '__main__':
    snopes = Snopes(1, "https://www.snopes.com/fact-check/page/", "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
    snopes.start()
# def analyze_forbes_page():
#
#     pass
#
#
# def check_next_page(url):
#     try to open url + number
#     url = "https://www.snopes.com/fact-check/page/"
#
#
#

# def get_all_claims_from_page():
#     pass
#
# #This is the main function of the Snopes Scrapper, the one that must be added to the function_mappings dictionary
# def snopes(self, url):
#     destination_folder = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\1\html_claims"
#     for i in range(1, 1021):
#         print (i)
#         get_all_claims_from_page()

    # content = self._get_full_doc_(url)
    # filepath = destination_folder+ i +".txt"
    # self.write_webpage_content_tofile(content, destination_folder)


#         analyze_forbes_page()
# #
#     scrap = new Scrapper("https://www.snopes.com/fact-check/page/")
#     scrap._get_full_doc_(url+1)