from scrappers.Commons import *


class Snopes(Commons):
    def __init__(self, seed_id, seed_url, drive_path="scrappers\seeds\chromedriver.exe"):
        Commons.__init__(self, drive_path)
        self.destination_folder = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\1\html_claims\\"
        self.seed_id = seed_id
        self.seed_url = seed_url
        self.initialize_driver()

    def start(self):
        for i in range(1020):
            url = self.seed_url+str(i)
            content = self._get_full_doc_(url)
            #GET THE MULTIPLE URLS OF THE PAGE WITH EACH CLAIM AND CREATE A LIST OF URLS
            #CRAWL THE INFORMATION THAT WE NEED, CLAIMS, ID, LABEL ..
            #WRITE URL TO FILE

            filepath = self.destination_folder + str(i)+".txt"
            self.write_webpage_content_tofile(content, filepath)


if __name__ == '__main__':
    snopes = Snopes(1, "https://www.snopes.com/fact-check/page/", "C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\chromedriver.exe")
    snopes.start()

# def analyze_forbes_page():
#
#     pass
#
#
# def check_next_page(url):
#     try to open url + number
#     url = "https://www.snopes.com/fact-check/page/"
#
#
#

# def get_all_claims_from_page():
#     pass
#
# #This is the main function of the Snopes Scrapper, the one that must be added to the function_mappings dictionary
# def snopes(self, url):
#     destination_folder = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\1\html_claims"
#     for i in range(1, 1021):
#         print (i)
#         get_all_claims_from_page()

    # content = self._get_full_doc_(url)
    # filepath = destination_folder+ i +".txt"
    # self.write_webpage_content_tofile(content, destination_folder)


#         analyze_forbes_page()
# #
#     scrap = new Scrapper("https://www.snopes.com/fact-check/page/")
#     scrap._get_full_doc_(url+1)