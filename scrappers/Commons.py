from selenium import webdriver

class Commons:
    def __init__(self):
        pass
    def _get_full_doc_(self, url):
        webpage_content = ""
        self.driver.get(url)
        try:
            webpage_content = self.driver.page_source.encode("utf-8")
        except Exception as e:
            # self.cont_errors += 1
            print(str(e), url)
            self.reopen_driver()
            webpage_content = ""
            return webpage_content
        return webpage_content


    # Reopen driver in case it crashes or anything else.
    def reopen_driver(self):
        self.driver.quit()
        # self.driver = webdriver.Chrome(executable_path="C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
        self.driver = webdriver.Chrome(executable_path="scrappers\chromedriver.exe")
        self.driver.set_page_load_timeout(20)
        ## The settings below are just to set some configuration if we want to crawl the screenshot of the webpages
        # self.driver.maximize_window()
        # self.driver.get('chrome://settings/')
        # # self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.7);')
        # self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(' + str(self.zoom_out) + ');')
        # self.driver.set_page_load_timeout(120)

    def initialize_driver(self):
        self.driver = webdriver.Chrome(executable_path="scrappers\chromedriver.exe")
        self.driver.set_page_load_timeout(20)


    # Function that writes the crawled html to file..
    def write_webpage_content_tofile(self, content, path):
        # file_out = open(self.destiny_rawdata_folder+"\\"+str(doc_id)+".html","w")
        file_out = open(path ,"w")
        # file_out.write(str(doc_id)+"<--->"+str(url)+"<--->"+str(content))
        file_out.write(str(content))
        file_out.close()