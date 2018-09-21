from selenium import webdriver
from scrappers.seeds.snopes import Snopes
from scrappers.seeds.truthorfiction import TruthOrFiction

class Crawling(object):
    def __init__(self, path):
        self.path = path
        self.dict_seeds = {}
        self.class_mappings = {"1":Snopes, "2":TruthOrFiction}

    #Function responsible to read the seeds that we are going to crawl
    def read_all_seeds_(self):
        with open(self.path) as f:
            content = f.readlines()
        content = [x.rstrip() for x in content]
        for line in content:
            #It should have the format SEED_ID URL
            parts = line.split(' ', 2)
            seed_id = parts[0]
            seed_url = parts[1]
            if seed_id not in self.dict_seeds:
                self.dict_seeds[seed_id] = seed_url

    def start(self):
        #Reading all seeds from file ..
        self.read_all_seeds_()

        #For each seed written in the file, call its respective scrapper
        for seed_id, seed_url in self.dict_seeds.items():
            self.cont_errors = 0
            self.seed_id = seed_id
            class_name = self.class_mappings[seed_id]
            scrapper = class_name(seed_id, seed_url)
            scrapper.start()