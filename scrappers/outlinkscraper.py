import os
from bs4 import BeautifulSoup

class OutLinkScraper(object):
    def __init__(self, schemas_path="seeds/schemas/"):
        self.self = self
        self.schemas_path = schemas_path
        self.dict_article_content = {"abc": {"class": "article section"},
                                     "factcheckorg": {"class": "entry-content"},
                                     "fullfact": {"class": "col-xs-12"},
                                     "truthorfiction": {"class": "theiaStickySidebar"},
                                     "washingtonpost": {"class": "article-body"},
                                     "hoaxslayer": {"class": "penci-main-sticky-sidebar"},
                                     "theconversation": {"itemprop": "articleBody"},
                                     "leadstories": {"class": "l_col_s_12 l_col_m_12 l_col_l_8 l_col_xl_8"},
                                     "pandora": {"class": "boxmidlede"},
                                     "radionz": {"class": "article__body"},
                                     "theguardian": {"itemprop": "articleBody"}}

        # self.dict_article_content = {"radionz": {"class": "article__body"}}
        # , "factcheckorg": {"class": "entry-content"},
        #                              "fullfact": {"class": "col-xs-12 no-padding"},
        #                              "truthorfiction": {"class": "theiaStickySidebar"},
        #                              "washingtonpost": {"class": "article-body"}}
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
            print("Parsing: ",seed_name)
            if seed_name in self.dict_article_content:
                self.dict_claim_outlinks[seed_name] = {}
                with open(schema, encoding="utf8") as f:
                    content = f.readlines()
                content = [x.rstrip() for x in content]
                #It starts from 1 to remove the header
                for line in content[1:]:
                    # parts = line.split("   ")
                    parts = line.split("\t")
                    if len(parts) != 12:
                        parts = line.split("   ")

                    claim_id = parts[0]
                    path_id = claim_id
                    if "_" in claim_id:
                        path_id = claim_id.split("_")[0]
                    if claim_id not in self.dict_claim_outlinks[seed_name]:
                        self.dict_claim_outlinks[seed_name][claim_id] = []


                    claim_url = parts[3]
                    full_path = "seeds/raw_content/"+str(seed_name)+"/"+path_id+".html"
                    self.dict_claim_outlinks[seed_name][claim_id] = self.parse_webdocument(seed_name,full_path)
        self.write_outlinks_to_file()

    def parse_webdocument(self, seed_name, file_path):
        outlinks = []
        with open(file_path, encoding="utf8") as f:
            # content = f.readlines()
            soup = BeautifulSoup(f.read(), 'html.parser')
            # print (soup)
            test = soup.find("div", self.dict_article_content[seed_name])
            if test is not None:
                for a in test.find_all("a"):
                    if a.get("href") is not None:
                        if a.get("href").startswith("http"):
                            outlinks += [a.get("href")]
        return outlinks

    def write_outlinks_to_file(self):
        for seed, claims in self.dict_claim_outlinks.items():
            with open("seeds/outlinks/"+ str(seed) +".txt","w") as file_out:
                for claim_id, outlinks in claims.items():
                    for outlink in outlinks:
                        file_out.write(str(claim_id)+"\t"+str(outlink)+"\n")




if __name__ == '__main__':
    outlinkscraper = OutLinkScraper("seeds/schemastest/")
