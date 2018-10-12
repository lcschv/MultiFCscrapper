import os
from bs4 import BeautifulSoup

class OutLinkScraper(object):
    def __init__(self, schemas_path="seeds/schemas/"):
        self.self = self
        self.schemas_path = schemas_path
        self.dict_article_content = {"abc": {"class": "article section"}, "factcheckorg": {"class": "entry-content"},
                                     "fullfact": {"class": "col-xs-12 no-padding"},
                                     "truthorfiction": {"class": "theiaStickySidebar"},
                                     "washingtonpost": {"class": "article-body"}}
        self.read_schemas()
        # "div", {"class": "inline-content wysiwyg right"}

    def get_list_schemas(self):
        onlyfiles = [os.path.join(self.schemas_path, f) for f in os.listdir(self.schemas_path)]
        return onlyfiles

    def read_schemas(self):
        self.dict_claim_outlinks = {}
        schemas = self.get_list_schemas()

        for schema in schemas:
            seed_name = schema.split("/")[-1].replace(".txt","")
            self.dict_claim_outlinks[seed_name] = {}
            with open(schema, encoding="utf8") as f:
                content = f.readlines()
            content = [x.rstrip() for x in content]
            #It starts from 1 to remove the header
            for line in content[1:]:
                parts = line.split("   ")
                claim_id = parts[0]
                if claim_id not in self.dict_claim_outlinks[seed_name]:
                    self.dict_claim_outlinks[seed_name][claim_id] = []
                if "_" in claim_id:
                    claim_id = claim_id.split("_")[0]

                claim_url = parts[3]
                full_path = "seeds/raw_content/"+str(seed_name)+"/"+claim_id+".html"
                self.parse_webdocument(seed_name,full_path)
        print (self.dict_claim_outlinks)

    def parse_webdocument(self, seed_name, file_path):
        with open(file_path, encoding="utf8") as f:
            # content = f.readlines()
            soup = BeautifulSoup(f.read(), 'html.parser')
            # print (soup)
            print (self.dict_article_content[seed_name])
            test = soup.find("div", self.dict_article_content[seed_name])
            print (test)


    def get_clam_id(self):
        pass



if __name__ == '__main__':
    outlinkscraper = OutLinkScraper("seeds/schemastest/")
