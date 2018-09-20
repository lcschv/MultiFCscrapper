import sys
sys.path.append("..")
from Commons import *

"""
iterate 

1. get full content 
2. 
"""
base_url = 'http://factscan.ca/page/'
maximum = 23
	

if __name__ == '__main__':
	comm = Commons('C:\L\CredibilityDataset\CredibilityDataset\scrappers\seeds\chromedriver.exe')
	
	for i in range(maximum):
		page_num = i+1
		doc = comm._get_full_doc_(base_url+str(page_num))
		if i>1:
			break
