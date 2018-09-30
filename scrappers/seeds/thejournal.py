import sys
sys.path.append("..")
from Commons import *
from bs4 import BeautifulSoup


"""
iterate 

1. get full content 
2. 
"""
base_url = 'http://www.thejournal.ie/factcheck/news/page/'
maximum = 5

def parse(doc):
	soup = BeautifulSoup(doc,features='lxml')
	section_list = soup.find_all('div',{'class','post'})
	for claim in section_list:
		claim_txt = claim.find('h4')
		if claim_txt==None:
			continue
		print('claim:',claim_txt.text.strip())
		link = claim_txt.find('a').get('href')
		print('link:',link)


if __name__ == '__main__':
	comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')
	
	for i in range(1,maximum+1):	
		doc = comm._get_full_doc_(base_url+str(i)) 
		parse(doc)
		if i>0:
			break
		

