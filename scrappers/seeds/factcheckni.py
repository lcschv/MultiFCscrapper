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
base_url = 'https://www.factcheckni.org/fact-category/'
maximum = 4

comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')
count = 0
dict_objects = {}
category = ''

def parse(doc):
	soup = BeautifulSoup(doc,features='html.parser')
	article_list = soup.find_all('div',{'class','grid-column'})
	for article in article_list:
		claim_obj = ClaimSchema()
		global category
		claim_obj.set_categories(category)
		fact_title = article.find('div',{'class','fact-title'})
		link = fact_title.find('a').get('href')
		title = fact_title.find('a').text.strip()
		print('title',title)
		claim_obj.set_article_title(title)
		claim_obj.set_claim_url(link)
		get_page(link,claim_obj)
		global count
		count = count+1
		print(count)
		dict_objects[count] = claim_obj


def get_page(url,claim_obj):
	doc = comm._get_full_doc_(url)
	soup = BeautifulSoup(doc,features='html.parser')
	post_time = soup.find('div',{'class','post-date'})
	if post_time is not None:
			claim_obj.set_publish_date(post_time.text.strip())
	brief = soup.find('div',{'class','in-brief'})
	ps = brief.find_all('p')
	for p in ps:
		p_txt = p.text.strip()
		if 'CLAIM:' in p_txt:
			# print('claim:',p_txt)
			claim_obj.set_claim(p_txt)
		if 'CONCLUSION:' in p_txt:
			# print('conclusion:',p_txt)
			claim_obj.set_label(p_txt)
		if 'VERDICT:' in p_txt:
			# print('VERDICT:',p_txt)
			claim_obj.set_label(p_txt)


if __name__ == '__main__':
	for keyword in ['brexit','economy','education','elections','europe','facts','health','immigration','law','peace']:	
		category = keyword
		doc = comm._get_full_doc_(base_url+keyword) 
		parse(doc)
	comm.print_object_as_tsv("schemas/factcheckni.txt", dict_objects)
	comm.summarize_statistics("statistics/factcheckni.txt", dict_objects)
		
