import sys
sys.path.append("..")
from Commons import *
from bs4 import BeautifulSoup


"""
iterate 

1. get full content 
2. 
"""
base_url = 'https://www.factcheckni.org/fact-category/'
maximum = 4

comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')
	

def parse(doc):
	soup = BeautifulSoup(doc,features='html.parser')
	article_list = soup.find_all('div',{'class','grid-column'})
	for article in article_list:
		fact_title = article.find('div',{'class','fact-title'})
		link = fact_title.find('a').get('href')
		title = fact_title.find('a').text.strip()
		print('title',title)
		get_page(link)


def get_page(url):
	doc = comm._get_full_doc_(url)
	soup = BeautifulSoup(doc,features='html.parser')
	brief = soup.find('div',{'class','in-brief'})
	ps = brief.find_all('p')
	for p in ps:
		p_txt = p.text.strip()
		if 'CLAIM:' in p_txt:
			print('claim:',p_txt)
		if 'CONCLUSION:' in p_txt:
			print('conclusion:',p_txt)
		if 'VERDICT:' in p_txt:
			print('VERDICT:',p_txt)

if __name__ == '__main__':
	
	i=0
	for keyword in ['brexit','economy','education','elections','europe','facts','health','immigration','law','peace']:	
		doc = comm._get_full_doc_(base_url+keyword) 
		parse(doc)
		i = i+1
		if i>1:
			break
		
