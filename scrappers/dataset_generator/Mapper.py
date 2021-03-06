import PyPDF4
import wordninja
import re
import os
# import warc
from scrappers.dataset_generator.DocumentSchema import *
import sys
import ast
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
        self.dict_entities = {}
        self.total = 0
        self.i = 0

    @staticmethod
    def get_all_schema_and_outlinks_files(schemas_path="../seeds/schemastestCopyFinal/", outlinks_path="../seeds/outlinksCopy/"):
        onlyfiles_schema = [os.path.join(schemas_path, f) for f in os.listdir(schemas_path)]
        onlyfiles_outlinks = [os.path.join(outlinks_path, f) for f in os.listdir(outlinks_path)]
        return onlyfiles_schema, onlyfiles_outlinks

    def get_url_from_schema(self, file):
        with open(file, encoding="utf8", errors="ignore") as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        for line in content[1:]:
            parts = line.split("\t")
            if len(parts) != 12:
                parts = line.split("   ")
                if len(parts) != 12:
                    parts = line.split("	")
            if len(parts) != 12:
                print(file, line,"Opa opa opa")
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
            with open(log, encoding="utf8", errors="ignore") as f:
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
        with open(file, encoding="utf8", errors="ignore") as f:
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
        print("This is the total:", len(self.dict_unique_urls))
        return self.dict_unique_urls

    def create_unique_urls_file(self, file_path="data/unique_urls.txt"):
        with open(file_path, "w") as f:
            dict_url = self.get_unique_urls()
            for url,number in dict_url.items():
                f.write(str(number)+"\t"+url+"\n")

    def get_duplicate_claims(self):
        dict_duplicates = {}
        with open("data/duplicate_ids_group_IDonly.txt") as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        for line in content:
            vect = ast.literal_eval(line)
            for x in vect[1:]:
                if x not in dict_duplicates:
                    dict_duplicates[x] = 0
        return (dict_duplicates)

    def merge_claim_schemas(self):
        i = 1
        dict_duplicates_claims = self.get_duplicate_claims()
        # print(dict_duplicates_claims)
        # exit()
        claims_schemas, _ = self.get_all_schema_and_outlinks_files()
        with open("data/claims_schema_separator_tab", "w", encoding="utf8") as f2, open("data/claim_id_mapper.txt", "w") as fileout:
            f2.write(
                "1:ClaimID\t2:Claim\t3:Label\t4:ClaimURL\t5:Reason\t6:Categories\t7:Speaker\t8:Checker\t9:Tags\t10:ArticleTitle\t11:PublishDate\t12:ClaimDate\n")
            # f2.write("ClaimID<<::>>Claim<<::>>Label<<::>>ClaimURL<<::>>Reason<<::>>Categories<<::>>Speaker<<::>>Checker<<::>>Tags<<::>>ArticleTitle<<::>>PublishDate<<::>>ClaimDate\n")
            for file in claims_schemas:
                with open(file, encoding="utf8", errors="ignore") as f:
                    content = f.readlines()
                i = 1

                content = [x.rstrip() for x in content]
                seed = file.split("/")[-1].replace('.txt', '').rstrip()
                print(seed, "--- size:",len(content[1:]))
                self.total+=len(content[1:])
                abbreviation = (seed[:2]+seed[-2:])
                for line in content[1:]:
                    parts = line.split("\t")
                    if len(parts) != 12:
                        parts = line.split("   ")
                        if len(parts) != 12:
                            parts = line.split("	")
                            if len(parts) != 12:
                                parts = line.split("	")
                    if len(parts)!= 12:
                        print(line)
                    old_claim_id = parts[0]
                    if parts[1] == "None":
                        parts[1] = parts[9]
                    new_claim_id = abbreviation+"-"+str(i).zfill(5)
                    if new_claim_id in dict_duplicates_claims:
                        i += 1
                        continue
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
        dict_duplicates_claims = self.get_duplicate_claims()
        # print(len(dict_duplicates_claims))
        dict_claim_urls = {}
        with open(claim_filepath, encoding="utf8", errors="ignore") as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        with open(docid_url_path, "w") as f:
            for line in content:
                parts = line.split("\t")
                claim_id = parts[0]
                if claim_id in dict_duplicates_claims:
                    continue
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
        for file in schemas_files:
            seed = file.split('/')[-1].replace('.txt','')
            with open(file, encoding="utf8", errors="ignore") as f:
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
                    file_path = file_path.replace(".html", ".json")
                    if not os.path.isfile(file_path):
                        # print("File not found....", seed, url)
                        file_path = "None"
                if url not in self.dict_url_rawpath:
                    self.dict_url_rawpath[url] = file_path
                    # print(url, file_path)

        i=0
        for file in outlink_files:
            seed = file.split('/')[-1].replace('.txt', '')
            with open(file, encoding="utf8", errors="ignore") as f:
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
                            if not os.path.isfile(file_path):
                                # print("File not found....", seed, url)
                                file_path = "None"
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

    def get_entities(self,file_entities="data\entities4all"):
        with open(file_entities) as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        for line in content:
            parts = line.split("\t")
            self.dict_entities[parts[0]] = {"num":len(ast.literal_eval((parts[1]))),"entities":ast.literal_eval(parts[1])}

    ####This function reads the outlink files and read all outlinks into a dict###
    ###claim_id: [list_outlinks]
    def get_list_outlinks_by_claim_doc(self):
        dict_outlinks_by_claim_doc = {}
        _, outlinks_files = self.get_all_schema_and_outlinks_files()
        for file in outlinks_files:
            with open(file, encoding="utf8", errors="ignore") as f:
                content = f.readlines()
            seed = file.split("/")[-1].replace('.txt', '').rstrip()
            content = [x.rstrip() for x in content]
            for line in content:
                parts = line.split("\t",2)
                old_id = parts[0]
                url = parts[1]
                new_id = self.dict_old_to_new_claimID[seed][old_id]
                if new_id not in dict_outlinks_by_claim_doc:
                    dict_outlinks_by_claim_doc[new_id] = {}
                if url not in self.dict_exceptions_urls and url not in dict_outlinks_by_claim_doc[new_id]:
                    dict_outlinks_by_claim_doc[new_id][url] = 0
        return dict_outlinks_by_claim_doc

    def read_url_docid(self, file="data/docID_url.txt"):
        dict_url_docid = {}
        with open(file,encoding="utf8",errors="ignore") as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        for line in content:
            parts = line.split("\t",2)
            dict_url_docid[parts[1]] = parts[0]
        # print(dict_url_docid["https://africacheck.org/wp-content/uploads/2018/02/26431154608_45ce1d4ae4_k.jpg"])
        return dict_url_docid


    def get_label_scale(self):
        self.label_scales = {}
        claims_schemas, _ = self.get_all_schema_and_outlinks_files()
        for file in claims_schemas:
            with open(file, encoding="utf8", errors="ignore") as f:
                content = f.readlines()
            content = [x.rstrip() for x in content]
            seed = file.split("/")[-1].replace('.txt', '').rstrip()
            abbv = seed[:2] + seed[-2:]
            self.label_scales[abbv] = {}
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
                label = parts[2].rstrip().replace(u'\xa0', u' ')
                label = re.sub('\s+', ' ', label).strip().lower()
                if label not in self.label_scales[abbv]:
                    self.label_scales[abbv][label] = 0
        return self.label_scales



    # This function will extract and return the pdf file text content.
    def extractPdfText(self, filePath=''):
        # Open the pdf file in read binary mode.
        fileObject = open(filePath, 'rb')

        # Create a pdf reader .
        # Get total pdf page number.
        try:
            pdfFileReader = PyPDF4.PdfFileReader(fileObject)
            currentPageNumber = 0
            totalPageNumber = pdfFileReader.numPages
            text = ''
        except:
            return ""
        try:
            while (currentPageNumber < totalPageNumber):
                pdfPage = pdfFileReader.getPage(currentPageNumber)
                text = text + pdfPage.extractText()
                # Process next page.
                currentPageNumber += 1
        except:
            pass
        text = wordninja.split(text)
        return text

    def write_warc_file(self, buffer):
        self.i+=1
        # header = [
        #     {"WARC-Version:":"WARC/1.0"},
        #     {"WARC-Type:":"warcinfo"},
        #     {"WARC-Date:":str(datetime.datetime.now())},
        #     {"WARC-File-Length:":0},
        #     {"WARC-Number-of-Documents:":len(buffer)},
        #     {"WARC-Data-Type:":"web crawl"},
        #     {"WARC-Record-ID:":self.i},
        #     {"WARC-Content-Length:":0},
        # ]
        file_out = open("trynig_"+str(self.i)+".txt", "w")
        for obj in buffer:
            for attr, value in obj.__dict__.items():
                print(attr + ": " + str(value).replace('\n', ' ').replace('\r', ''), file=file_out)

    def get_full_text(self, file="full_text.txt"):
        dict_full_text = {}
        with open(file) as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        for line in content:
            parts = line.split("::")
            if parts[0] not in dict_full_text:
                dict_full_text[parts[0]] = parts[1]

        return dict_full_text

    def generate_docid_url_sources_file(self):
        self.get_unique_urls()
        dict_plaintext_labels = {"faly":0,"fani":0,"fuct":0,"thal":0}
        dict_labels_scales = self.get_label_scale()
        # for seed,labels in dict_labels_scales.items():
        #     if len(labels) > 16:
        #         print(seed, len(labels), list(labels.keys()))
        # exit()
        dict_out_links_urls = self.get_list_outlinks_by_claim_doc()
        read_url_docid = self.read_url_docid()
        # exit(1)
        self.get_entities()
        self.get_claim_object()
        dict_outlinks_sources = self.get_dict_sources()
        dict_full_text = self.get_full_text()
        inlinks = []
        self.get_original_path_raw_document()
        with open("data/docID_url.txt") as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        self.dict_doc_id_url = {}
        for line in content:
            parts = line.split("\t")
            if "-c-" in parts[0]:
                self.dict_doc_id_url[parts[0].split("-c-")[0]] = parts[0]
            elif "-b-" in parts[0]:
                self.dict_doc_id_url[parts[0].split("-b-")[0]] = parts[0]
        # with open("data/claim_docid_path_url.txt","w",encoding="utf8", errors="ignore") as fout:
        buffer = []
        for line in content[:61]:
            parts = line.split("\t")
            url = parts[1]
            docid = parts[0]
            if url in dict_outlinks_sources:
                claims_sources = self.transform_old_id_to_new(dict_outlinks_sources[url])
                inlinks = [self.dict_doc_id_url[x] for x in claims_sources if self.dict_doc_id_url[x] != docid]

            outlinks = []
            document_record = DocumentSchema()
            claim_info = None
            if "-c-" in docid:
                document_record.set_isClaim("claim")
                claim_info = self.dict_claim_objects[docid.split("-c-")[0]]
                # document_record.set_list_entities(self.dict_entities[claim_info["1:ClaimID"]]["entities"])
                # document_record.set_number_entities(self.dict_entities[claim_info["1:ClaimID"]]["num"])
                if claim_info["1:ClaimID"] in dict_out_links_urls:
                    outlinks = [read_url_docid[x] for x in list(dict_out_links_urls[claim_info["1:ClaimID"]].keys()) if x in read_url_docid]
                document_record.set_list_outlinks(outlinks)
            elif "-b-" in docid:
                document_record.set_isClaim("claim and document")
                claim_info = self.dict_claim_objects[docid.split("-b-")[0]]
                # document_record.set_list_entities(self.dict_entities[claim_info["1:ClaimID"]]["entities"])
                # document_record.set_number_entities(self.dict_entities[claim_info["1:ClaimID"]]["num"])
                if claim_info["1:ClaimID"] in dict_out_links_urls:
                    outlinks = [read_url_docid[x] for x in list(dict_out_links_urls[claim_info["1:ClaimID"]].keys()) if x in read_url_docid]
                document_record.set_list_outlinks(outlinks)
            else:
                document_record.set_isClaim("document")
            try:
                if claim_info is not None:
                    seed_abbrv = claim_info["1:ClaimID"].split("-")[0]
                    document_record.set_id(claim_info["1:ClaimID"])
                    if claim_info["2:Claim"] is not None:
                        document_record.set_claim(claim_info["2:Claim"])
                    else:
                        document_record.set_claim(claim_info["10:ArticleTitle"])
                    document_record.set_label(claim_info["3:Label"])
                    # document_record.set_clai(claim_info["4:ClaimURL"])
                    document_record.set_reason(claim_info["5:Reason"])
                    document_record.set_categories(claim_info["6:Categories"])
                    document_record.set_speaker(claim_info["7:Speaker"])
                    document_record.set_checker(claim_info["8:Checker"])
                    document_record.set_tags(claim_info["9:Tags"])
                    if seed_abbrv in dict_plaintext_labels and claim_info["3:Label"] is not None:
                        document_record.set_label_scale(["Free Text"])
                    else:
                        document_record.set_label_scale(list(dict_labels_scales[docid.split("-")[0]].keys()))
                    document_record.set_article_title(claim_info["10:ArticleTitle"])
                    document_record.set_publish_date(claim_info["11:PublishDate"])
                    document_record.set_claim_date(claim_info["12:ClaimDate"])
            except:
                continue
            document_record.set_doc_id(docid)
            if docid in dict_full_text:
                document_record.set_full_article_text(dict_full_text[docid])
            document_record.set_list_inlinks(inlinks)
            path = self.dict_url_rawpath[url]

            content = None
            if path.endswith(".pdf"):
                print(path)
                content_type = "application/pdf"
                content = self.extractPdfText(path)
            elif path.endswith(".json"):
                content_type = "json"
            else:
                content_type = "text/html"
                temp_file = open(path,"rb")
                content = temp_file.read()
                document_length = len(temp_file.read())
                document_record.set_document_length(document_length)
            # if claim_info is not None:
            #     print(claim_info["1:ClaimID"], docid, path, content_type, url, file=fout)
            # else:
            #     print("XXX-00000", docid, path, content_type, url, file=fout)

                # temp_file.close()

            document_record.set_content_type(content_type)
            # document_record.set_content(path)
            document_record.set_content(content)
            document_record.set_url(url)
            buffer += [document_record]
            if len(buffer) > 20:
                self.write_warc_file(buffer)
                buffer = []
            # document_record.pretty_print()
            # a = ("DocID:", docid, "\toriginalpath:",self.dict_url_rawpath[url], "\tDocumentInlinks:",inlinks,"\tUrl:",url)
            # except:
            #     print(line)

            # print("DocID:", docid, "\toriginalpath:", "\tDocumentInlinks:",inlinks,"\tUrl:",url)


if __name__ == '__main__':
    mapper = Mapper()
    mapper.create_unique_urls_file()
    # mapper.merge_claim_schemas()
    mapper.generate_doc_id_url_file()
    mapper.generate_docid_url_sources_file()