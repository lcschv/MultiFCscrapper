from pprint import pprint


class ClaimSchema(object):
    def __init__(self, string=None):
        if string is None:
            self.claim_id = None
            self.claim = None
            self.label = None
            self.claim_url = None
            self.reason = None
            self.categories = None
            self.speaker = None
            self.checker = None
            self.tags = None
            self.article_title = None
            self.publish_date = None
            self.claim_date = None
        else:
            parts = string.split("\t")
            assert (len(parts) == 12)
            self.claim_id = parts[0]
            self.claim = parts[1]
            self.label = parts[2]
            self.claim_url = parts[3]
            self.reason = parts[4]
            self.categories = parts[5]
            self.speaker = parts[6]
            self.checker = parts[7]
            self.tags = parts[8]
            self.article_title = parts[9]
            self.publish_date = parts[10]
            self.claim_date = parts[11]

    """Getters"""
    def get_claim_id(self):
        return self.claim_id

    def get_claim_url(self):
        return self.claim_url

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

    """Setters"""
    def set_id(self, claim_id):
        self.claim_id = claim_id

    def set_claim_url(self, claim_url):
        self.claim_url = claim_url

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
