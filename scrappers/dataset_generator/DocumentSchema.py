from pprint import pprint
class DocumentSchema(object):
    def __init__(self):
        self.claim_id = None
        self.claim = None
        self.label = None
        self.url = None
        self.reason = None
        self.categories = None
        self.speaker = None
        self.checker = None
        self.tags = None
        self.article_title = None
        self.publish_date = None
        self.claim_date = None

        self.content_type = None
        self.isClaim = None
        self.doc_id = None
        self.full_article_text = None
        self.document_length = None
        self.list_inlinks = None
        self.list_outlinks = None
        self.label_scale = None
        self.number_entities = None
        self.list_entities = None
        self.content = None

    """Getters"""
    def get_content_type(self):
        return self.content_type
    def get_isClaim(self):
        return self.isClaim
    def get_list_inlinks(self):
        return self.list_inlinks
    def get_list_outlinks(self):
        return self.list_outlinks

    def get_doc_id(self):
        return self.doc_id
    def get_full_article_text(self):
        return self.full_article_text
    def get_document_length(self):
        return self.document_length
    def get_content(self):
        return self.content
    def get_label_scale(self):
        return self.label_scale
    def get_number_entities(self):
        return self.number_entities
    def get_list_entities(self):
        return self.list_entities


    """"Getters claim"""
    def get_claim_id(self):
        return self.claim_id

    def get_claim_url(self):
        return self.url

    def get_claim(self):
        return self.claim

    def get_label(self):
        return self.label

    def get_reason(self):
        return self.reason

    def get_categories(self):
        return self.categories

    def get_speaker(self):
        return self.speaker

    def get_checker(self):
        return self.checker

    def get_tags(self):
        return self.tags

    def get_article_title(self):
        return self.article_title

    def get_publish_date(self):
        return self.publish_date

    def get_claim_date(self):
        return self.claim_date

    """"Setters Document"""
    def set_content_type(self, content_type):
        self.content_type = content_type
    def set_isClaim(self, isClaim):
        self.isClaim = isClaim
    def set_list_inlinks(self, list_inlinks):
        self.list_inlinks = list_inlinks
    def set_list_outlinks(self, list_outlinks):
        self.list_outlinks = list_outlinks
    def set_doc_id(self, doc_id):
        self.doc_id = doc_id
    def set_full_article_text(self, full_article_text):
        self.full_article_text = full_article_text
    def set_document_length(self, document_length):
        self.document_length = document_length
    def set_content(self, content):
        self.content = content

    def set_label_scale(self, label_scale):
        self.label_scale = label_scale

    def set_number_entities(self, number_entities):
        self.number_entities = number_entities

    def set_list_entities(self, list_entities):
        self.list_entities = list_entities

    """Setters Claim"""
    def set_id(self, claim_id):
        self.claim_id = claim_id

    def set_url(self, url):
        self.url = url

    def set_claim(self, claim):
        self.claim = claim

    def set_label(self, label):
        self.label = label

    def set_reason(self, reason):
        self.reason = reason

    def set_categories(self, categories):
        self.categories = categories

    def set_speaker(self, speaker):
        self.speaker = speaker

    def set_checker(self, checker):
        self.checker = checker

    def set_tags(self, tags):
        self.tags = tags

    def set_article_title(self, article_title):
        self.article_title = article_title

    def set_publish_date(self, publish_date):
        self.publish_date = publish_date

    def set_claim_date(self, claim_date):
        self.claim_date = claim_date


    def pretty_print(self):
        pprint(vars(self))
