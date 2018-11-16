from scrappers.Commons import *
from scrappers.ClaimSchema import *
from bs4 import BeautifulSoup

class Snopes(Commons):
    def __init__(self, seed_id, seed_url, drive_path="scrappers\seeds\chromedriver.exe"):
        Commons.__init__(self, drive_path)
        self.destination_folder = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\1\html_claims\\"
        self.seed_id = seed_id
        self.seed_url = seed_url
        self.dict_claims_urls = {}
        self.dict_unique_urls = {}
        self.claim_num = 1
        self.dict_objects = {}

    def get_claim(self, soup, url):
        claim = ""
        div_tag = soup.find_all("div",{"class": "article-text-inner"})
        try:
            for tag in div_tag:
                claim = soup.find("p").text.strip()
        except Exception as e:
            print ("Could not get claim for url: ",url)
            # claim = ""
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


    def article_info(self, soup, url):
        author, publish_date = "", ""
        publish_date = soup.find("span",{"class":"date-wrapper"}).text.strip()
        pTags = soup.findAll("p",{"class":"author-box"})
        for tag in pTags:
            author = tag.find("a",{"class":"author-link"}).text.strip()
        return author, publish_date


    def get_claim_date(self):
        pass

    #They dont have tags
    def get_tags(self):
        pass

    def get_claim_category(self, soup, url):
        category = None
        div_tag = soup.find_all("div",{"class":"breadcrumb-nav"})
        for tag in div_tag:
            aTags = tag.find_all("a")
        for a in aTags:
            if "/category/" in a["href"]:
                category = a.text.strip()
        return category

    def get_article_title(self, soup, url):
        title=None
        try:
            title = soup.find("h1",{"class":"article-title"}).text.strip()
        except Exception as e:
            print ("Was not able to get the article-title for this url: ", url)
            title = "wrong article title"
        return title


    def parse_claim_url(self):

        i=1
        for claim_id, claim_url in self.dict_claims_urls.items():
            try:

                html = self._get_full_doc_(claim_url)
                with open("raw_content/snopes/"+str(claim_id)+".html","w") as f:
                    f.write(str(html))
                soup = BeautifulSoup(html, 'html.parser')
                self.clean_soup(soup)
                article_title = self.get_article_title(soup, claim_url)
                claim = self.get_claim(soup, claim_url)
                label = self.get_claim_label(soup, claim_url)
                if claim != "" and label != "":
                    author, publish_date =self.article_info(soup, claim_url)
                    category = self.get_claim_category(soup, claim_url)
                    # print (claim_id, claim, label, article_title, author, publish_date)
                    claim_object = ClaimSchema()

                    claim_object.set_id(claim_id)
                    claim_object.set_claim_url(claim_url)
                    claim_object.set_claim(claim)
                    claim_object.set_label(label)
                    claim_object.set_article_title(article_title)
                    claim_object.set_categories(category)
                    claim_object.set_checker(author)
                    claim_object.set_publish_date(publish_date)
                    # claim_object.set_reason(author)
                    # claim_object.set_tags(tags)
                    self.dict_objects[i] = claim_object
                    i+=1
                    claim_object.pretty_print()
            except:
                self.reopen_driver()
                continue

    def get_list_claims_url(self, soup):
        div_tag = soup.find_all("div", {"class": "list-group"})
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
        for i in range(39,40):
            try:
                url = self.seed_url+str(i)
                html = self._get_full_doc_(url)
            except:
                continue
            soup = BeautifulSoup(html, 'html.parser')
            self.clean_soup(soup)
            self.get_list_claims_url(soup)
        self.parse_claim_url()
        self.print_object_as_tsv("schemas/snopes.txt", self.dict_objects)
        self.summarize_statistics("statistics/snopes.txt", self.dict_objects)
            # filepath = self.destination_folder + str(i)+".txt"
            # self.write_webpage_content_tofile(html, filepath)
        self.driver.close()

if __name__ == '__main__':
    snopes = Snopes(1, "https://www.snopes.com/fact-check/page/", "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
    snopes.start()