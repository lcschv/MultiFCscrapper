import os
from bs4 import BeautifulSoup
import re
from bs4.element import NavigableString

class Tokenizer(object):
    def __init__(self):
        pass
    def convert_accented_characters(self, text):
        """
        Converts accented characters in a string to their unaccented forms.
        The string is assumed to be in UTF-8 form.
        """
        # TODO: we should account for other types of encodings and remove all
        # strange characters.
        special_chars = "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿšŽčžŠšČłńężść"
        chars = "aaaaaaeceeeeiiiidnoooooxouuuuypsaaaaaaeceeeeiiiionooooooouuuuypysZczSsClnezsc"

        new_text = ""
        for c in text:
            index = special_chars.find(c)
            if index != -1:
                new_text += chars[index]
            else:
                new_text += c
        return new_text

    def remove_urls(self, text):
        """
        Removes urls from a string.
        """
        regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(regex, '', text)

    def remove_emails(self, text):
        """
        Removes emails from a string.
        """
        # The Regex is a simplified version of the one that would account
        # for all emails, but it is good enough for most cases.
        text = re.sub('\S+@\S+(\.\S+)+', '', text)

        # Sometimes the domain is omitted from the email.
        text = re.sub('\S\S\S+\.\S\S\S+', '', text)
        return text

    def tokenize_text(self, text):
        """
        Extracts a list of textual tokens from a string, ignoring
        urls, titles and emails. This might not be useful in our case, but still.
        """
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        text = self.convert_accented_characters(text.strip()).lower()
        if len(text) == 0 or text == None:
            return [];

        return re.compile("[^a-zA-Z0-9]+").split(text)

    def tokenize(self, html):
        """
        Returns a list of HtmlTokens extracted from an HTML document.
        """
        result = []
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style tags.
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]
        for br in soup.find_all("br"):
            if len(br.findChildren()) == 0:
                br.replace_with(" linebreak ")

        # Iterate through all text elements.
        n_strs = [i for i in soup.recursiveChildGenerator() if type(i) == NavigableString]
        for n_str in n_strs:
            content = n_str.rstrip('\r')
            if len(content) == 0 or content is None:
                continue

            # Tokenize content and remove double spaces.
            tkns = self.tokenize_text(content)
            tkns = [t for t in tkns if (len(t) > 1 and re.match("^\S+$", t) != None)]

            #Append each token from each here
            for i in range(0, len(tkns)):
                result.append(tkns[i])

        return result

