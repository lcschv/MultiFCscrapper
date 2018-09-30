import sys
sys.path.append("..")
from Commons import *
from bs4 import BeautifulSoup


"""
iterate 

1. get full content 
2. 
"""
base_url = 'https://africacheck.org/latest-reports/page/'
maximum = 44

def parse(doc):
	soup = BeautifulSoup(doc,features='html')
	claim_list = soup.select('.article-content')
	for claim in claim_list:
		claim_title = claim.select('h2')
		print('claim_title:',claim_title[0].string)
		# get link under claim_title
		link = claim_title[0].select('a')
		print('link:',link[0]['href'])
		#get report claim if possible
		report_claim = claim.select('.report-claim')
		if len(report_claim)>0:
			report_claim_txt = report_claim[0].select('strong')
			print('report_claim:',report_claim_txt[0].string)
		#get report verdict if possible
		report_verdict = claim.select('.report-verdict')
		if len(report_verdict)>0:
			# get verdict p from report verdict
			verdict_p = report_verdict[0].select('strong')
			print('verdict:',verdict_p[0].string)
		# get update time
		update_time = claim.select('time')
		print('date-published:',update_time[0]['datetime'])
		print('----end of one claim---')


if __name__ == '__main__':
	comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')
	
	for i in range(maximum):
		page_num = i+1
		doc = comm._get_full_doc_(base_url+str(page_num))
		parse(doc)
		if i>0:
			break

