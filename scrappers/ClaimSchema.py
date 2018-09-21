from pprint import pprint


class ClaimSchema(object):
    def __init__(self):
        self.claim_id = None
        self.claim = None
        self.label = None
        self.reason = None
        self.categories = None
        self.checker = None
        self.tags = None
        self.article_title = None

    """Getters"""
    def get_claim_id(self):
        return self.claim_id

    def get_claim(self):
        return self.claim

    def get_label(self):
        return self.label

    def get_reason(self):
        return self.reason

    def get_categories(self):
        return self.categories

    def get_checker(self):
        return self.checker

    def get_tags(self):
        return self.tags

    def get_article_title(self):
        return self.article_title

    """Setters"""
    def set_id(self, claim_id):
        self.claim_id = claim_id

    def set_claim(self, claim):
        self.claim = claim

    def set_label(self, label):
        self.label = label

    def set_reason(self, reason):
        self.reason = reason

    def set_categories(self, categories):
        self.categories = categories

    def set_checker(self, checker):
        self.checker = checker

    def set_tags(self, tags):
        self.tags = tags

    def set_article_title(self, article_title):
        self.article_title = article_title

    def pretty_print(self):
        pprint(vars(self))
