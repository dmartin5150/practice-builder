class Practice:
    def __init__ (self,name, address,city,state,zip,phone,link):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.phone = phone
        self.website = link

    def __repr__ (self):
        return (f'Name: {self.name}, Address:{self.address}, City: {self.city}, state:{self.state} zip: {self.zip}, phone:{self.phone}, link: {self.website}')


