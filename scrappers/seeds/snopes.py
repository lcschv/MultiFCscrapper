from scrappers.Commons import *


class Snopes(Commons):
    def __init__(self, seed_id, seed_url):
        Commons.__init__(self)
        self.destination_folder = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\1\html_claims\\"
        self.seed_id = seed_id
        self.seed_url = seed_url
        self.initialize_driver()

    def start(self):
        content = self._get_full_doc_(self.seed_url)
        filepath = self.destination_folder + "1" +".txt"
        self.write_webpage_content_tofile(content, filepath)



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