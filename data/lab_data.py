import pandas as pd


class LabData:

    def __init__(self):
        self.labs = pd.read_csv('data/labs.csv').fillna({'institute': 'None found'})
        self.labs['total'] = self.labs['number_women'] + self.labs["number_men"]
        self.faculties = ["ALL"] + list(self.labs["faculty"].unique())
        

    def filter_labs_by_faculty(self, faculty):
        if faculty == 'ALL':
            return self.labs
        else:
            return (self.labs[self.labs['faculty'] == faculty])

    def sort_labs_by(self, faculty, gender):
        faculty_labs = self.filter_labs_by_faculty(faculty)

        if gender == 'women':
            return faculty_labs.sort_values(by=["number_women", "acronym"])
        elif gender == 'men':
            return faculty_labs.sort_values(by=["number_men", "acronym"])
        else:
            return faculty_labs.sort_values(by=['total', "acronym"])

    def get_random_lab(self):
        return self.labs.sample()
