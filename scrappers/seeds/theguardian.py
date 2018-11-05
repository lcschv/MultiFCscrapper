from scrappers.Commons import *
from scrappers.ClaimSchema import *
from bs4 import BeautifulSoup

class TheGuardian(Commons):
    def __init__(self, seed_id, seed_url, drive_path="scrappers\seeds\chromedriver.exe"):
        Commons.__init__(self, drive_path)
        self.destination_folder = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\1\html_claims\\"
        self.seed_id = seed_id
        self.seed_url = seed_url
        self.dict_claims_urls = {}
        self.dict_unique_urls = {}
        self.claim_num = 1
        self.dict_objects = {}
        self.dict_title = {}
        self.dict_claims = {}
        self.dict_publish_date = {}

    def article_info(self, soup, url):
        author, publish_date = "", ""
        categories = []
        dict_authors = {}
        authors = []
        infobox = soup.find("div",{"class":"pfcontentmid"}).find("div",{"class":"boxmid"})
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
                    publish_date = p.text.replace("Published:","").strip()

        authors = ", ".join(dict_authors.keys())

        return authors, publish_date, categories
    def get_categories(self,soup,url):
        category = []
        categories = soup.find_all("span",{"class":"label__link-wrapper"})
        for cat in categories:
            cate= cat.text.strip()
            if cate != "Reality check":
                category += [cate]
        if len(category) == 0:
            return None
        else:
            return category
    def get_author(self, soup, url):
        author = None
        author = soup.find("span",{"itemprop":"name"})
        if author is not None:
            return author.text.strip()
    def get_label(self, soup, url):
        verdict = None
        h2s = soup.find_all("h2")
        for h2 in soup.findAll():
            h2_text = h2.text
            nextNode = h2
            if h2.name == "h2":
                if h2_text is not None and "Verdict" in h2_text or "verdict" in h2_text:
                    i=1
                    verdict = ""
                    while i == 1:
                            nextNode = nextNode.nextSibling
                            try:
                                tag_name = nextNode.name
                            except AttributeError:
                                tag_name = ""
                                continue
                            if tag_name == "p" and nextNode.string is not None:
                                # print(nextNode.string)
                                verdict += nextNode.string.strip()+ " "
                            if tag_name == "div":
                                break
        if verdict is not None and len(verdict) > 0:
            return verdict
        else:
            return None

    def parse_claim_url(self):

        i=1
        for claim_id, claim_url in self.dict_claims_urls.items():
            # try:
            try:
                html = self._get_full_doc_(claim_url)
                with open("raw_content/theguardian/" + str(claim_id) + ".html", "w") as f:
                    f.write(str(html))
            except:
                self.reopen_driver()
                continue
            # html = self._get_full_doc_(claim_url)
            soup = BeautifulSoup(html, 'html.parser')
            self.clean_soup(soup)
                # article_title = self.get_article_title(soup, claim_url)
            # try:
            claim_object = ClaimSchema()
            # claim = self.dict_claims[claim_id]
            # claim_object.set_claim(claim)
            claim_object.set_claim_url(claim_url)
            claim_object.set_id(claim_id)
            title = self.dict_title[claim_id]
            claim_object.set_article_title(title)
            label = self.get_label(soup,claim_url)
            claim_object.set_label(label)

            # speaker = self.dict_speaker[claim_id]
            # claim_object.set_speaker(speaker)

            # # if claim != "" and label != "":
            # author, publish_date, category = self.article_info(soup, claim_url)

            claim_object.set_categories(self.get_categories(soup,claim_url))
            claim_object.set_checker(self.get_author(soup,claim_url))
            #     #
            claim_object.set_publish_date(self.dict_publish_date[claim_id])
                # claim_object.set_reason(author)
            #     # claim_object.set_tags(tags)
            self.dict_objects[i] = claim_object
            i+=1
            claim_object.pretty_print()
            # except:
            #     self.reopen_driver()
            #     continue

    def get_list_claims_url(self, soup, url):
        # url = url.replace('index.html','')
        base = "http://pandora.nla.gov.au//pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/"
        div_tag = soup.find_all("section", {"class": "fc-container"})
        print(len(div_tag))
        for tag in div_tag:
            url_claim = tag.find('a',{"data-link-name":"article"}).get('href')
            title = tag.find('a',{"data-link-name":"article"}).text.strip()
            publishdate = tag.find('a').text.strip()
        #     # print (url_claim)
        #     # for article_tag in articleTags:
        #     #     aTags = article_tag.find_all("a")
        #     #     for a_tag in aTags:
        #     #         url_claim = str(a_tag.get('href'))
            if url_claim not in self.dict_unique_urls:
                self.dict_title[self.claim_num] = title
                self.dict_publish_date[self.claim_num] = publishdate
                self.dict_unique_urls[url_claim] = self.claim_num
                self.dict_claims_urls[self.claim_num] = url_claim
            self.claim_num+=1


    def clean_soup(self, soup):
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]

    def start(self):

        base_url = "https://www.theguardian.com/news/reality-check?page="
        for i in range(1,11):
        # for i in range(0,1026):
            url=base_url+str(i)
        #     url = self.seed_url+str(i)
            try:
                html = self._get_full_doc_(url)
            except:
                self.reopen_driver()
                continue
            soup = BeautifulSoup(html, 'html.parser')
        # self.clean_soup(soup)
            self.get_list_claims_url(soup, url)
        self.parse_claim_url()
        self.print_object_as_tsv("schemas/theguardian.txt", self.dict_objects)
        self.summarize_statistics("statistics/theguardian.txt", self.dict_objects)
        #     # filepath = self.destination_folder + str(i)+".txt"
        #     # self.write_webpage_content_tofile(html, filepath)
        self.driver.close()

if __name__ == '__main__':
    theguardian = TheGuardian(1, "https://www.snopes.com/fact-check/page/", "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
    theguardian.start()