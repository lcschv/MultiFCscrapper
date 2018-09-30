import sys
sys.path.append("..")
from Commons import *
from bs4 import BeautifulSoup


"""
iterate 

1. get full content 
2. 
"""
base_url = ' http://checkyourfact.com/page/'
maximum = 18

def parse(doc):
	soup = BeautifulSoup(doc,features='html')
	atom = soup.find('atom')
	article_list = atom.find_all('a')
	for claim in article_list:
		claim_txt = claim.find('name')
		if claim_txt==None:
			continue
		print(claim_txt.text.strip())
		link = claim.get('href')
		print('link',link)


if __name__ == '__main__':
	comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')
	
	for i in range(1,maximum+1):
		if i>0:
			break
		doc = comm._get_full_doc_(base_url+str(i)) 
		parse(doc)
		

