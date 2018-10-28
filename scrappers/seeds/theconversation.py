from scrappers.Commons import *
from scrappers.ClaimSchema import *
from bs4 import BeautifulSoup


class TheConversation(Commons):
    def __init__(self, seed_id, seed_url, drive_path="scrappers\seeds\chromedriver.exe"):
        Commons.__init__(self, drive_path)
        self.destination_folder = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\1\html_claims\\"
        self.seed_id = seed_id
        self.seed_url = seed_url
        self.dict_claims_urls = {}
        self.dict_unique_urls = {}
        self.claim_num = 1
        self.dict_objects = {}

    def article_info(self, soup, url):
        author, publish_date = "", ""
        categories = []
        dict_authors = {}
        authors = []
        infobox = soup.find("div", {"class": "pfcontentmid"}).find("div", {"class": "boxmid"})
        for p in infobox.find_all("p"):
            strong = p.find("strong")
            # print("SAUEUSAHEHUASHUESA:", strong)
            if strong is not None:
                option = strong.text
                if option == "Subjects:":
                    tags_a = p.find_all("a")
                    for a in tags_a:
                        categories += [a.text.strip()]
                if option == "Written by:":
                    tags_a = p.find_all("a")
                    for a in tags_a:
                        if a.text.strip() not in dict_authors:
                            dict_authors[a.text.strip()] = 0
                if option == "Published:":
                    publish_date = p.text.replace("Published:", "").strip()

        authors = ", ".join(dict_authors.keys())

        return authors, publish_date, categories

    def get_claim_and_speaker(self,soup,url):
        claim = ""
        div = soup.find("div",{"class":"grid-ten large-grid-nine grid-last content-body content entry-content instapaper_body"})
        claim = div.find("blockquote").find("p").text.strip()
        speaker = div.find("strong").text.strip()
        return claim, speaker

    def get_verdict(self,soup,url):
        achei = 0
        div = soup.find("div", {
            "class": "grid-ten large-grid-nine grid-last content-body content entry-content instapaper_body"})
        for tag in div.find_all():
            if achei == 1:
                return tag.text.strip()
            if tag.text == "Verdict":
                achei = 1

    def get_tags(self, soup, url):
        tags = []
        div = soup.find("div",{"class":"grid-ten grid-prepend-two large-grid-nine grid-last content-topics topic-list"})
        if div is not None:
            for a in div.find_all("a"):
                tags += [a.text.strip()]
        if len(tags)== 0:
            tags = None
        return tags

    def get_category(self,soup,url):
        category =None
        nav = soup.find("nav",{"id":"primary-navigation"})
        if nav is not None:
            category = nav.find("a",{"class":"current"}).get("title").strip()
        return category
    def parse_claim_url(self):

        i = 1
        for claim_id, claim_url in self.dict_claims_urls.items():
            try:
                html = self._get_full_doc_(claim_url)
                soup = BeautifulSoup(html, 'html.parser')
                self.clean_soup(soup)
                # article_title = self.get_article_title(soup, claim_url)
                claim_object = ClaimSchema()
                claim,speaker = self.get_claim_and_speaker(soup,claim_url)
                claim_object.set_claim(claim)
                claim_object.set_claim_url(claim_url)
                claim_object.set_id(claim_id)
                claim_object.set_article_title(self.dict_article_title[claim_url])
                tags = self.get_tags(soup,claim_url)
                category = self.get_category(soup,claim_url)
                # title = soup.find("h1")
                # if title is not None:
                #     article_title = title.text.strip()
                #     claim_object.set_article_title(article_title)
                # label = self.dict_labels[claim_id]
                verdict = self.get_verdict(soup, claim_url)
                claim_object.set_label(verdict)
                #
                claim_object.set_categories(category)
                claim_object.set_speaker(speaker)
                #
                # # # if claim != "" and label != "":
                # author, publish_date, category = self.article_info(soup, claim_url)
                #
                # claim_object.set_categories(category)
                claim_object.set_checker(self.dict_checker[claim_url])
                # #     #
                claim_object.set_publish_date(self.dict_publish_date[claim_url])
                # # claim_object.set_reason(author)
                claim_object.set_tags(tags)
                # self.dict_objects[i] = claim_object
                # i += 1
                claim_object.pretty_print()
            except:
                self.reopen_driver()
                continue

    def get_list_claims_url(self, soup, url):
        self.dict_claims = {}
        self.dict_labels = {}
        div_tag = soup.find("section",{"id": "articles"}).find_all("article")
        self.dict_speaker = {}
        self.dict_publish_date = {}
        self.dict_checker = {}
        self.dict_article_title ={}
        url_base = "https://theconversation.com"
        for tag in div_tag:
            url_claim = url_base + tag.find('a', {"class": "article-link"}).get('href')
            print(url_claim)
            # for article_tag in articleTags:
            #     aTags = article_tag.find_all("a")
            #     for a_tag in aTags:
            #         url_claim = str(a_tag.get('href'))
            if url_claim not in self.dict_unique_urls:
                self.dict_publish_date[url_claim] = tag.find("time",{"pubdate":"pubdate"}).text.strip()
                self.dict_checker[url_claim] = tag.find("p",{"class":"byline"}).find("span").find("a").text.strip()
                self.dict_article_title[url_claim] = tag.find("h2").find("a").text.strip()
                # self.dict_speaker[self.claim_num] = tag.find('div', {"class": "mugshot"}).find("img").get('alt').strip()
                # self.dict_claims[self.claim_num] = tag.find('h2').text.strip()
                # self.dict_labels[self.claim_num] = tag.find('div', {"class": "meter"}).find("img").get('alt').strip()
                self.dict_unique_urls[url_claim] = self.claim_num
                self.dict_claims_urls[self.claim_num] = url_claim
            self.claim_num += 1

    def clean_soup(self, soup):
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]

    def start(self):
        seeds = ['https://theconversation.com/uk/topics/fact-check-uk-15076']
        # 'https://theconversation.com/uk/topics/fact-check-uk-15076?page=2',
        # 'https://theconversation.com/uk/topics/fact-check-uk-15076?page=3',
        # 'https://theconversation.com/uk/topics/fact-check-uk-15076?page=4']

        for url in seeds:
            # for i in range(0,1026):
            #     url = self.seed_url+str(i)
            html = self._get_full_doc_(url)
            soup = BeautifulSoup(html, 'html.parser')
            # self.clean_soup(soup)
            self.get_list_claims_url(soup, url)
        self.parse_claim_url()
        # self.print_object_as_tsv("schemas/snopes.txt", self.dict_objects)
        # self.summarize_statistics("statistics/snopes.txt", self.dict_objects)
        #     # filepath = self.destination_folder + str(i)+".txt"
        #     # self.write_webpage_content_tofile(html, filepath)
        self.driver.close()


if __name__ == '__main__':
    theconversation = TheConversation(1, "https://www.snopes.com/fact-check/page/",
                      "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
    theconversation.start()