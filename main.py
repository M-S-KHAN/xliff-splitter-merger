from lxml import etree
import glob
import pickle
import os
from merge import merge
from split import split


if __name__ == "__main__":

    action = "merge"

    option = None

    while option != '3':

        print("""******** Please select your action: ********
        1. Merge
        2. Split
        3. Quit""")

        option = input()

        if "1" in option:
            print("Please give path of your xliff files directory (i.e ./xliff_files): ")
            path = input()
            merge(path)

        elif "2" in option:
            print("Please give path of your merged file and pickle file directory (i.e ./merged): ")
            path1 = input()
            print("Please give path of your splitted files directory (i.e ./splitted): ")
            path2 = input()
            split(path1, path2)
