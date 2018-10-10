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
base_url = 'https://africacheck.org/latest-reports/page/'
maximum = 44
count = 0
dict_objects = {}

def parse(doc):
	soup = BeautifulSoup(doc,features='html')
	claim_list = soup.select('.article-content')
	for claim in claim_list:
		claim_obj = ClaimSchema()

		claim_title = claim.find('h2')
		# print('claim_title:',claim_title[0].string)
		claim_obj.set_article_title(claim_title.text.strip())
		# get link under claim_title
		link = claim_title.find('a').get('href')
		# print('link:',link[0]['href'])
		claim_obj.set_claim_url(link)

		#get report verdict
		report_verdict = claim.find('div',{'class':'report-verdict'})
		if report_verdict is not None:
			claim_obj.set_label(report_verdict.text.strip())
		# get update time
		update_time = claim.select('time')
		print('date-published:',update_time[0]['datetime'])
		claim_obj.set_publish_date(update_time)
		
		get_page(link,claim_obj)
		global count
		print(count)
		count = count+1
		

def get_page(url, claim_obj):
	doc = comm._get_full_doc_(url)
	soup = BeautifulSoup(doc,features='html.parser')

	claims = soup.find_all('div',{'class':'inline-rating'})
	in_count = 1
	for claim in claims:
		c_content = claim.find('p',{'class':'claim-content'})
		claim_obj.set_claim(c_content.text.strip())
		verdict = claim.find('div',{'class':'indicator'})
		if verdict is not None:
			claim_obj.set_label(verdict.find('span').text.strip())
		in_count = in_count+1
		global count
		dict_objects[str(count)+'_'+str(in_count)] = claim_obj



if __name__ == '__main__':
	comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')
	
	for i in range(maximum):
		page_num = i+1
		doc = comm._get_full_doc_(base_url+str(page_num))
		parse(doc)
	comm.print_object_as_tsv("schemas/africacheck.txt", dict_objects)
	comm.summarize_statistics("statistics/africacheck.txt", dict_objects)

