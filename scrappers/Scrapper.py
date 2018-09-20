from selenium import webdriver

class Scrappers(object):
    def __init__(self, path):
        self.path = path
        self.dict_seeds = {}

        #After creating the scrapper, add in the dictionary below Key = SeedID and Value = Function_name
        self.function_mappings = {"1":self.snopes}

    #Make sure to import your new function here
    from scrappers.seeds.snopes import snopes


    #Function responsible to read the seeds that we are going to crawl
    def read_all_seeds_(self):
        with open(self.path) as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        for line in content:
            #It should have the format SEED_ID URL
            parts = line.split(' ', 2)
            seed_id = parts[0]
            seed_url = parts[1]
            if seed_id not in self.dict_seeds:
                self.dict_seeds[seed_id] = seed_url


    def _get_full_doc_(self, url):
        webpage_content = ""
        self.driver.get(url)
        try:
            webpage_content = self.driver.page_source.encode("utf-8")
        except Exception as e:
            self.cont_errors += 1
            print(str(e), self.cont_errors, self.seed_id, url)
            self.reopen_driver()
            webpage_content = ""
            return webpage_content
        return webpage_content


    #Reopen driver in case it crashes or anything else.
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

    #Function that writes the crawled html to file..
    def write_webpage_content_tofile(self, content, path):
        # file_out = open(self.destiny_rawdata_folder+"\\"+str(doc_id)+".html","w")
        file_out = open(path,"w")
        # file_out.write(str(doc_id)+"<--->"+str(url)+"<--->"+str(content))
        file_out.write(str(content))
        file_out.close()

    def start(self):
        #Reading all seeds from file ..
        self.read_all_seeds_()

        #Initializing Driver (chrome) to crawl the data and setting timeout
        # self.driver = webdriver.Chrome(
        #     executable_path="C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
        self.driver = webdriver.Chrome(
            executable_path="scrappers\chromedriver.exe")
        self.driver.set_page_load_timeout(20)

        #For each seed written in the file, call its respective scrapper
        for seed_id, seed_url in self.dict_seeds.items():
            self.cont_errors = 0
            self.seed_id = seed_id
            scrapper = self.function_mappings[seed_id]
            scrapper(seed_url)