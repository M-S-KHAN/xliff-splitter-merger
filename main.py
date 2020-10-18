from lxml import etree
import glob
import pickle
import os
from merge import merge
from split import split


if __name__ == "__main__":

    action = "merge"
    print("""******** Please select your action: ********
    1. Merge
    2. Split\n""")

    option = input()

    if "1" in option:
        merge()
    elif "2" in option:
        split()
