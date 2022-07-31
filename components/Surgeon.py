from weakref import ref
from util.utilities import reformat_name


class Surgeon:
    def __init__(self, name, ministry,npi=0):
        self.name = name
        self.ministry = ministry
        self.webmd_name = ''
        self.primary_practicename = ''
        self.npi = npi
        self.specialites = []
        self.webmd_link = ''
        self.practices = []

    def __repr__(self):
        print(f'name: {self.name}')

    def get_name(self):
        return self.name

    def compare_name(self, name):
        ascension = reformat_name(self.name)
        web_md = reformat_name(name)
        if ascension[0] == web_md[0] and ascension[-1] == web_md[-1]:
            return True
        return False
    
    def set_webmd_link(self,link):
        self.webmd_link = link

    def add_specialty(self,specialty):
        self.specialites.append(specialty)
    
    def add_practice(self,practice):
        self.practices.append(practice)

    def get_practices(self):
        return self.practices


