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
base_url = 'http://checkyourfact.com/page/'
base = 'http://checkyourfact.com'
maximum = 18
count = 0
dict_objects = {}

def parse(doc):
	soup = BeautifulSoup(doc,features='html.parser')
	atom = soup.find('atom')
	article_list = atom.find_all('a')
	for claim in article_list:
		claim_obj = ClaimSchema()
		claim_txt = claim.find('name')
		if claim_txt==None:
			continue
		print(claim_txt.text.strip())	# claim
		claim_obj.set_claim(claim_txt.text.strip())
		link = claim.get('href')
		print('link',base+link)	# url
		claim_obj.set_claim_url(base+link)
		get_page(base+link,claim_obj)
		global count
		count = count+1
		print(count)
		dict_objects[count] = claim_obj


def get_page(url,claim_obj):
	doc = comm._get_full_doc_(url)
	soup = BeautifulSoup(doc,features='html.parser')
	released_time = soup.find('time')
	if released_time is not None:
		publish_date = released_time.text.strip() # release date
		# print('publish_date:',publish_date)
		claim_obj.set_publish_date(publish_date)
	spans = soup.find_all('span')
	author = soup.find('author')
	if author is not None:
		claim_obj.set_checker(author.text.strip())
	for span in spans:
		s_txt = span.text.strip()
		if 'Verdict:' in s_txt:
			claim_obj.set_label(s_txt)
		




if __name__ == '__main__':
	comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')
	
	for i in range(1,maximum+1):
		doc = comm._get_full_doc_(base_url+str(i)) 
		print(base_url+str(i))
		parse(doc)
	comm.print_object_as_tsv("schemas/checkyourfact.txt", dict_objects)
	comm.summarize_statistics("statistics/checkyourfact.txt", dict_objects)
		

