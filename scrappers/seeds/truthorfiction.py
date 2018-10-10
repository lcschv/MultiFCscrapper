from scrappers.Commons import *
from scrappers.ClaimSchema import *
from bs4 import BeautifulSoup
import requests

class TruthOrFiction(Commons):
    def __init__(self, seed_id, seed_url, drive_path="scrappers\seeds\chromedriver.exe"):
        Commons.__init__(self, drive_path)
        self.destination_folder = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\2\html_claims\\"
        self.seed_id = seed_id
        self.seed_url = seed_url
        self.dict_claims_urls = {}
        self.dict_unique_urls = {}
        self.dict_claims_category = {}
        self.claim_num = 1
        self.dict_objects = {}
    def get_claim(self, soup, url, title):
        claim = ""
        div_tag = soup.find_all("div",{"class": "inner-post-entry"})
        for tag in div_tag:
            try:
                claim = tag.find("h2",style=True).text.strip().rsplit('-', 1)[0]
                return claim
            except:
                # attrs = {'style': 'font-size: 0.8em;text-align: center;width: 28%;', 'class': 'half'}
                return title

        return claim

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
            label = ""
        return label

    def get_publish_date(self, soup, url):
        publish_date = ""
        try:
            publish_date = soup.find("div",{"class":"post-box-meta-single"}).find("span").text.strip()
        except:
            return publish_date
        return publish_date

    def get_author(self):
        pass

    def get_claim_date(self):
        pass

    #They dont have tags
    def get_tags(self, soup, url):
        tags = []
        try:
            aTags = soup.find("div",{"class":"post-tags"}).find_all("a")
            for a in aTags:
                tags+=[a.text.strip()]
            return tags
        except:
            return tags



    def get_claim_category(self, soup, url):
        category = ""
        div_tag = soup.find_all("div",{"class":"breadcrumb-nav"})
        for tag in div_tag:
            aTags = tag.find_all("a")
        for a in aTags:
            if "/category/" in a["href"]:
                category = a.text.strip()
        return category

    def get_article_title_and_label(self, soup, url):
        title=""
        label = ""
        try:
            entire_title = soup.find("h1",{"class":"post-title single-post-title"}).text.strip()
            title = entire_title.rsplit('-', 1)[0]
            label = entire_title.rsplit('-', 1)[1]
        except:
            return title, label


        return title, label


    def parse_claim_url(self):
        for claim_id, claim_url in self.dict_claims_urls.items():
            try:
                html = self._get_full_doc_(claim_url)
                with open("raw_content/truthorfiction/" + str(claim_id) + ".html", "w") as f:
                    f.write(str(html))
            except:
                self.reopen_driver()
                continue
            soup = BeautifulSoup(html, 'html.parser')
            # self.clean_soup(soup)
            claim_object = ClaimSchema()
            article_title, label = self.get_article_title_and_label(soup, claim_url)
            claim = self.get_claim(soup, claim_url, article_title)
            if claim != "":
                claim_object.set_claim(claim)
            else:
                continue
            try:
                category = self.dict_claims_category[claim_url]
                claim_object.set_categories(category)
            except:
                category =""

            if article_title != "":
                claim_object.set_article_title(article_title)
                claim_object.set_label(label)
            publish_date = self.get_publish_date(soup, claim_url)
            if publish_date != "":
                claim_object.set_publish_date(publish_date)


            # author, publish_date =self.article_info(soup, claim_url)
            # category = self.get_claim_category(soup, claim_url)
            tags = self.get_tags(soup, claim_url)
            if len(tags)>0:
                claim_object.set_tags(tags)

            # # print (claim_id, claim, label, article_title, author, publish_date)

            #
            claim_object.set_id(claim_id)
            claim_object.set_claim_url(claim_url)

            self.dict_objects[claim_id] = claim_object
            # claim_object.set_checker(author)
            # claim_object.set_reason(author)

            claim_object.pretty_print()

    def get_list_claims_url(self, soup, category):
        ulTags = soup.findAll("ul", {"class": "penci-grid"})
        for tag in ulTags:
            articleTag = tag.find_all("article",{"class":"item"})
            for article in articleTag:
                a = article.find("a")
                url_claim = a.get('href')
                if url_claim not in self.dict_unique_urls:
                    self.dict_claims_category[url_claim] = category
                    self.dict_unique_urls[url_claim] = self.claim_num
                    self.dict_claims_urls[self.claim_num] = url_claim
                    self.claim_num+=1

    def clean_soup(self, soup):
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]

    def start(self):
        categories = ["9-11-attack","animals", "appeals","business", "celebrities","christmas", "clinton",
                      "clintons", "computers", "crime-police", "education", "environment", "food", "government",
                      "guns","health-medical", "holidays", "household", "humorous", "natural-disasters/hurricane",
                      "immigration","insects", "inspirational", "international", "internet","natural-disasters/katrina",
                      "mass-shootings", "medical", "military", "miscellaneous", "missing", "money-financial", "natural-disasters",
                      "obama", "pleas", "politics", "prayers", "promises", "redfaces", "religious", "russia", "social-media",
                      "space-aviation", "sports", "terrorism", "trump", "politics/trump-politics", "natural-disasters/tsunami",
                      "virus", "war", "warnings"]

        # categories = ["animals"]
        for category in categories:
            #Enter the first time to crawl
            i=1
            url = self.seed_url + category + "/page/" + str(i)
            request = requests.get(url)
            #Check whether there exists next webpages

            while request.status_code == 200:
                html = self._get_full_doc_(url)
                soup = BeautifulSoup(html, 'html.parser')
                self.clean_soup(soup)
                self.get_list_claims_url(soup, category)
                i += 1
                url = self.seed_url + category + "/page/" + str(i)
                request = requests.get(url)

        self.parse_claim_url()
        self.print_object_as_tsv("schemas/truthorfiction.txt", self.dict_objects)
        self.summarize_statistics("statistics/truthorfiction.txt", self.dict_objects)
                # filepath = self.destination_folder + str(i)+".txt"
                # self.write_webpage_content_tofile(html, filepath)
        self.driver.close()


if __name__ == '__main__':
    truthorfiction = TruthOrFiction(2, "https://www.truthorfiction.com/category/", "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
    truthorfiction.start()