import sys
sys.path.append("..")
from Commons import *
from bs4 import BeautifulSoup


"""
iterate 

1. get full content 
2. 
"""
base_url = 'http://factscan.ca/page/'
maximum = 23

def parse(doc):
	soup = BeautifulSoup(doc,features='lxml')
	claim_list = soup.select('.post-content')
	for claim in claim_list:
		claim_txt = claim.select('h1')
		print(claim_txt[0].string)
		print('link',claim_txt[0].a['href'])
		claim_figure = claim.select('img')
		print(claim_figure[0]['alt'])
		claim_exp = claim.select('p')
		print(claim_exp[0].string)


if __name__ == '__main__':
	comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')
	
	for i in range(1,maximum+1):
		doc = comm._get_full_doc_(base_url+str(i))
		parse(doc)
		if i>0:
			break

