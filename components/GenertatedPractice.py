import pandas as pd

class Generated_Practice:
    def __init__ (self,name='Practice',full_data=pd.DataFrame(), old_clinics =[], new_clinics=[], old_surgeons=[], new_surgeons=[]):
        self.name = name
        self.full_data = full_data
        self.old_clinics = old_clinics
        self.new_clinics = new_clinics
        self.old_surgeons = old_surgeons
        self.new_surgeons = new_surgeons

    def no_new_clinics(self):
        return len(self.old_clinics) == len(self.new_clinics)
    
    def no_new_surgeons(self):
        return len(self.old_surgeons) == len(self.new_surgeons)

    def get_practice_surgeons(self):
        # print('in get practice surgeons')
        self.old_surgeons = self.new_surgeons
        self.new_surgeons = (self.full_data[self.full_data['Clinic_Name'].isin(self.new_clinics)]['Ascension_Name']).unique().tolist()
        # print('Num old surgeons: ', self.get_number_old_surgeons())
        # print('Num new surgeons ', self.get_number_new_surgeons())
        # # print('old_surgeons: ', self.old_surgeons)
        # print('new_surgeons: ', self.new_surgeons)
        return self.no_new_surgeons()

    def get_surgeon_clinics(self):
        self.old_clinics = self.new_clinics
        self.new_clinics = self.full_data[self.full_data['Ascension_Name'].isin(self.new_surgeons)]['Clinic_Name'].unique().tolist()

        # print('Num old clincs: ', self.get_number_old_clinics())
        # print('Num new clinics: ', self.get_number_new_clinics())
        # print('old_clinics: ', self.old_clinics)
        # print('new_clinics: ', self.new_clinics)
        return self.no_new_clinics()


    def get_number_old_clinics(self):
        return len(self.old_clinics)

    def get_number_new_clinics(self):
        return len(self.new_clinics)

    def get_number_old_surgeons(self):
        return len(self.old_surgeons)

    def get_number_new_surgeons(self):
        return len(self.new_surgeons)

    def reset_data(self):
        self.old_clinics = []
        self.new_clinics = []
        self.old_surgeons = []
        self.new_surgeons = []    


    def generate_practice_data(self,initial_clinic):
        self.reset_data()
        self.new_clinics.append(initial_clinic)
        no_additional_clinics = False
        no_additional_surgeons = False
        i = 0
        # print('in generate data')
        # print ((no_additional_clinics or no_additional_surgeons))
        while not no_additional_clinics and  not no_additional_surgeons:
            # print ('in loop ', i)
            if i > 20:
                print("Unable to fully generate practice data")
                break
            no_additional_surgeons = self.get_practice_surgeons()
            no_additional_clinics = self.get_surgeon_clinics()
            i = i + 1