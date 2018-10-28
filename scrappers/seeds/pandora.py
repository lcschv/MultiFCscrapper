from scrappers.Commons import *
from scrappers.ClaimSchema import *
from bs4 import BeautifulSoup

class Pandora(Commons):
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



    def parse_claim_url(self):

        i=1
        for claim_id, claim_url in self.dict_claims_urls.items():
            try:
                html = self._get_full_doc_(claim_url)
                soup = BeautifulSoup(html, 'html.parser')
                self.clean_soup(soup)
                    # article_title = self.get_article_title(soup, claim_url)
                claim_object = ClaimSchema()
                claim = self.dict_claims[claim_id]
                claim_object.set_claim(claim)
                claim_object.set_claim_url(claim_url)
                claim_object.set_id(claim_id)
                title = soup.find("h1")
                if title is not None:
                    article_title = title.text.strip()
                    claim_object.set_article_title(article_title)
                label = self.dict_labels[claim_id]
                claim_object.set_label(label)
    
                speaker = self.dict_speaker[claim_id]
                claim_object.set_speaker(speaker)

                # # if claim != "" and label != "":
                author, publish_date, category = self.article_info(soup, claim_url)

                claim_object.set_categories(category)
                claim_object.set_checker(author)
                #     #
                claim_object.set_publish_date(publish_date)
                    # claim_object.set_reason(author)
                #     # claim_object.set_tags(tags)
                self.dict_objects[i] = claim_object
                i+=1
                claim_object.pretty_print()
            except:
                self.reopen_driver()
                continue

    def get_list_claims_url(self, soup, url):
        url = url.replace('index.html','')
        self.dict_claims = {}
        self.dict_labels = {}
        div_tag = soup.find_all("div", {"class": "scoretableContainer"})
        self.dict_speaker = {}
        for tag in div_tag:
            url_claim = url+tag.find('p',{"class":"quote"}).find('a').get('href')
            # print (url_claim)
            # for article_tag in articleTags:
            #     aTags = article_tag.find_all("a")
            #     for a_tag in aTags:
            #         url_claim = str(a_tag.get('href'))
            if url_claim not in self.dict_unique_urls:
                self.dict_speaker[self.claim_num] = tag.find('div',{"class":"mugshot"}).find("img").get('alt').strip()
                self.dict_claims[self.claim_num] = tag.find('h2').text.strip()
                self.dict_labels[self.claim_num] = tag.find('div',{"class":"meter"}).find("img").get('alt').strip()
                self.dict_unique_urls[url_claim] = self.claim_num
                self.dict_claims_urls[self.claim_num] = url_claim
            self.claim_num+=1


    def clean_soup(self, soup):
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]

    def start(self):
        seeds = [
            'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/index.html']
        # seeds = [
        #     'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/index.html',
        #     'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/index4658.html?page=2',
        #     'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/index9ba9.html?page=3',
        #     'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/indexfdb0.html?page=4',
        #     'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/indexaf4d.html?page=5',
        #     'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/indexc575.html?page=6',
        #     'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/index235c.html?page=7',
        #     'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/indexfdfa.html?page=8',
        #     'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/index0b08.html?page=9',
        #     'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/index1448.html?page=10',
        #     'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/index1c8b.html?page=11',
        #     'http://pandora.nla.gov.au/pan/140601/20131209-1141/www.politifact.com.au/truth-o-meter/statements/indexce37.html?page=12',
        #     'http://pandora.nla.gov.au/pan/140601/20130908-0354/www.politifact.com.au/truth-o-meter/statements/index.html',
        #     'http://pandora.nla.gov.au/pan/140601/20130908-0354/www.politifact.com.au/truth-o-meter/statements/index4658.html?page=2',
        #     'http://pandora.nla.gov.au/pan/140601/20130908-0354/www.politifact.com.au/truth-o-meter/statements/index9ba9.html?page=3',
        #     'http://pandora.nla.gov.au/pan/140601/20130908-0354/www.politifact.com.au/truth-o-meter/statements/indexfdb0.html?page=4',
        #     'http://pandora.nla.gov.au/pan/140601/20130908-0354/www.politifact.com.au/truth-o-meter/statements/indexaf4d.html?page=5',
        #     'http://pandora.nla.gov.au/pan/140601/20130908-0354/www.politifact.com.au/truth-o-meter/statements/indexc575.html?page=6',
        #     'http://pandora.nla.gov.au/pan/140601/20130908-0354/www.politifact.com.au/truth-o-meter/statements/index235c.html?page=7',
        #     'http://pandora.nla.gov.au/pan/140601/20130908-0354/www.politifact.com.au/truth-o-meter/statements/indexfdfa.html?page=8',
        #     'http://pandora.nla.gov.au/pan/140601/20130908-0354/www.politifact.com.au/truth-o-meter/statements/index0b08.html?page=9',
        #     'http://pandora.nla.gov.au/pan/140601/20130908-0354/www.politifact.com.au/truth-o-meter/statements/index1448.html?page=10',
        #     'http://pandora.nla.gov.au/pan/140601/20130521-0808/www.politifact.com.au/index.html']
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
    pandora = Pandora(1, "https://www.snopes.com/fact-check/page/", "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
    pandora.start()