import sys
sys.path.append("..")
from Commons import *
from bs4 import BeautifulSoup


"""
iterate 

1. get full content 
2. 
"""
base_url = 'https://zimfact.org/category/fact-reports/page/'
maximum = 4

comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')
	

def parse(doc):
	soup = BeautifulSoup(doc,features='lxml')
	primary_section = soup.find(id='primary')
	article_list = primary_section.find_all('article',{'class','page-article'})
	for article in article_list:
		more_link = article.find('div',{'class','more-link'})
		link = more_link.find('a').get('href')
		print('link:',link)
		get_page(link)

def get_page(url):
	doc = comm._get_full_doc_(url)
	soup = BeautifulSoup(doc,features='lxml')
	block = soup.find('div',{'class','entry-content'})
	ps = block.find_all('p')
	for p in ps:
		p_txt = p.text.strip()
		if 'CLAIM:' in p_txt:
			print('claim:',p_txt)
		if 'CONCLUSION:' in p_txt:
			print('conclusion:',p_txt)
		if 'VERDICT:' in p_txt:
			print('VERDICT:',p_txt)

if __name__ == '__main__':
	
	for i in range(1,maximum+1):	
		doc = comm._get_full_doc_(base_url+str(i)) 
		parse(doc)
		if i>0:
			break
		

