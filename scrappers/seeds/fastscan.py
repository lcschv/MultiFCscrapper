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

base_url = 'http://factscan.ca/page/'
maximum = 23
count = 0
dict_objects = {}


def parse(doc):
	soup = BeautifulSoup(doc,features='lxml')
	claim_list = soup.select('.post-content')
	for claim in claim_list:
		claim_obj = ClaimSchema()
		claim_txt = claim.select('h1')
		speaker_claim = claim_txt[0].text.strip().split(':')
		claim_obj.set_speaker(speaker_claim[0])
		claim_obj.set_claim(speaker_claim[1])
		# print('speaker:', speaker_claim[0])
		link = claim_txt[0].a['href']
		# print('link',link)	# link
		claim_obj.set_claim_url(link)
		claim_figure = claim.select('img')	# label
		claim_obj.set_label(claim_figure[0]['alt'])
		# print('label:',claim_figure[0]['alt'])
		claim_exp = claim.select('p')	# claim explain
		# print('labeling_reason:',claim_exp[0].string)
		claim_obj.set_reason(claim_exp[0].string)
		get_page(link,claim_obj)
		global count
		count = count+1
		print(count)
		dict_objects[count] = claim_obj
		# claim_object.pretty_print()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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
	comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')
	
	for i in range(1,maximum+1):
		doc = comm._get_full_doc_(base_url+str(i))
		parse(doc)
	comm.print_object_as_tsv("schemas/factscan.txt", dict_objects)
	comm.summarize_statistics("statistics/factscan.txt", dict_objects)

