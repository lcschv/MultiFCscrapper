from scrappers.Commons import *
from scrappers.ClaimSchema import *
from bs4 import BeautifulSoup

class Fullfact(Commons):
    def __init__(self, seed_id, seed_url, drive_path="scrappers\seeds\chromedriver.exe"):
        Commons.__init__(self, drive_path)
        self.destination_folder = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\1\html_claims\\"
        self.seed_id = seed_id
        self.seed_url = seed_url
        self.dict_claims_urls = {}
        self.dict_unique_urls = {}
        self.dict_claims_category = {}
        self.claim_num = 1

    def get_claim(self, soup, url):
        claim, rating = [], []
        div_tag = soup.find("div",{"class": "box-panel"})
        if div_tag is not None:
            div_tags_claims = div_tag.find_all("div",{"class":"col-xs-12 col-sm-6 col-left"})
            for claim_ in div_tags_claims:
                claim += [claim_.find("p").text.strip()]
            div_tags_rating = div_tag.find_all("div", {"class": "col-xs-12 col-sm-6 col-right"})
            for rating_ in div_tags_rating:
                rating += [rating_.find("p").text.strip()]
        return claim, rating

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


    def get_author(self, soup, url):
        author = ""
        p = soup.find("p",{"class":"post-content-footer-author"})
        if p is not None:
            author = p.text.strip().replace("By ","")
        return author

    def get_publish_date(self, soup, url):
        publish_date = ""
        p = soup.find("p",{"class":"hidden-xs hidden-sm date updated"})
        if p is not None:
            publish_date = p.text.strip().replace('Published: ','')
        return publish_date

    def get_claim_date(self):
        pass

    #They dont have tags
    def get_tags(self):
        pass

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
        title=""
        try:
            title = soup.find("h1").text.strip()
        except Exception as e:
            print ("Was not able to get the article-title for this url: ", url)
            title = "wrong article title"
        return title

    def parse_claim_url(self):
        i = 1
        for claim_id, claim_url in self.dict_claims_urls.items():
            html = self._get_full_doc_(claim_url)
            soup = BeautifulSoup(html, 'html.parser')
            self.clean_soup(soup)
            claims, ratings = self.get_claim(soup, claim_url)
            category = self.dict_claims_category[claim_url]
            article_title = self.get_article_title(soup, claim_url)
            publish_date = self.get_publish_date(soup, claim_url)
            author = self.get_author(soup, claim_url)
            if len(claims)>=1 and len(ratings) >=1:
                for claim, label in zip(claims, ratings):
                    claim_object = ClaimSchema()

                    claim_object.set_id(i)
                    claim_object.set_claim_url(claim_url)
                    claim_object.set_claim(claim)
                    claim_object.set_label(label)
                    claim_object.set_article_title(article_title)
                    claim_object.set_categories(category)
                    claim_object.set_checker(author)
                    claim_object.set_publish_date(publish_date)
                    claim_object.set_reason(author)
                    # claim_object.set_tags(tags)
                    claim_object.set_reason(label)
                    i+=1
                    claim_object.pretty_print()

    def get_list_claims_url(self, soup):
        domain = "https://fullfact.org"
        div_tag = soup.find_all("h2", {"class": "postlist-item-heading"})
        for tag in div_tag:
            articleTags = tag.find("a")
            url = str(articleTags.get('href'))
            category = url.split('/')[1]
            url_claim = domain + url
            if url_claim not in self.dict_unique_urls:
                self.dict_unique_urls[url_claim] = self.claim_num
                self.dict_claims_urls[self.claim_num] = url_claim
                self.dict_claims_category[url_claim] = category
                # print("ClaimID:", self.claim_num, "Url:", url_claim)
                # self.parse_claim_url(url_claim)
                self.claim_num+=1

    def clean_soup(self, soup):
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]

    def start(self):
        """"IN THIS CASE THE LABEL IS THE SAME AS THE REASON
            NOT ABLE TO CRAWL SPEAKER AND TAGS
        """
        for i in range(1,20):
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
    fullfact = Fullfact(6, "https://fullfact.org/search/?q=1&page=", "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
    fullfact.start()
