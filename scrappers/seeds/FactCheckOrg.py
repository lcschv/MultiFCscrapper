from scrappers.Commons import *
from scrappers.ClaimSchema import *
from bs4 import BeautifulSoup
import requests

class FactCheckOrg(Commons):
    def __init__(self, seed_id, seed_url, drive_path="scrappers\seeds\chromedriver.exe"):
        Commons.__init__(self, drive_path)
        self.destination_folder = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\3\html_claims\\"
        self.seed_id = seed_id
        self.seed_url = seed_url
        self.dict_claims_urls = {}
        self.dict_unique_urls = {}
        self.dict_claims_category = {}
        self.claim_num = 1
        self.dict_objects = {}

    def get_claim(self, soup, url):
        claim = ""
        div_share = soup.find("div",itemprop="claimReviewed")
        if div_share is not None:
            claim = div_share.text.strip()
        else:
            div_share = soup.find("div",{"class":"sharethefacts-statement"})
            if div_share is not None:
                claim = div_share.text.strip()
        return claim

    def get_claim_label(self, soup, url):
        label = ""
        div_share = soup.find("div", itemprop="alternateName")
        if div_share is not None:
            label = div_share.text.strip()
        else:
            div_share = soup.find("div", {"class":"sharethefacts-rating"})
            if div_share is not None:
                img = div_share.find("img")
                if img is not None:
                    label = img['src'].rsplit('/', 1)[1].replace('.png','')
        return label

    def get_publish_date(self, soup, url):
        publish_date = soup.find("p",{"class":"posted-on"}).find("time").text.strip()
        return publish_date

    def get_author(self, soup, url):
        author = soup.find("p",{"class":"byline"}).find("a").text.strip()
        return author

    def get_speaker(self, soup, url):
        speaker = ""
        div_share = soup.find("div", itemprop="name")
        if div_share is not None:
            speaker = div_share.text.strip()
        else:
            div_share = soup.find("div", {"class": "sharethefacts-speaker-name"})
            if div_share is not None:
                speaker = div_share.text.strip()

        return speaker

    def get_tags(self, soup, url):
        tags = []
        liTags = soup.find_all("li",{"class":"post_tag"})
        for li in liTags:
            if li is not None:
                tags_a = li.find("a").text.strip()
                tags+=[tags_a]
        liIssue = soup.find_all("li",{"class":"issue"})
        for li in liIssue:
            if li is not None:
                tags_a = li.find("a").text.strip()
                tags+=[tags_a]
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

    def get_article_title(self, soup, url):
        title = ""
        entire_title = soup.find("h1",{"class":"entry-title"}).text.strip()
        return entire_title


    def get_claim_date_published(self, soup, url):
        claim_date = ""
        div_share = soup.find("div", itemprop="datePublished")
        div_share = soup.find("div", itemprop="datePublished")
        if div_share is not None:
            claim_date = div_share.text.strip()
        else:
            div_share = soup.find("div", {"class": "sharethefacts-dateline"})
            if div_share is not None:
                claim_date = div_share.text.rsplit('/')
        return claim_date


    def parse_claim_url(self):
        for claim_id, claim_url in self.dict_claims_urls.items():
            # try:
            html = self._get_full_doc_(claim_url)
            with open("raw_content/factcheckorg/"+str(claim_id)+".html","w") as f:
                f.write(str(html))
            soup = BeautifulSoup(html, 'html.parser')
            self.clean_soup(soup)
            claim = self.get_claim(soup, claim_url)
            if claim == "":
                continue
            claim_object = ClaimSchema()
            category = self.dict_claims_category[claim_url]
            article_title = self.get_article_title(soup, claim_url)
            publish_date = self.get_publish_date(soup,claim_url)
            author = self.get_author(soup, claim_url)
            if author != "":
                claim_object.set_checker(author)
            tags = self.get_tags(soup, claim_url)
            if len(tags) > 0:
                claim_object.set_tags(tags)
            label = self.get_claim_label(soup,claim_url)
            if label != "":
                claim_object.set_label(label)
            speaker = self.get_speaker(soup, claim_url)
            if speaker != "":
                claim_object.set_speaker(speaker)
            claim_date = self.get_claim_date_published(soup, claim_url)
            if claim_date != "":
                claim_object.set_claim_date(claim_date)
            if article_title != "":
                claim_object.set_article_title(article_title)
            if publish_date != "":
                claim_object.set_publish_date(publish_date)


            claim_object.set_id(claim_id)
            claim_object.set_claim_url(claim_url)
            claim_object.set_claim(claim)
            claim_object.set_categories(category)
            self.dict_objects[claim_id] = claim_object
            # except:
            #     self.reopen_driver()
            #     continue

            claim_object.pretty_print()

    def get_list_claims_url(self, soup, category):
        articleTags = soup.findAll("article")
        for article in articleTags:
            a = article.find("a")
            url_claim = a.get('href')
            # print ("Url_Claim:", url_claim)
            if url_claim not in self.dict_unique_urls:
                self.dict_claims_category[url_claim] = category
                self.dict_unique_urls[url_claim] = self.claim_num
                self.dict_claims_urls[self.claim_num] = url_claim
                self.claim_num+=1

    def clean_soup(self, soup):
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]

    def start(self):
        """
        Some comments:
        We are only collecting websites that contain the "sharethefact" card because we they are the only one that contains the label
        For multiple claim in the same url, we duplicate the information and create a new claim, label, and speaker.
        Worst rating 1, best rating 11
        In the TAGS we added the tags that were in ISSUE as well.
        Same label might occur twice differently (this happens because sometimes I can extract directly, other times I extract from the imagesrc.
        """

        categories = ["the-factcheck-wire","featured-posts", "scicheck","askfactcheck", "fake-news"]
        # categories = ["the-factcheck-wire"]

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
        self.print_object_as_tsv("schemas/factcheckorg.txt", self.dict_objects)
        self.summarize_statistics("statistics/factcheckorg.txt", self.dict_objects)

                # filepath = self.destination_folder + str(i)+".txt"
                # self.write_webpage_content_tofile(html, filepath)
        self.driver.close()


if __name__ == '__main__':
    factcheckorg = FactCheckOrg(3, "https://www.factcheck.org/", "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
    factcheckorg.start()