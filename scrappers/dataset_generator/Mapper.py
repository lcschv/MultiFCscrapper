import re
import os
from scrappers.dataset_generator.DocumentSchema import *
import sys
class Mapper(object):

    def __init__(self):
        self.dict_unique_urls = {}
        self.dict_claim_objects = {}
        self.total_number_urls = 1
        self.unique_urls = 1
        self.check_occurance_letter = {}
        self.dict_old_to_new_claimID = {}
        self.dict_outlink_source = {}
        self.dict_exceptions_urls = {}
        self.dict_url_rawpath = {}
        self.total = 0

        self.get_unique_urls()


    @staticmethod
    def get_all_schema_and_outlinks_files(schemas_path="../seeds/schemastest/", outlinks_path="../seeds/outlinks/"):
        onlyfiles_schema = [os.path.join(schemas_path, f) for f in os.listdir(schemas_path)]
        onlyfiles_outlinks = [os.path.join(outlinks_path, f) for f in os.listdir(outlinks_path)]
        return onlyfiles_schema, onlyfiles_outlinks

    def get_url_from_schema(self, file):
        with open(file, encoding="utf8") as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        for line in content[1:]:
            parts = line.split("\t")
            if len(parts) != 12:
                parts = line.split("   ")
                if len(parts) != 12:
                    parts = line.split("	")
            url = parts[3]
            self.total_number_urls += 1
            if url not in self.dict_unique_urls:
                self.dict_unique_urls[url] = self.unique_urls
                self.unique_urls += 1
                self.check_occurance_letter[url] = "c"
                self.dict_outlink_source[url] = [{file.split("/")[-1].replace(".txt", ""): parts[0]}]

    def get_urls_from_log_exceptions(self, logs_path="../logs_exceptions/"):
        logs = [os.path.join(logs_path, f) for f in os.listdir(logs_path)]
        for log in logs:
            with open(log) as f:
                content = f.readlines()
            content= [x.rstrip() for x in content]
            for line in content:
                try:
                    url = line.split("\t")[0]
                    if url not in self.dict_exceptions_urls:
                        self.dict_exceptions_urls[url] = line.split("\t")[1]
                except:
                    continue

    def get_url_from_outlinks(self, file):
        self.get_urls_from_log_exceptions()
        with open(file, errors="ignore") as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        for line in content:
            parts = line.split("\t")
            url = parts[1]
            if url in self.dict_exceptions_urls:
                continue
            self.total_number_urls += 1
            if url not in self.dict_unique_urls:
                self.dict_unique_urls[url] = self.unique_urls
                self.unique_urls += 1
                self.dict_outlinks_urls = self.unique_urls
                self.check_occurance_letter[url] = "o"
                self.dict_outlink_source[url] = [{file.split("/")[-1].replace(".txt",""):parts[0]}]
            else:
                self.dict_outlink_source[url] += [{file.split("/")[-1].replace(".txt", ""): parts[0]}]
                if self.check_occurance_letter[url] == "c":
                   self.check_occurance_letter[url] = "b"

    def get_unique_urls(self):
        files_schema, file_outlinks = Mapper.get_all_schema_and_outlinks_files()
        for file in files_schema:
            self.get_url_from_schema(file)
        for file in file_outlinks:
            self.get_url_from_outlinks(file)
        return self.dict_unique_urls

    def create_unique_urls_file(self, file_path="data/unique_urls.txt"):
        with open(file_path, "w") as f:
            dict_url = self.get_unique_urls()
            for url,number in dict_url.items():
                f.write(str(number)+"\t"+url+"\n")

    def merge_claim_schemas(self):
        i = 1
        claims_schemas, _ = self.get_all_schema_and_outlinks_files()
        with open("data/claims_schema_separator_tab", "w", encoding="utf8") as f2, open("data/claim_id_mapper.txt", "w") as fileout:
            f2.write(
                "1:ClaimID\t2:Claim\t3:Label\t4:ClaimURL\t5:Reason\t6:Categories\t7:Speaker\t8:Checker\t9:Tags\t10:ArticleTitle\t11:PublishDate\t12:ClaimDate\n")
            # f2.write("ClaimID<<::>>Claim<<::>>Label<<::>>ClaimURL<<::>>Reason<<::>>Categories<<::>>Speaker<<::>>Checker<<::>>Tags<<::>>ArticleTitle<<::>>PublishDate<<::>>ClaimDate\n")
            for file in claims_schemas:
                with open(file, encoding="utf8") as f:
                    content = f.readlines()
                i = 1

                content = [x.rstrip() for x in content]
                seed = file.split("/")[-1].replace('.txt', '').rstrip()
                print(seed, "--- size:",len(content[1:]))
                self.total+=len(content[1:])
                abbreviation = (seed[:2]+seed[-1])
                for line in content[1:]:
                    parts = line.split("\t")
                    if len(parts) != 12:
                        parts = line.split("   ")
                        if len(parts) != 12:
                            parts = line.split("	")
                            if len(parts) != 12:
                                parts = line.split("	")
                    old_claim_id = parts[0]
                    new_claim_id = abbreviation+"-"+str(i).zfill(5)
                    if seed not in self.dict_old_to_new_claimID:
                        self.dict_old_to_new_claimID[seed] = {}
                    if old_claim_id not in self.dict_old_to_new_claimID[seed]:
                        self.dict_old_to_new_claimID[seed][old_claim_id] = new_claim_id

                    fileout.write(new_claim_id+"\t"+old_claim_id+"\t"+seed+"\n")
                    f2.write(abbreviation+"-"+str(i).zfill(5)+"\t"+re.sub(' +',' ',"\t".join(parts[1:]))+"\n")

                    i+=1
        print("Total number of claims:" ,self.total)
    def get_dict_sources(self):
        no_duplicates_urls = {}
        for url, values in self.dict_outlink_source.items():
            for dict in values:
                for seed, value in dict.items():
                    if url not in no_duplicates_urls:
                        no_duplicates_urls[url] = {}
                    if seed not in no_duplicates_urls[url]:
                        no_duplicates_urls[url][seed] = set()
                    no_duplicates_urls[url][seed].add(value)
        return no_duplicates_urls


    def generate_doc_id_url_file(self,claim_filepath="data\claims_schema_separator_tab" ,docid_url_path = "data/docID_url.txt"):
        self.merge_claim_schemas()
        # dict_unique_urls = self.get_unique_urls()
        dict_claim_urls = {}
        with open(claim_filepath, encoding="utf8") as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        with open(docid_url_path, "w") as f:
            for line in content:
                parts = line.split("\t")
                claim_id = parts[0]
                url = parts[3]
                if url in self.check_occurance_letter:
                    docid = str(claim_id)+"-"+str(self.check_occurance_letter[url])+"-"+str(self.dict_unique_urls[url]).zfill(6)
                    # docid = str(claim_id)+str(self.check_occurance_letter[url])+str(dict_unique_urls[url]).zfill(6)
                    if url not in dict_claim_urls:
                        dict_claim_urls[url] = docid
                    f.write(docid+"\t"+url+"\n")

            for url, id in self.dict_unique_urls.items():
                if url not in dict_claim_urls:
                    first_part = "XXX-00000-o-"
                    docid = str(first_part)+str(id).zfill(6)
                    f.write(docid+"\t"+url+"\n")

    def transform_old_id_to_new(self, dict_sources):
        sources = []
        for seed, values in dict_sources.items():
            for value in values:
                sources += [self.dict_old_to_new_claimID[seed][value]]
        return sources

    def get_original_path_raw_document(self):
        schemas_files ,outlink_files = self.get_all_schema_and_outlinks_files()
        print(schemas_files)
        for file in schemas_files:
            seed = file.split('/')[-1].replace('.txt','')
            with open(file, encoding="utf8") as f:
                content = f.readlines()
            content = [x.rstrip() for x in content]
            for line in content[1:]:
                parts = line.split("\t")
                if len(parts) != 12:
                    parts = line.split("   ")
                    if len(parts) != 12:
                        parts = line.split("	")
                        if len(parts) != 12:
                            parts = line.split("	")
                url = parts[3]
                claim_id = parts[0]
                if "_" in claim_id:
                    claim_id = claim_id.split('_')[0]
                file_path = "../seeds/raw_content/"+seed+"/"+str(claim_id)+".html"
                if not os.path.isfile(file_path):
                    file_path = file_path.replace(".html", ".txt")
                if url not in self.dict_url_rawpath:
                    self.dict_url_rawpath[url] = file_path
                    # print(url, file_path)

        i=0
        for file in outlink_files:
            seed = file.split('/')[-1].replace('.txt', '')
            with open(file, encoding="utf8") as f:
                content = f.readlines()
                content = [x.rstrip() for x in content]
                dict_claim = {}
                for line in content:
                    parts = line.split("\t")
                    claim_id = line.split("\t")[0]
                    # print(line)
                    url = line.split("\t")[1]
                    if claim_id not in dict_claim:
                        i = 1
                        dict_claim[claim_id] = {}
                    if url not in dict_claim[claim_id]:
                        dict_claim[claim_id][url] = i
                        i += 1
                    if url not in self.dict_url_rawpath and url not in self.dict_exceptions_urls:
                        file_path= "../seeds/raw_content_outlinks/"+seed+"/"+str(claim_id)+"/"+str(dict_claim[claim_id][url])+".html"
                        if not os.path.isfile(file_path):
                            file_path = file_path.replace(".html", ".pdf")
                        self.dict_url_rawpath[url] = file_path

    def get_claim_object(self, schemas_filepath="data/claims_schema_separator_tab"):
        with open(schemas_filepath, encoding="utf8") as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        for line in content[1:]:
            parts = line.split("\t")
            if len(parts) != 12:
                parts = line.split("   ")
                if len(parts) != 12:
                    parts = line.split("	")
                    if len(parts) != 12:
                        parts = line.split("	")
                        if len(parts) != 12:
                            parts = line.split("	")
            claim_id = parts[0]
            if claim_id not in self.dict_claim_objects:
                self.dict_claim_objects[claim_id] = {k:v for k, v in zip(content[0].split("\t"), line.split("\t"))}
                # for k,v in zip(content[0].split("\t"),line.split("\t")):
                #     if v == "":
                #         print(k)
                #         print(line)
                #         v = None

                # self.dict_claim_objects[claim_id] = {k:v for k, v in zip(content[0].split("\t"), line.split("\t"))}

    def generate_docid_url_sources_file(self):
        self.get_claim_object()
        dict_outlinks_sources = self.get_dict_sources()
        inlinks = []
        self.get_original_path_raw_document()
        with open("data/docID_url.txt") as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        for line in content:
            parts = line.split("\t")
            url = parts[1]
            docid = parts[0]
            if url in dict_outlinks_sources:
                inlinks = self.transform_old_id_to_new(dict_outlinks_sources[url])

            document_record = DocumentSchema()
            claim_info = None
            if "-c-" in docid:
                document_record.set_isClaim(True)
                claim_info = self.dict_claim_objects[docid.split("-c-")[0]]
            elif "-b-" in docid:
                document_record.set_isClaim(True)
                claim_info = self.dict_claim_objects[docid.split("-b-")[0]]
            try:
                if claim_info is not None:
                    document_record.set_id(claim_info["1:ClaimID"])
                    document_record.set_claim(claim_info["2:Claim"])
                    document_record.set_label(claim_info["3:Label"])
                    # document_record.set_clai(claim_info["4:ClaimURL"])
                    document_record.set_reason(claim_info["5:Reason"])
                    document_record.set_categories(claim_info["6:Categories"])
                    document_record.set_speaker(claim_info["7:Speaker"])
                    document_record.set_checker(claim_info["8:Checker"])
                    document_record.set_tags(claim_info["9:Tags"])
                    document_record.set_article_title(claim_info["10:ArticleTitle"])
                    document_record.set_publish_date(claim_info["11:PublishDate"])
                    document_record.set_claim_date(claim_info["12:ClaimDate"])
            except:
                continue
            document_record.set_doc_id(docid)
            document_record.set_origins(inlinks)
            path = self.dict_url_rawpath[url]
            if path.endswith(".pdf"):
                content_type = "application/pdf"
            else:
                content_type = "text/html"
                # temp_file = open(path,"rb")
                # document_length = len(temp_file.read())
                # temp_file.close()
                # document_record.set_document_length(document_length)
            document_record.set_content_type(content_type)
            document_record.set_content(path)
            document_record.set_url(url)
            document_record.pretty_print()
            # a = ("DocID:", docid, "\toriginalpath:",self.dict_url_rawpath[url], "\tDocumentInlinks:",inlinks,"\tUrl:",url)
            # except:
            #     print(line)

            # print("DocID:", docid, "\toriginalpath:", "\tDocumentInlinks:",inlinks,"\tUrl:",url)


if __name__ == '__main__':
    mapper = Mapper()
    # mapper.create_unique_urls_file()
    mapper.merge_claim_schemas()
    # mapper.generate_doc_id_url_file()
    # mapper.generate_docid_url_sources_file()