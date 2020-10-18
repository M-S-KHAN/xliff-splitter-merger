from lxml import etree
import glob
import pickle
import os
from merge import merge
from split import split


if __name__ == "__main__":

    action = "merge"

    option = None

    lines = None
    with open("paths.inf", "r") as file:
        lines = file.readlines()
    

    path = path1 = path2 = None

    for i, line in enumerate(lines):
        if i == 5:
            path = line.split("= ")[-1][:-1]
        elif i == 6:
            path1 = line.split("= ")[-1][:-1]
        elif i == 7:
            path2 = line.split("= ")[-1][:-1]
        

    while option != '3':

        print("""******** Please select your action: ********
        1. Merge
        2. Split
        3. Quit""")

        option = input()

        try:

            if "1" in option:
                
                # print("Please give path of your xliff files directory (i.e ./xliff_files): ")
                # path = input()

                merge(path)

            elif "2" in option:
                
                # print("Please give path of your merged file and pickle file directory (i.e ./merged): ")
                # path1 = input()
                # print("Please give path of your splitted files directory (i.e ./splitted): ")
                # path2 = input()

                split(path1, path2)

        except Exception as e:
            print(e)

        print('\n')
