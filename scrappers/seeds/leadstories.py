from scrappers.Commons import *
from scrappers.ClaimSchema import *
from bs4 import BeautifulSoup

class LeadStories(Commons):
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
        self.dict_labels = {}

    def article_info(self, soup, url):
        author, publish_date = "", ""
        categories = []
        dict_authors = {}
        authors = []
        infobox = soup.find("div",{"class":"pfcontentmid"}).find("div",{"class":"boxmid"})
        for p in infobox.find_all("p"):
            strong = p.find("strong")
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
        try:
            author = soup.find("ul",{"class":"e_data_list"}).find("li").find("a")
            if author is not None:
                return author.text.strip()
        except:
            return author
    def get_publish_date(self, soup, url):
        publish_date = None
        try:
            publish_date = soup.find("ul",{"class":"e_data_list"}).find_all("li")[1].text.strip().split("(")[1].replace(')',"")
            return publish_date
        except:
            return publish_date
    def get_label(self, soup, url):
        verdict = ""
        h2s = soup.find_all("h2")
        for h2 in soup.findAll():
            h2_text = h2.text
            nextNode = h2
            if h2.name == "h2":
                if h2_text is not None and "Verdict" in h2_text or "verdict" in h2_text:
                    i=1
                    while i == 1:
                            nextNode = nextNode.nextSibling
                            try:
                                tag_name = nextNode.name
                            except AttributeError:
                                tag_name = ""
                                continue
                            if tag_name == "p" and nextNode.string is not None:
                                # print(nextNode.string)
                                verdict += nextNode.string+ " "
                            if tag_name == "div":
                                break
        return verdict

    def parse_claim_url(self):

        i=1
        for claim_id, claim_url in self.dict_claims_urls.items():
            # try:
            try:
                html = self._get_full_doc_(claim_url)
                with open("raw_content/leadstories/" + str(claim_id) + ".html", "w") as f:
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
            label = self.dict_labels[claim_id]
            if claim_id in self.dict_claims:
                claim_object.set_claim(self.dict_claims[claim_id])
            claim_object.set_label(label)
            author = self.get_author(soup, claim_url)
            claim_object.set_checker(author)
            claim_object.set_publish_date(self.get_publish_date(soup,claim_url))

            # speaker = self.dict_speaker[claim_id]
            # claim_object.set_speaker(speaker)

            # # if claim != "" and label != "":
            # author, publish_date, category = self.article_info(soup, claim_url)

            # claim_object.set_categories(self.get_categories(soup,claim_url))
            # claim_object.set_checker("Brett M. Christensen")
            #     #

            # claim_object.set_publish_date(self.dict_publish_date[claim_id])
            #     # claim_object.set_tags(tags)
            self.dict_objects[i] = claim_object
            i+=1
            claim_object.pretty_print()
            # except:
            #     self.reopen_driver()
            #     continue

    def get_list_claims_url(self):
        HoaxAlert = {155:"https://leadstories.com/cgi-bin/mt/mt-search.cgi?search=&IncludeBlogs=1&blog_id=1&category=31&archive_type=Category&template_id=108&limit=10&page="}
        # HoaxAlert = {1:"https://leadstories.com/cgi-bin/mt/mt-search.cgi?search=&IncludeBlogs=1&blog_id=1&category=31&archive_type=Category&template_id=108&limit=10&page="}
        # Facebook = {31:"https://www.hoax-slayer.net/category/scams/facebook-scams/page/"}
        # FakeNews = {10:"https://www.hoax-slayer.net/category/fake-news/page/"}
        # Truth = {5:"https://www.hoax-slayer.net/category/true/page/"}
        # Misleading = {5:"https://www.hoax-slayer.net/category/misleading/page/"}

        dict_seeds = {"Hoax":HoaxAlert}
        # dict_seeds = {"Bogus Warning":BogusWarning}
        for label, seeds in dict_seeds.items():
            for size, url_base in seeds.items():
                for i in range(1,size+1):
                    try:
                        html = self._get_full_doc_(url_base+str(i))
                        soup = BeautifulSoup(html,'html.parser')
                    except:
                        self.reopen_driver()
                        continue
                    section = soup.find("section",{"class":"mod_collection"})
                    lis = section.find_all('article',{"class":"mod_category_article"})
                    for li in lis:
                        url_claim = li.find('h1').find("a").get('href')
                        article_title = li.find('h1').find("a").text.strip().replace("’","").replace("“","").replace("‘","")
                        descrp = li.find("div",{"class":"e_descr"}).text.strip()
                        parts = descrp.split('?',2)
                        claim = ""
                        if len(parts)>1:
                            claim = parts[0] + "?"

                        if url_claim not in self.dict_unique_urls:
                            self.dict_title[self.claim_num] = article_title
                            if claim != "":
                                self.dict_claims[self.claim_num]= claim
                            # self.dict_publish_date[self.claim_num] = publish_date
                            self.dict_labels[self.claim_num] = label
                            self.dict_unique_urls[url_claim] = self.claim_num
                            self.dict_claims_urls[self.claim_num] = url_claim
                            self.claim_num += 1
    def clean_soup(self, soup):
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]

    def start(self):

        self.get_list_claims_url()
        # for i in range(1,11):
        # # for i in range(0,1026):
        #     url=base_url+str(i)
        # #     url = self.seed_url+str(i)
        #     try:
        #         html = self._get_full_doc_(url)
        #     except:
        #         self.reopen_driver()
        #         continue
        #     soup = BeautifulSoup(html, 'html.parser')
        # # self.clean_soup(soup)
        #     self.get_list_claims_url(soup, url)
        self.parse_claim_url()
        self.print_object_as_tsv("schemas/leadstories.txt", self.dict_objects)
        self.summarize_statistics("statistics/leadstories.txt", self.dict_objects)
        # #     # filepath = self.destination_folder + str(i)+".txt"
        # #     # self.write_webpage_content_tofile(html, filepath)
        self.driver.close()

if __name__ == '__main__':
    leadstories = LeadStories(1, "https://www.snopes.com/fact-check/page/", "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
    leadstories.start()