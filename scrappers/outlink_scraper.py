import urllib.request
import threading
from selenium import webdriver
import urllib.request
import urllib.error
from scrappers.Commons import *
import socket
import httplib2
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import urllib.request
#Overriding class urlopener to fake user agent.

#Defining global variables.
dict_claim = {}
dict_url = {}
dict_exeptions = {}
cont = 1
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"

class FixFancyURLOpener(urllib.request.FancyURLopener):

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        if errcode == 403:
            raise ValueError("403")
        return super(FixFancyURLOpener, self).http_error_default(
            url, fp, errcode, errmsg, headers
        )
#Class to create the threads
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, urls_list, seed):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.seed = seed

        #Chunk of the dict_url that this thread will deal with
        self.dict_url = urls_list

        #create one of the scrapper for each thread
        self.scrapper = Scrapper()

    def run(self):
        self.scrapper.web_scrapper(self.dict_url,self.name, self.seed)
        # print ("Exiting " + self.name)

class Scrapper(object):
    def __init__(self):

        #Select where you want to save the raw html and webpages screenshots
        self.destiny_rawdata_folder = "seeds\\raw_content_outlinks\\"
        # self.destiny_screenshots = "C:\\Lucas\\PhD\\Datasets\\CF_assessments_screenshots"
        # self.zoom_out = zoom_out

    def web_scrapper(self, urls_list, thread_name="", seed=""):
        self.seed = seed
        opener = AppURLopener()

        # print (urls_list)
        count=0
        for  url, _ in urls_list:
            # doc_id = document[0]
            # url = document[1]

            try:
                url = url.rstrip()
                # url = 'https://www.google.com/search?q=python'
                if url.endswith('.pdf') or "twitter.com" in url:
                    if self.seed not in dict_exeptions:
                        dict_exeptions[self.seed] = {url: "This is a .pdf document, not HTML."}
                    continue
                fp = urllib.request.urlopen(url, timeout=5)
                content_type = fp.headers.get('content-type')
                if 'application/pdf' in content_type:
                    if self.seed not in dict_exeptions:
                        dict_exeptions[self.seed] = {url: "This is a .pdf document, not HTML."}
                    continue
                mybytes = fp.read()

                mystr = mybytes
                # content = ""
                content = mystr

                self.write_rawdata_tofile(url, content)
                # print (response.read())
            except Exception as e:
                if self.seed not in dict_exeptions:
                    dict_exeptions[self.seed] = {url:str(e)}
                # self.reopen_driver()
                continue

    def write_rawdata_tofile(self, url, content):
        for claim_id in dict_url[url]:
            if url == "https://www.qlrc.qld.gov.au/__data/assets/pdf_file/0004/576166/qlrc-report-76-2018-final.pdf":
                print ("Vai toma no cu..")
            check_dir_exists_and_create(self.destiny_rawdata_folder+"\\"+self.seed+"\\"+str(claim_id))
            file_id = dict_claim[claim_id][url]
            file_out = open(self.destiny_rawdata_folder+"\\"+self.seed+"\\"+str(claim_id)+"\\"+str(file_id)+".html","w")
            file_out.write(str(content))
            file_out.close()

    def get_list_schemas(self, schemas_path):
        onlyfiles = [os.path.join(schemas_path, f) for f in os.listdir(schemas_path)]
        return onlyfiles

def get_outlinks_files_schema(schemas_path):
    onlyfiles = [os.path.join(schemas_path, f) for f in os.listdir(schemas_path)]
    return onlyfiles

def get_dict_url(file):
    i=0
    dict_just_url = {}
    dict_claim = {}
    dict_url = {}
    with open(file, "r", encoding="utf8") as f:
        content = f.readlines()
    content = [x.rstrip() for x in content]
    for line in content:
        claim_id = line.split("\t")[0]
        url = line.split("\t")[1]
        if claim_id not in dict_claim:
            i=1
            dict_claim[claim_id] = {}
        if url not in dict_claim[claim_id]:
            i+=1
            dict_claim[claim_id][url] = i

        if url not in dict_url:
            dict_url[url] = {}
            dict_just_url[url] = 1
        if claim_id not in dict_url[url]:
            dict_url[url][claim_id] = 0
    return dict_claim, dict_url, dict_just_url


def check_dir_exists_and_create(path):
    if not os.path.isdir(path):
        os.mkdir(path)

import time


if __name__ == '__main__':
    outlinks_files_schema = get_outlinks_files_schema("seeds\outlinks")
    for file in outlinks_files_schema:
        start_time = time.time()
        seed = file.rsplit("\\")[-1].replace(".txt","")
        dict_claim, dict_url, dict_just_url = get_dict_url(file)
        check_dir_exists_and_create("seeds\\raw_content_outlinks\\"+str(seed))
        n_threads = 70
        if len(dict_claim) < n_threads:
            n_threads = round(len(dict_claim)/2)
        print ("Seed:",seed)
        dict_size = len(dict_just_url)
        # print("Uniques:",len(dict_just_url))
        batch_size = dict_size/n_threads
        # print (batch_size)
        dict_slices = []
        thread_vec = []

        for t in range(n_threads):

            i = t*batch_size
            j = (t+1)*batch_size
            dict_chunk  = (sorted(dict_just_url.items())[int(i):int(j)])
            # print (file, len(dict_chunk))

            thread_vec += [myThread(t, "Thread-"+str(t), t, dict_chunk, seed)]

        for thread in thread_vec:
            thread.start()
            # print ("Threads started..")
        for thread in thread_vec:
            thread.join()
        print("Unique url:",len(dict_just_url))
        print("--- Avg: %.2f doc/sec ---" % (len(dict_just_url)/(time.time() - start_time)))


    for seed, exceptions in dict_exeptions.items():
        with open("logs_exceptions\\"+str(seed)+".txt", "w") as log_file:
            for url, expt in exceptions.items():
                log_file.write(url+"\t"+expt+"\n")


