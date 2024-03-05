import csv


class Participant:
    def__init__(self,age,industry,salary,currency)

def main():
    print("hello world")
    load_csv_file("survey.csv")


def load_csv_file(filename):
    rows = []
    with open(filename, "r" , eoncoding='iso-8859-1') as f:
        reader_obj = csv.