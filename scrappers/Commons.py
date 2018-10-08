from selenium import webdriver
import inspect, os

import io
class Commons:
    def __init__(self, drive_path="scrappers\seeds\chromedriver.exe"):
        self.drive_path = drive_path
        self.driver = webdriver.Chrome(executable_path=self.drive_path)
        self.driver.set_page_load_timeout(20)

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
    def reopen_driver(self, ):
        self.driver.quit()
        # self.driver = webdriver.Chrome(executable_path="C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
        self.driver = webdriver.Chrome(executable_path=self.drive_path)
        self.driver.set_page_load_timeout(20)
        ## The settings below are just to set some configuration if we want to crawl the screenshot of the webpages
        # self.driver.maximize_window()
        # self.driver.get('chrome://settings/')
        # # self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.7);')
        # self.driver.execute_script('chrome.settingsPrivate.setDefaultZoom(' + str(self.zoom_out) + ');')
        # self.driver.set_page_load_timeout(120)

    def initialize_driver(self):
        self.driver = webdriver.Chrome(executable_path=self.drive_path)
        self.driver.set_page_load_timeout(20)

    def print_object_as_tsv(self, file_name, dict_objects):
        header = '  '.join("%s"% item[0] for item in vars(dict_objects[1]).items())
        with io.open(file_name,"w", encoding="utf8") as f:
            f.write(header+"\n")
            for id, object in dict_objects.items():
                attrs = vars(object)
                f.write('   '.join("%s"% item[1] for item in attrs.items())+"\n")

    def summarize_statistics(self, file_out, dict_objects):
        dict_summary = {}
        keys = vars(dict_objects[1])
        for key in keys:
            dict_summary[key] = {"collected":0,"missed":0}
        for id, object in dict_objects.items():
            attrs = vars(object)
            for key, value in attrs.items():
                if value is None:
                    dict_summary[key]["missed"] +=1
                else:
                    dict_summary[key]["collected"] += 1
        with open(file_out,"w") as f:
            f.write("Information"+" "+'   '.join("%s" % item[0] for item in dict_summary.items()) + "\n")
            f.write("Total" + "   " + '   '.join("%s" % str(item[1]["missed"]+ item[1]["collected"]) for item in dict_summary.items())+"\n")
            f.write("Collected"+"   "+'   '.join("%s" % item[1]["collected"] for item in dict_summary.items())+"\n")
            f.write("Missed"+"   "+'   '.join("%s" % item[1]["missed"] for item in dict_summary.items()))


            # print('\t'.join("%s" % item[1] for item in attrs.items()))

            # f.write('   '.join("%s" % item[1] for item in attrs.items()) + "\n")

            # Function that writes the crawled html to file..
    def write_webpage_content_tofile(self, content, path):
        # file_out = open(self.destiny_rawdata_folder+"\\"+str(doc_id)+".html","w")
        file_out = open(path ,"w")
        # file_out.write(str(doc_id)+"<--->"+str(url)+"<--->"+str(content))
        file_out.write(str(content))
        file_out.close()