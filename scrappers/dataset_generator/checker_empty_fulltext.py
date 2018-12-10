with open("full_text.txt", encoding="utf8") as f:
    content = f.readlines()
content = [x.rstrip() for x in content]
dict_checker = {}
for line in content:
    parts = line.split("::")
    if parts[1] == "":
        print(line)
        if line.split("::")[0].split("-")[0] not in dict_checker:
            dict_checker[line.split("::")[0].split("-")[0]] = 0
        dict_checker[line.split("::")[0].split("-")[0]] +=1

for seed,value in dict_checker.items():
    print(seed, value)
from bs4 import BeautifulSoup
# import json
# with open("C:\Lucas\PhD\CredibilityDataset\scrappers\seeds\\raw_content\politifact_story\\1.xml") as f:
#     file = json.load(f)
#     print("soup:", file["entry"])

