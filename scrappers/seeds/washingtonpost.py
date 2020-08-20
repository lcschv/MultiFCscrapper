from scrappers.Commons import *
from scrappers.ClaimSchema import *
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
import time
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import json

class WashingtonPost(Commons):
    def __init__(self, seed_id, seed_url, drive_path="scrappers\seeds\chromedriver.exe"):
        Commons.__init__(self, drive_path)
        self.destination_folder = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\2\html_claims\\"
        self.seed_id = seed_id
        self.seed_url = seed_url
        self.dict_claims_urls = {}
        self.dict_unique_urls = {}
        self.dict_claims_category = {}
        self.claim_num = 1
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
        self.dict_objects = {}
    def get_share_statements(self, soup, url):
        claim = []
        claim = soup.find_all("div",{"class":"sharethefacts"})
        return claim

    def get_claim_label(self, sharefact , url):
        label = ""
        image = sharefact.find('div',{"class":"sharethefacts-rating"})
        if image is not None:
            url = image.find('img')['src']
            if "pinnochios" in url:
                label =  url[-5]+ " pinnochios"
            else:
                urlretrieve(url, "000001.jpg")
                text = self.get_text_from_image("000001.jpg")
                label = text.replace('\n',' ')
        return label

    def get_text_from_image(self, path):
        image = Image.open(path)  # the second one
        text = pytesseract.image_to_string(image)
        return text

    def get_claim_date_published(self, soup, url):
        claim_date = ""

        div_share = soup.find("div", {"class": "sharethefacts-dateline"})
        if div_share is not None:
            try:
                claim_date = div_share.text.rsplit('–')[1]
            except:
                return claim_date
        return claim_date

    def get_checker(self, soup, url):
        author = ""
        author_info = soup.find("a",{"class":"author-name"})
        if author_info is not None:
            author = author_info.text.strip()
        # author = author_info.find('a').text
        return author

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

    def get_text_image_test(self):
        text = self.get_text_from_image("caption_3469858.jpg")
        print (text)
        # label = text.replace('\n', ' ')

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
        div = soup.find('div',{"class":"topper-headline"})
        if div is not None:
            h1 = div.find('h1')
            if h1 is not None:
                title = h1.text.strip()
        # title = entire_title.rsplit('-',1)[0]
        # label = entire_title.rsplit('-', 1)[1]
        return title

    def get_speaker(self, statement, url):
        speaker = ""
        div_share = statement.find("div",{"class": "sharethefacts-speaker-name"})
        if div_share is not None:
            speaker = div_share.text.strip()
        return speaker

    def get_publish_date(self, soup, claim_url):
        publish_date = ""
        span = soup.find("span",{"class":"author-timestamp"})
        if span is not None:
            publish_date = span.text.strip()
        return publish_date

    def get_claim(self, sharefact, claim_url):
        claim = ""
        statement = sharefact.find("div",{"class":"sharethefacts-statement"})
        if statement is not None:
            claim = statement.text.strip()
        return claim

    def parse_claim_url(self):

        for claim_id, claim_url in self.dict_claims_urls.items():
            # try:
            try:
                self.driver.get(claim_url)
                html = self.driver.page_source.encode("utf-8")
                # html = self._get_full_doc_(claim_url)
            except:
                # self.reopen_washington()
                continue
            soup = BeautifulSoup(html, 'html.parser')
            with open("raw_content/washingtonpost/"+str(claim_id)+".html","w") as f:
                f.write(str(html))

                # self.clean_soup(soup)

            # label = self.dict_claims_category[claim_url]
            # article_title, label = self.get_article_title_and_label(soup, claim_url)
            publish_date = self.get_publish_date(soup, claim_url)
            share_statements = self.get_share_statements(soup, claim_url)
            if len(share_statements) > 0:
                checker = self.get_checker(soup, claim_url)
                article_title = self.get_article_title(soup, claim_url)
                # category = self.dict_claims_category[claim_url]
                i = 1
                for sharefact in share_statements:
                    # article_title = self.get_article_title(soup, claim_url)
                    # label = self.get_claim_label(soup, claim_url)

                    speaker = self.get_speaker(sharefact, claim_url)
                    claim = self.get_claim(sharefact, claim_url)
                    label = self.get_claim_label(sharefact, claim_url)

                    claim_date = self.get_claim_date_published(sharefact, claim_url)

                    claim_object = ClaimSchema()
                    if len(share_statements)>1:
                        claim_object.set_id(str(claim_id)+"_"+str(i))
                        id = str(claim_id)+"_"+str(i)
                    else:
                        claim_object.set_id(str(claim_id))
                        id = claim_id
                    claim_object.set_claim_url(claim_url)
                    claim_object.set_claim(claim)
                    if label != "":
                        claim_object.set_label(label)
                    if article_title != "":
                        claim_object.set_article_title(article_title)
                    # if category != "":
                    #     claim_object.set_categories(category)
                    if claim_date != "":
                        claim_object.set_claim_date(claim_date)
                    if speaker != "":
                        claim_object.set_speaker(speaker)
                    # claim_object.set_reason(reason)
                    if checker != "":
                        claim_object.set_checker(checker)
                    if publish_date != "":
                        claim_object.set_publish_date(publish_date)
                    # claim_object.set_tags(tags)
                    #
                    i+=1
                    self.dict_objects[id] = claim_object
                    claim_object.pretty_print()
            else:
                continue
            # except:
            #     self.reopen_washington()
            #     continue

    def parse_documents(self):
        with open("C:\Lucas\PhD\Datasets\CrawlingLogs\washingtonpost\\urls.txt") as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        for line in content:
            parts = line.split(',',2)
            claim_id = parts[0]
            url = parts[1]
            self.dict_claims_urls[claim_id] = url
        for claim_id, claim_url in self.dict_claims_urls.items():
            # try:
            try:
            #     # self.driver.get(claim_url)
                with open("raw_content/washingtonpost/"+claim_id+".html") as f:
                    html = f.read()
            #     # html = self.driver.page_source.encode("utf-8")
            #     # html = self._get_full_doc_(claim_url)
            except:
                # self.reopen_washington()
                continue
            soup = BeautifulSoup(html, 'html.parser')
            # with open("raw_content/washingtonpost/" + str(claim_id) + ".html", "w") as f:
            #     f.write(str(html))

                # self.clean_soup(soup)

            # label = self.dict_claims_category[claim_url]
            # article_title, label = self.get_article_title_and_label(soup, claim_url)
            # print(soup)
            publish_date = self.get_publish_date(soup, claim_url)
            share_statements = self.get_share_statements(soup, claim_url)
            if len(share_statements) > 0:
                checker = self.get_checker(soup, claim_url)
                article_title = self.get_article_title(soup, claim_url).replace("\\xe2\\x80\\x9c", "").replace("\\xe2\\x80\\x9d", "").replace("\\xe2\\x80\\x99", "'")
                # category = self.dict_claims_category[claim_url]
                i = 1
                for sharefact in share_statements:
                    # article_title = self.get_article_title(soup, claim_url)
                    # label = self.get_claim_label(soup, claim_url)

                    speaker = self.get_speaker(sharefact, claim_url)
                    claim = self.get_claim(sharefact, claim_url).replace("\\xe2\\x80\\x9c", "").replace("\\xe2\\x80\\x9d", "").replace("\\xe2\\x80\\x99", "'")

                    label = self.get_claim_label(sharefact, claim_url)

                    claim_date = self.get_claim_date_published(sharefact, claim_url)

                    claim_object = ClaimSchema()
                    if len(share_statements) > 1:
                        claim_object.set_id(str(claim_id) + "_" + str(i))
                        id = str(claim_id) + "_" + str(i)
                    else:
                        claim_object.set_id(str(claim_id))
                        id = claim_id
                    claim_object.set_claim_url(claim_url)
                    claim_object.set_claim(claim)
                    if label != "":
                        claim_object.set_label(label)
                    if article_title != "":
                        claim_object.set_article_title(article_title)
                    # if category != "":
                    #     claim_object.set_categories(category)
                    if claim_date != "":
                        claim_object.set_claim_date(claim_date)
                    if speaker != "":
                        claim_object.set_speaker(speaker)
                    # claim_object.set_reason(reason)
                    if checker != "":
                        claim_object.set_checker(checker)
                    if publish_date != "":
                        claim_object.set_publish_date(publish_date)
                    # claim_object.set_tags(tags)
                    #
                    i += 1
                    self.dict_objects[id] = claim_object
                    claim_object.pretty_print()
            else:
                continue

    def click_on_load_more(self):
        self.driver.get("https://www.washingtonpost.com/news/fact-checker/")
        time.sleep(5)
        # i=1
        while True:
            # self.driver.implicitly_wait(10)
            try:
                self.driver.find_element_by_class_name('pb-loadmore').click()
                # i+=1
                time.sleep(0.5)
            except:
                break

    def get_list_claims_url(self, soup, base_url):
        for story in soup.find_all("div", {"class": "story-headline"}):
            a = story.find('h3').find('a')
            url_claim = base_url + a['href']
            category = a['href'].split('/')[1]
            if url_claim not in self.dict_unique_urls:
                self.dict_claims_category[url_claim] = category
                self.dict_unique_urls[url_claim] = self.claim_num
                self.dict_claims_urls[self.claim_num] = url_claim
                self.claim_num += 1

    def clean_soup(self, soup):
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]


    def reopen_washington(self):
        from selenium.webdriver.chrome.options import Options
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
        # self.driver = webdriver.Chrome(executable_path="C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
        self.driver.quit()
        self.driver = webdriver.Chrome(executable_path=self.drive_path, chrome_options=opts)
        self.driver.set_page_load_timeout(30)
        self.driver.get("https://www.washingtonpost.com")
        time.sleep(2)
        self.driver.find_element_by_xpath(
            ".//*[contains(text(), 'Browse now')]"
        ).click()
        time.sleep(2)
        self.driver.find_element_by_class_name('agree-ckb').click()
        self.driver.find_element_by_xpath(
            ".//*[contains(text(), 'Continue to site')]"
        ).click()
        time.sleep(2)
        self.driver.get(
            "https://subscribe.washingtonpost.com/loginregistration/index.html#/register/group/default?action=login&rememberme=true")
        time.sleep(2)
        self.driver.find_element_by_id("login").send_keys("ADDYOUREMAIL")
        self.driver.find_element_by_id("password").send_keys("ADDYOURPASSWORD")
        self.driver.find_element_by_id("signinBtnTWP").click()
        time.sleep(90)

        # time.sleep(1)
        # self.driver.find_element_by_class_name('agree-ckb').click()
        # time.sleep(0.5)
        # self.driver.find_element_by_class_name('continue-btn button accept-consent').click()
        # time.sleep(0.5)
        ## The settings below are just to set some configuration if we want to crawl the screenshot of the webpages
        # self.driver.maximize_window()
        # self.driver.get('chrome://settings/')
        # # self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.7);')
        # self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(' + str(self.zoom_out) + ');')
        # self.driver.set_page_load_timeout(120)
    def start(self):

        # self.driver.get("https://subscribe.washingtonpost.com/loginregistration/index.html#/register/group/default?action=login&rememberme=true")
        # self.driver.find_element_by_id("login").send_keys("ADDYOUREMAIL")
        # self.driver.find_element_by_id("password").send_keys("ADDYOURPASSWORD")
        # self.driver.find_element_by_id("signinBtnTWP").click()
        # self.reopen_washington()
        # base_url = "https://www.washingtonpost.com"
        # # from selenium.webdriver.support.ui import WebDriverWait
        # #
        # # #Initialize webpages
        # self.click_on_load_more()
        # webpage_content = self.driver.page_source.encode("utf-8")
        # soup = BeautifulSoup(webpage_content, 'html.parser')
        # self.get_list_claims_url(soup, base_url)
        # for item in self.dict_claims_urls.items():
        #     print(item)
        # # self.dict_claims_urls[1]= "https://www.washingtonpost.com/politics/2018/09/14/obamas-claim-that-trumps-obamacare-moves-have-already-cost-million-people-health-insurance/?utm_term=.4e3d5baff68f"
        # self.parse_claim_url()
        self.print_object_as_tsv("schemas/washingtonpost.txt", self.dict_objects)
        self.summarize_statistics("statistics/washingtonpost.txt", self.dict_objects)
        self.driver.close()



if __name__ == '__main__':
    washingtonpost = WashingtonPost(5, "https://www.washingtonpost.com/news/fact-checker/", "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
    # washingtonpost.parse_documents()
    # washingtonpost.start()
    washingtonpost.get_text_image_test()
