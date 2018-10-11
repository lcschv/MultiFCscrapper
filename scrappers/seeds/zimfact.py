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
base_url = 'https://zimfact.org/category/fact-reports/page/'
maximum = 5
count = 0
dict_objects = {}

comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')


def parse(doc):
	soup = BeautifulSoup(doc,features='html.parser')
	primary_section = soup.find(id='primary')
	article_list = primary_section.find_all('article',{'class':'page-article'})
	for article in article_list:
		claim_obj = ClaimSchema()
		more_link = article.find('div',{'class':'more-link'})
		link = more_link.find('a').get('href')
		print('link:',link)
		claim_obj.set_claim_url(link)
		get_page(link,claim_obj)

		global count
		count = count+1
		print(count)
		dict_objects[count] = claim_obj

def get_page(url, claim_obj):
	doc = comm._get_full_doc_(url)
	soup = BeautifulSoup(doc,features='html.parser')

	# find title
	main_part = soup.find('main',{'id':'more-content'})
	title = main_part.find('h1',{'class','entry-title'})
	if title is not None:
		claim_obj.set_article_title(title.text.strip())
	date = main_part.find('time')
	if date is not None:
		claim_obj.set_publish_date(date.get('datetime'))
	cates = main_part.find('span',{'class':'entry-catagory'})
	if cates is not None:
		claim_obj.set_categories(cates.text.strip())
	author = main_part.find('span',{'class':'entry-author'})
	if author is not None:
		claim_obj.set_checker(author.text.strip())
	# find claim and label
	block = soup.find('div',{'class':'entry-content'})
	ps = block.find_all('p')
	flag = 0
	for p in ps:
		p_txt = p.text.strip()
		bold = p.find('strong')
		if bold is not None:
			bold_txt = bold.text.strip()
			if 'CLAIM:' in bold_txt:
				# print('claim:',p_txt)
				if len(p_txt)>15:
					claim_obj.set_claim(p_txt)
				else:
					flag = 1	# claim
			if 'CONCLUSION:' in bold_txt:
				# print('conclusion:',p_txt)
				if len(p_txt)>15:
					claim_obj.set_reason(p_txt)
				else:
					flag = 2
			if 'VERDICT:' in bold_txt:
				print('VERDICT:',p_txt)
				claim_obj.set_label(p_txt)
			if 'Source:' in bold_txt:
				claim_obj.set_speaker(p_txt)
			if 'Author:' in bold_txt:
				claim_obj.set_checker(p_txt)
		else:
			if flag==1:
				claim_obj.set_claim(p_txt)
			if flag==2:
				claim_obj.set_reason(p_txt)
			flag=0

if __name__ == '__main__':
	
	for i in range(1,maximum+1):	
		doc = comm._get_full_doc_(base_url+str(i)) 
		parse(doc)
	comm.print_object_as_tsv("schemas/zimfact.txt", dict_objects)
	comm.summarize_statistics("statistics/zimfact.txt", dict_objects)
		

