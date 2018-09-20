
""""
1- Go to the seed, and check for claims




"""

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
#This is the main function of the Snopes Scrapper, the one that must be added to the function_mappings dictionary
def snopes(self, url):
    path = "C:\Lucas\PhD\CredibilityDataset\data\seeds\\1\html_claims"

    content = self._get_full_doc_(url)
    self.write_webpage_content_tofile(content, path+"\\1.txt")


#         analyze_forbes_page()
# #
#     scrap = new Scrapper("https://www.snopes.com/fact-check/page/")
#     scrap._get_full_doc_(url+1)
if __name__ == '__main__':
