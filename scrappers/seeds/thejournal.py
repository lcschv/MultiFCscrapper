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
base_url = 'http://www.thejournal.ie/factcheck/news/page/'
maximum = 5
count = 0
dict_objects = {}

def parse(doc):
	soup = BeautifulSoup(doc,features='html.parser')
	section_list = soup.find_all('div',{'class':'post'})
	for claim in section_list:
		claim_obj = ClaimSchema()
		date = claim.find('span',{'class','date'})
		if date is not None:
			claim_obj.set_publish_date(date)	#date
		claim_txt = claim.find('h4')
		if claim_txt==None:
			continue
		# print('claim:',claim_txt.text.strip())
		claim_obj.set_claim(claim_txt.text.strip())
		link = claim_txt.find('a').get('href')
		claim_obj.set_claim_url(link)
		print('link:',link)
		get_page(link,claim_obj)

def get_page(url,claim_obj):
	doc = comm._get_full_doc_(url)
	soup = BeautifulSoup(doc,features='html.parser')
	article = soup.find('div',{'id':'articleContent'})
	ps = article.find_all('p')
	flag = 0
	
	for p in ps:
		inline_count =0
		p_txt = p.text.strip()
		strong_part = p.find('strong')
		if strong_part is not None:
			bold_txt = strong_part.text.strip()
			if bold_txt.startswith('claim:'):
				inline_count = inline_count+1
				# judge to output previous one 
				if inline_count>1:
					global count
					count = count+1
					print(count)
					dict_objects[str(count)+'_'+str(inline_count)] = claim_obj

				if len(p_txt)>15:
					claim_obj.set_claim(p_txt)
				else:
					flag = 1
			if bold_txt.startswith('CLAIM:'):
				inline_count = inline_count+1
				if inline_count>1:
					count = count+1
					print(count)
					dict_objects[str(count)+'_'+str(inline_count)] = claim_obj
				if len(p_txt)>15:
					claim_obj.set_claim(p_txt)
				else:
					flag = 1
				inline_count = inline_count+1
			if 'Conclusion:' in bold_txt:
				if len(p_txt)>15:
					claim_obj.set_reason(p_txt)
				else:
					flag = 2	# title
			if 'True' in bold_txt:
				claim_obj.set_label(p_txt)
			if 'FALSE' in bold_txt:
				claim_obj.set_label(p_txt)
			if 'TRUE' in bold_txt:
				claim_obj.set_label(p_txt)
			if 'Verdict' in bold_txt:
				claim_obj.set_label(p_txt)

		else:
			if flag==1:
				claim_obj.set_claim(p_txt)
			if flag ==2:
				claim_obj.set_reason(p_txt)
			flag = 0
		count = count+1
		print(count)
		dict_objects[str(count)] = claim_obj

if __name__ == '__main__':
	comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')
	
	for i in range(1,maximum+1):	
		doc = comm._get_full_doc_(base_url+str(i)) 
		parse(doc)
		comm.print_object_as_tsv("schemas/thejournal.txt", dict_objects)
		comm.summarize_statistics("statistics/thejournal.txt", dict_objects)
		

