import pandas as pd


class Lab_Data:

    def __init__(self):
        self.labs = pd.read_csv('db/labs.csv').sort_values(by="number_women")
        self.faculties = ["ALL"] + list(self.labs["faculty"].unique())

    def sort_labs_by(self, faculty, gender):
        if faculty == 'ALL':
            faculty_labs = self.labs
        else:
            faculty_labs = (self.labs[self.labs['faculty'] == faculty]).sort_values(
                by="number_women")

        if gender == 'women':
            faculty_labs = faculty_labs.sort_values(by="number_women")
        elif gender == 'men':
            faculty_labs = faculty_labs.sort_values(by="number_men")
        else:
            faculty_labs["total"] = faculty_labs['number_women'] + \
                faculty_labs['number_men']
            faculty_labs = faculty_labs.sort_values(by='total')
        return faculty_labs
