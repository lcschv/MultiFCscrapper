import sys
sys.path.append("..")
from Commons import *
from ClaimSchema import *
from bs4 import BeautifulSoup



"""
iterate 

1. get full content 
2. 
"""

base_url = 'https://theferret.scot/category/fact-check/'
maximum = 23
count = 0
dict_objects = {}

comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')


import time
def click_on_load_more(url):
    comm.driver.get(url)
    time.sleep(5)
    i=1
    while True:
        i = i+1
        try:
        	comm.driver.find_element_by_id("infinite-handle").click()
        	time.sleep(10)
        	print("HOLAboy")
        except:
        	break


def parse(doc):
	soup = BeautifulSoup(doc,features='html.parser')
	posts = soup.find('div',{'id':'posts'})
	articles = posts.find_all('article')
	for article in articles:
		claim_obj = ClaimSchema()
		title_sec = sec.find('h1',{'class':'entry-title'}).find('a')
		link = title_set.get('href')
		claim = title_sec.text.strip()


		get_page(link,claim_obj)
		global count
		count = count+1
		print(count)
		dict_objects[count] = claim_obj


def get_page(url,claim_obj):
	doc = comm._get_full_doc_(url)
	soup = BeautifulSoup(doc,features='html.parser')
	released_time = soup.find('time')
	if released_time is not None:
		publish_date = released_time.get('datetime') # release date
		# print('publish_date:',publish_date)
		claim_obj.set_publish_date(publish_date)
	content = soup.find('div',{"class":"summary-box"})
	if content is not None:
		# print (content)
		ps = content.find_all('p')
		for p in ps:
			p_txt = p.text.strip()
			if is_number(p_txt[-4:]) and ' on ' in p_txt:
				speaking_date = p_txt[-13:]
				claim_obj.set_claim_date(speaking_date)
				# print('speaking_date:',speaking_date)


if __name__ == '__main__':
	click_on_load_more(base_url)
	# webpage_content = comm.driver.page_source.encode("utf-8")
	# parse(webpage_content)
	# comm.print_object_as_tsv("schemas/theferret.txt", dict_objects)
	# comm.summarize_statistics("statistics/theferret.txt", dict_objects)