class Parser(object):
    def __init__(self, schemas_path="seeds/schemas/"):
        self.self = self
        self.schemas_path = schemas_path
        self.dict_info = {}
        self.tokenizer = Tokenizer()

        #Please add the seed name, html tag name, and information about the tag.
        # self.dict_article_content= {
        #                             "radionz":{"div":{"class":"article__body"}},
        #                             "climatefeedback":{"div":{"class":"entry-content"}},
        #                             "gossipcop":{"div":{"class":"blurb-text"}},
        #                             "pesacheck":{"div":{"class":"section-content"}},
        #                             "nytimes":{"attrs":{"itemprop":"articleBody"}},
        #                             "huffingtonpostca":{"attrs":{"class":"post-contents"}},
        #                             "mprnews":{"attrs":{"class":"entry-content"}},
        #                             "pandora":{"div":{"class": "storyblock"}},
        #                             "washingtonpost":{"div":{"class": "article-body"}},
        #                             "truthorfiction":{"div":{"class": "inner-post-entry"}},
        #                             "factcheckorg":{"div":{"class": "entry-content"}},
        #                             "fullfact":{"div":{"class": "col-xs-12 no-padding"}},
        #                             "hoaxslayer":{"div":{"class": "penci-main-sticky-sidebar"}},
        #                             "theconversation":{"div":{"class": "grid-ten large-grid-nine grid-last content-body content entry-content instapaper_body"}},
        #                             "leadstories":{"div":{"class": "l_col_s_12 l_col_m_12 l_col_l_8 l_col_xl_8"}},
        #                             "theguardian":{"div":{"itemprop": "articleBody"}},
        #                             "wral":{"attrs":{"class":"p402_premium"}},
        #                             "observatory":{"section":{"class":"entry-content clearfix"}},
        #                             "swissinfo":{"div":{"itemprop": "articleBody"}},
        #                             "snopes":{"div":{"class":"post-body-card post-card card"}},
        #                             "abc":{"div":{"class":"article section"}},
        #                              'africacheck':{"div":{"id":"main"}},
        #                             "politico":{"div":{"class":"story-text"}},
        #                             "factly":{"div":{"class":"col-8 main-content"}},
        #                             "altnews":{"div":{"class":"td-ss-main-content"}},
        #                             "boomlive":{"div":{"id":"mvp-post-content"}},
        #                             "verafiles":{"div":{"class":"row"}},
        #                             'thejournal': {"div": {"class": "post"}},
        #                             'crikey':{"div":{"class":"grid_9 prefix_2"}},
        #                             'factscan':{"div":{"class":"list-post"}},
        #                             'factcheckni': {"div": {"id": "primary"}},
        #                             # 'voiceofsandiego':{"div":{"class":"vo-page"}},# need to change the code a bit
        #                             'africacheck':{"div":{"id":"main"}},
        #                             'checkyourfact':{"div":{"id":"ob-read-more-selector"}},
        #                             'zimfact':{"div":{"class":"entry-content"}},
        #                             'theferret':{"div":{"class":"entry-content"}},
        #                             "politifact_stmt":{"div":{"class":"article__text"}},
        #                             "politifact_story":{"entry"},
        #                             "politifact_promise":{"div":{"class":"article__text"}}
        # }
        self.dict_article_content = {
            "ranz": {"div": {"class": "article__body"}},
            "clck": {"div": {"class": "entry-content"}},
            "goop": {"div": {"class": "blurb-text"}},
            "peck": {"div": {"class": "section-inner sectionLayout--insetColumn"}},
            "nyes": {"attrs": {"itemprop": "articleBody"}},
            "huca": {"attrs": {"class": "post-contents"}},
            "mpws": {"attrs": {"class": "entry-content"}},
            "para": {"div": {"class": "storyblock"}},
            "wast": {"div": {"class": "article-body"}},
            "tron": {"div": {"class": "inner-post-entry"}},
            "farg": {"div": {"class": "entry-content"}},
            "fuct": {"div": {"class": "col-xs-12 no-padding"}},
            "hoer": {"div": {"class": "penci-main-sticky-sidebar"}},
            "thon": {"div": {
                "class": "grid-ten large-grid-nine grid-last content-body content entry-content instapaper_body"}},
            "lees": {"div": {"class": "l_col_s_12 l_col_m_12 l_col_l_8 l_col_xl_8"}},
            "than": {"div": {"itemprop": "articleBody"}},
            "wral": {"attrs": {"class": "p402_premium"}},
            "obry": {"section": {"class": "entry-content clearfix"}},
            "swfo": {"div": {"itemprop": "articleBody"}},
            "snes": {"div": {"class": "post-body-card post-card card"}},
            "abbc": {"div": {"class": "article section"}},
            'afck': {"div": {"id": "main"}},
            # "poco": {"div": {"class": "story-text"}},
            # "faly": {"div": {"class": "col-8 main-content"}},
            # "alws": {"div": {"class": "td-ss-main-content"}},
            # "bove": {"div": {"id": "mvp-post-content"}},
            # "vees": {"div": {"class": "row"}},
            # 'thal': {"div": {"class": "post"}},
            # 'cry': {"div": {"class": "grid_9 prefix_2"}},
            # 'faan': {"div": {"class": "list-post"}},
            # 'fani': {"div": {"id": "primary"}},
            # 'vogo': {"div": {"class": "vo-page"}},  # need to change the code a bit
            # 'chct': {"div": {"id": "ob-read-more-selector"}},
            # 'zict': {"div": {"class": "entry-content"}},
            # 'thet': {"div": {"class": "entry-content"}},
            # "pomt": {"div": {"class": "article__text"}},
            # "pory": {"div":{"entry"}},
            # "pose": {"div": {"class": "article__text"}}
        }

    def get_claims_doc_path(self):
        with open("data/claim_docid_path_url.txt") as f:
            content = f.readlines()
        content = [re.sub( '\s+', ' ', x.rstrip()) for x in content]
        for line in content:
            parts = line.split(" ",4)
            claim_id = parts[0]
            docid = parts[1]
            path = parts[2]
            content_type = parts[3]
            url = parts[4]
            self.dict_info[claim_id] = {"doc":docid, "path":path,"content_type":content_type,"url":url, "full_text":""}

    def read_files(self):
        with open("full_text.txt", "w", encoding="utf8", errors="ignore") as file_out:
            for claim_id, info in self.dict_info.items():
                seed = claim_id.split("-")[0]
                if not os.path.isfile(info["path"]):
                    continue
                with open(info["path"], encoding="utf8", errors="ignore") as f:
                    content = f.read()
                if info["path"].endswith(".html"):
                    soup = BeautifulSoup(content, 'html.parser')
                # else:
                #     soup = BeautifulSoup(content, 'xml.parser')
                for key, value in self.dict_article_content[seed].items():
                    if key =="entry":
                        test = soup.find(value)
                        continue
                    elif key == "attrs":
                        # test = soup.find(attrs={"itemprop":"articleBody"})
                        test = soup.find(attrs=value)
                    elif key == "id":
                        test = soup.find(id=value)
                    else:
                        test = soup.find(key,value)
                    tokens = []
                    if test is not None:
                        tokens = self.tokenizer.tokenize(str(test).rstrip())
                    file_out.write(str(info["doc"]) + "::" + ' '.join(tokens) + "\n")

    # def write_outlinks_to_file(self):
    #     for seed, claims in self.dict_claim_outlinks.items():
    #         with open("seeds/outlinks/"+ str(seed) +".txt","w") as file_out:
    #             for claim_id, outlinks in claims.items():
    #                 for outlink in outlinks:
    #                     file_out.write(str(claim_id)+"\t"+str(outlink)+"\n")


if __name__ == '__main__':
    fulltext_parser = Parser("seeds/temp/")
    fulltext_parser.get_claims_doc_path()
    fulltext_parser.read_files()

