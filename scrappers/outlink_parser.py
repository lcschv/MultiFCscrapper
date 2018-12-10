import os
from bs4 import BeautifulSoup

class OutLinkScraper(object):
    def __init__(self, schemas_path="seeds/schemas/"):
        self.self = self
        self.schemas_path = schemas_path


        #Please add the seed name, html tag name, and information about the tag.
        self.dict_article_content= {
                                    # "radionz":{"div":{"class":"article_body"}},
                                    # "climatefeedback":{"div":{"class":"entry-content"}},
                                    "voiceofsandiego":{"div":{"data-module":"rich-text"}},
                                    # "gossipcop":{"div":{"class":"blurb-text"}},
                                    # "pesacheck":{"div":{"class":"section-content"}},
                                    # "nytimes":{"attrs":{"itemprop":"articleBody"}},
                                    # "huffingtonpostca":{"attrs":{"class":"post-contents"}},
                                    # "mprnews":{"attrs":{"class":"entry-content"}},
                                    # "pandora":{"div":{"class": "storyblock"}},
                                    # "washingtonpost":{"div":{"class": "article-body"}},
                                    # "truthorfiction":{"div":{"class": "inner-post-entry"}},
                                    # "factcheckorg":{"div":{"class": "entry-content"}},
                                    # "fullfact":{"div":{"class": "col-xs-12 no-padding"}},
                                    # "hoaxslayer":{"div":{"class": "penci-main-sticky-sidebar"}},
                                    # "theconversation":{"div":{"class": "grid-ten large-grid-nine grid-last content-body content entry-content instapaper_body"}},
                                    # "leadstories":{"div":{"class": "l_col_s_12 l_col_m_12 l_col_l_8 l_col_xl_8"}},
                                    # "theguardian":{"div":{"itemprop": "articleBody"}},
                                    # "wral":{"attrs":{"class":"p402_premium"}},
                                    # "observatory":{"section":{"class":"entry-content clearfix"}},
                                    # "swissinfo":{"div":{"itemprop": "articleBody"}},
                                    # "snopes":{"div":{"class":"post-body-card post-card card"}},
                                    # "abc":{"div":{"class":"article section"}}

        }

        ####Please add the seedname and the baseurl (without the / in the end)
        self.dict_base_url = {
                                    "radionz":"https://www.radionz.co.nz",
                                    "nytimes":"https://www.nytimes.com",
                                    "huffingtonpostca":"https://www.huffingtonpost.ca",
                                    "mprnews":"https://www.mprnews.org",
                                    "pandora":"https://pandora.nla.gov.au",
                                    "washingtonpost":"https://www.washingtonpost.com",
                                    "truthorfiction":"https://www.truthorfiction.com",
                                    "factcheckorg":"https://www.factcheck.org",
                                    "fullfact":"https://fullfact.org",
                                    "hoaxslayer":"https://hoax-slayer.com",
                                    "theconversation":"https://theconversation.com",
                                    "leadstories":"https://leadstories.com",
                                    "theguardian":"https://www.theguardian.com/us",
                                    "wral":"https://www.wral.com",
                                    "observatory":"https://observatory.journalism.wisc.edu",
                                    "swissinfo":"https://www.swissinfo.ch",
                                    "voiceofsandiego":"https://www.voiceofsandiego.org",
                                    "snopes":"https://www.snopes.com",
                                    "abc":"https://www.abc.net.au",
                                    "gossipcop":"https://www.gossipcop.com",
                                    "climatefeedback":"https://www.climatefeedback.org",
                                    "pesacheck":"https://www.pesacheck.org"
                              }

        self.read_schemas()

    def get_list_schemas(self):
        onlyfiles = [os.path.join(self.schemas_path, f) for f in os.listdir(self.schemas_path)]
        return onlyfiles

    def read_schemas(self):
        self.dict_claim_outlinks = {}
        schemas = self.get_list_schemas()
        for schema in schemas:
            seed_name = schema.split("/")[-1].replace(".txt","")
            print(seed_name)
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
                        if len(parts) != 12:
                            parts = line.split("	")

                    claim_id = parts[0]
                    path_id = claim_id
                    if "_" in claim_id:
                        path_id = claim_id.split("_")[0]
                    if claim_id not in self.dict_claim_outlinks[seed_name]:
                        self.dict_claim_outlinks[seed_name][claim_id] = []


                    claim_url = parts[3]
                    full_path = "seeds/raw_content/"+str(seed_name)+"/"+path_id+".html"

                    self.dict_claim_outlinks[seed_name][claim_id] = self.parse_webdocument(seed_name,full_path)
        # self.write_outlinks_to_file()

    def parse_webdocument(self, seed_name, file_path):
        outlinks = []
        try:
            f = open(file_path, encoding="utf8")
        except:
            f = open(file_path.replace(".html",".txt"), encoding="utf8")
        # content = f.readlines()
        soup = BeautifulSoup(f.read(), 'html.parser')
        # print (soup)
        for key, value in self.dict_article_content[seed_name].items():
            if key == "attrs":
                # test = soup.find(attrs={"itemprop":"articleBody"})
                test = soup.find(attrs=value)
            elif key == "id":
                test = soup.find(id=value)
            else:
                test = soup.find(key,value)
        print(test)
        if test is not None:
            for a in test.find_all("a"):
                if a.get("href") is not None:
                    if a.get("href").startswith("http"):
                        outlinks += [a.get("href")]
                    elif seed_name == "pandora" and a.get("href").replace("/external.html?link=","").startswith("http"):
                        outlinks += [a.get("href").replace("/external.html?link=","")]
                    elif a.get("href").startswith("/"):
                        outlinks += [self.dict_base_url[seed_name]+a.get("href")]
        return outlinks


    def write_outlinks_to_file(self):
        for seed, claims in self.dict_claim_outlinks.items():
            with open("seeds/outlinks/"+ str(seed) +".txt","w") as file_out:
                for claim_id, outlinks in claims.items():
                    for outlink in outlinks:
                        file_out.write(str(claim_id)+"\t"+str(outlink)+"\n")




if __name__ == '__main__':
    outlinkscraper = OutLinkScraper("seeds/temp/")
