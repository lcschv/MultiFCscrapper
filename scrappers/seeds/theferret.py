import sys
# sys.path.append("..")
from scrappers.Commons import *
from scrappers.ClaimSchema import *
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

comm = Commons()


import time
def click_on_load_more(url):
	comm.driver.get(url)
	time.sleep(40)
	# i=1
	# while True:
	# 	i = i+1
	# 	try:
	# 		comm.driver.find_element_by_id("infinite-handle").click()
	# 		time.sleep(10)
	# 		print("HOLAboy")
	# 	except:
	# 		break


def parse(doc):
	soup = BeautifulSoup(doc,features='html.parser')
	posts = soup.find('div',{'id':'posts'})
	articles = posts.find_all('article')
	for article in articles:
		claim_obj = ClaimSchema()
		title_sec = article.find('h1',{'class':'entry-title'}).find('a')
		link = title_sec.get('href')
		claim_obj.set_claim_url(link)
		claim = title_sec.text.strip()
		claim_obj.set_claim(claim)
		claim_obj.set_article_title(claim)
		categories = article.find("h2",{"class":"entry-subtitle"}).find_all("a")
		category = ""
		for cats in categories:
			category += cats.text.strip() + " "
		claim_obj.set_categories(category)
		publish_date = article.find("time",{"class":"entry-date published"}).text.strip()
		claim_obj.set_publish_date(publish_date)

		get_page(link,claim_obj)
		global count
		count = count+1
		print(count)
		dict_objects[count] = claim_obj


def get_page(url,claim_obj):
	doc = comm._get_full_doc_(url)
	soup = BeautifulSoup(doc,features='html.parser')
	# released_time = soup.find('time')
	# if released_time is not None:
	# 	publish_date = released_time.get('datetime') # release date
	# 	# print('publish_date:',publish_date)
	# 	claim_obj.set_publish_date(publish_date)
	content = soup.find('div',{"class":"entry-content aesop-entry-content"})
	if content is not None:
		# print (content)
		h3s = content.find_all('h3')
		for p in h3s:
			p_txt = p.text.strip()
			if "Ferret Fact Service verdict:" in p_txt:
				label = p_txt.split(':',2)[1]
				claim_obj.set_label(label)
		blockcode = content.find("blockquote")
		if blockcode is not None:
			span = blockcode.find("span")
			if span is not None:
				claim = span.text.strip()
				claim_obj.set_claim(claim)
			cite = 	blockcode.find("cite")
			if cite is not None:
				speaker = cite.text.strip()
				claim_obj.set_speaker(speaker)

	claim_obj.pretty_print()

				# print('speaking_date:',speaking_date)


if __name__ == '__main__':
	click_on_load_more(base_url)
	webpage_content = comm.driver.page_source.encode("utf-8")
	parse(webpage_content)
	comm.print_object_as_tsv("schemas/theferret.txt", dict_objects)
	comm.summarize_statistics("statistics/theferret.txt", dict_objects)

