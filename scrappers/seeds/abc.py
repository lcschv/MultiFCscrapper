from scrappers.Commons import *
from scrappers.ClaimSchema import *
from bs4 import BeautifulSoup
import requests

class Abc(Commons):
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

    def get_claim(self, soup, url):
        claim = ""
        div_Tag = soup.find("div",{"class":"inline-content wysiwyg right"})
        if div_Tag is not None:
            ul = div_Tag.find("ul")
            if ul is not None:
                claim = ul.find("li").text.strip()
            else:
                p = soup.find("p", {"class": "first"})
                if p is not None:
                    claim = p.text.strip()
            # print ("Veredict:", ul.find("li").text.strip())
        else:
            p = soup.find("p", {"class":"first"})
            if p is not None:
                claim = p.text.strip()
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
            label = "wrong label"
        return label

    def get_publish_date(self, soup, url):
        # publish_date = soup.find("div",{"class":"post-box-meta-single"}).find("span").text.strip()
        publish_date = soup.find("span",{"class":"print"}).text.strip()
        return publish_date

    def get_author(self):
        pass

    def get_claim_date(self):
        pass

    def get_reason(self, soup, url):
        reason = []
        div_Tag = soup.find("div", {"class": "inline-content wysiwyg right"})
        if div_Tag is not None:
            ul = div_Tag.find("ul")
            if ul is not None:
                reason += [ul.find("li").text.strip()]
        else:
            div_Tag = soup.find("div",{"class":"article section"}).find_all("h2")
            for tag in div_Tag:
                if tag.text.strip() == "The verdict":
                    nextNode = tag.next_sibling
                    while nextNode.name != "h2":
                        if nextNode.name == "p":
                            reason += [nextNode.string]
                            nextNode = nextNode.next_sibling
                        else:
                            nextNode = nextNode.next_sibling
                    # veredict = tag.next_sibling.string
                    # print (veredict)
            # p = soup.find("p", {"class": "first"})
            # if p is not None:
            #     reason = p.text.strip()
        return ' '.join(filter(None, reason))

    #They dont have tags
    def get_tags(self, soup, url):
        tags = []
        try:
            aTags = soup.find("p",{"class":"topics"}).find_all("a")
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

    def get_article_title(self, soup, url):
        title=""
        title= soup.find('div',{"class":"article section"}).find('h1').text.strip()
        # title = entire_title.rsplit('-',1)[0]
        # label = entire_title.rsplit('-', 1)[1]
        return title


    def parse_claim_url(self):
        for claim_id, claim_url in self.dict_claims_urls.items():
            try:
                html = self._get_full_doc_(claim_url)
                with open("raw_content/abc/"+str(claim_id)+".html","w") as f:
                    f.write(str(html))
            except:
                self.reopen_driver()
                continue
            soup = BeautifulSoup(html, 'html.parser')
            self.clean_soup(soup)
            ###THIS IS ASSUMING THAT THE LABEL IS DIVIDED INTO 3, however it's not just that.
            label = self.dict_claims_category[claim_url]
            # article_title, label = self.get_article_title_and_label(soup, claim_url)
            publish_date = self.get_publish_date(soup,claim_url)
            claim = self.get_claim(soup, claim_url)
            article_title = self.get_article_title(soup, claim_url)
            # label = self.get_claim_label(soup, claim_url)
            # author, publish_date =self.article_info(soup, claim_url)
            # category = self.get_claim_category(soup, claim_url)
            tags = self.get_tags(soup, claim_url)
            category = self.get_tags(soup, claim_url)
            reason = self.get_reason(soup, claim_url)
            # # print (claim_id, claim, label, article_title, author, publish_date)
            claim_object = ClaimSchema()

            claim_object.set_id(claim_id)
            claim_object.set_claim_url(claim_url)
            if claim != "":
                claim_object.set_claim(claim)
            else:
                continue
            if label != "":
                claim_object.set_label(label)
            if article_title != "":
                claim_object.set_article_title(article_title)
            if category != "":
                claim_object.set_categories(category)
            if reason != "":
                claim_object.set_reason(reason)
            # # claim_object.set_checker(author)
            if publish_date != "":
                claim_object.set_publish_date(publish_date)
            # # claim_object.set_reason(author)
            if tags != "":
                claim_object.set_tags(tags)
            self.dict_objects[claim_id] = claim_object
            #
            claim_object.pretty_print()

    def get_list_claims_url(self, soup, category):
        ulTags = soup.findAll("ul", {"class": "article-index"})
        for tag in ulTags:
            liTags = tag.find_all("li")
            for li in liTags:
                a = li.find("a")
                url_claim = a.get('href')
                url_claim = "http://www.abc.net.au"+url_claim
                if url_claim not in self.dict_unique_urls:
                    self.dict_claims_category[url_claim] = category
                    self.dict_unique_urls[url_claim] = self.claim_num
                    self.dict_claims_urls[self.claim_num] = url_claim
                    self.claim_num+=1

    def clean_soup(self, soup):
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]

    def start(self):
        # self.dict_labels = {"unsubstantiated":1, "exaggerates":1,"exaggerated":1, "out of context":1, "misleading":1,
        #                     "incorrect":1, "wrong":1, "half-baked":1, "ill-informed":1, "baseless":1, "doesn't check out":1,
        #                     "doesn't stack up":1, "myth":1, "wishful thinking":1, "overstated":1, "rewriting history":1,
        #                     "fanciful":1, "over the top":1, "nonsense":1, "untenable":1,"checks out":1,
        #                     "correct":1, "fair call":1, "faithful account":1, "good call":1, "jumping the gun":1,
        #                     "more to the story":1, "simplistic":1, "in the ballpark":1, "fair":1, "spin":1, "not the full story":1,
        #                     "flimsy":1, "not clear cut":1, "on shaky ground":1, "wide of the mark":1, "cherrypicking":1,
        #                     "overreach":1
        #                     }
        ###THIS IS ASSUMING THAT THE LABEL IS DIVIDED INTO 3, however it's not just that. We are not using the labels above.
        ### We are also assuming that the categories and tags are the same in this case.
        ##THERE IS NO INFORMATION ABOUT WHO CHECKS
        ## There is no direct answer to who spoke the claim.
        ## SHOULD DOUBLE CHECK IF THE TITLE OF THE ARTICLE IS THE CLAIM, OR THE CLAIM IS IN THE <h2> THE CLAIM

        categories = {"in-the-red":3, "in-the-green":3, "in-between":5}
        # categories = {"in-the-red":1, "in-the-green":1, "in-between":1}
        # categories = {"in-between":1}
        for category, max in categories.items():
            #Enter the first time to crawl
            i=1
            url = self.seed_url + category + "/?page=" + str(i)
            request = requests.get(url)
            #Check whether there exists next webpages

            while request.status_code == 200 and i <= max:
                html = self._get_full_doc_(url)
                soup = BeautifulSoup(html, 'html.parser')
                self.clean_soup(soup)
                self.get_list_claims_url(soup, category)
                i += 1
                url = self.seed_url + category + "/?page=" + str(i)
                request = requests.get(url)
        # for key, url in self.dict_unique_urls.items():
        #     print (key, url)
        self.parse_claim_url()
        self.print_object_as_tsv("schemas/abc.txt", self.dict_objects)
        self.summarize_statistics("statistics/abc.txt", self.dict_objects)

                # filepath = self.destination_folder + str(i)+".txt"
                # self.write_webpage_content_tofile(html, filepath)
        self.driver.close()

if __name__ == '__main__':
    abc = Abc(4, "http://www.abc.net.au/news/factcheck/", "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
    abc.start()