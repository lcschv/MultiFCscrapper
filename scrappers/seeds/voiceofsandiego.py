import sys
sys.path.append("..")
from Commons import *
from bs4 import BeautifulSoup


"""
iterate 

1. get full content 
2. 
"""
base_url = 'https://www.voiceofsandiego.org/category/fact/'
maximum = 4

comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')

import time
def click_on_load_more(url):
    comm.driver.get(url)
    time.sleep(5)
    i=1
    while i<2:
        i = i+1
        try:
        	comm.driver.find_element_by_class_name('vo-paginate').click()
        	time.sleep(10)
        except:
        	break

def parse(doc):
	soup = BeautifulSoup(doc,features='html.parser')
	primary_section = soup.find_all('div',{'class':'vo-excerpt'})
	for sec in primary_section:
		title_sec = sec.find('h2',{'class':'excerpt-title'})
		if title_sec==None:
			continue
		title = title_sec.find('a').text.strip()
		link = title_sec.find('a').get('href')
		print(title)
		get_page(link)

def get_page(url):
	doc = comm._get_full_doc_(url)
	print(url)
	soup = BeautifulSoup(doc,features='html.parser')
	
	content = soup.find('div',{"data-module":"rich-text"})
	if content is not None:
		# print (content)
		ps = content.find_all('p')
		for p in ps:
			p_txt = p.text.strip()
			if 'CLAIM:' in p_txt:
				print('claim:',p_txt)
			if 'Statement:' in p_txt:
				print('Statement:',p_txt)
			if 'VERDICT:' in p_txt:
				print('VERDICT:',p_txt)
	# else:
	# 	content = soup.find('div',{"class":"vo-rich-text -wysiwyg -article -legacy"})
	# 	if content is not None:
	# 		print ("Puta")

if __name__ == '__main__':
	
	click_on_load_more("https://www.voiceofsandiego.org/category/fact/")
	webpage_content = comm.driver.page_source.encode("utf-8")
	parse(webpage_content)
		

