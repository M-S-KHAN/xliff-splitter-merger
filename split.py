from lxml import etree
import glob
import pickle
import os

###############################################################################
#################         SPLITTING LOGIC GOES HERE           #################
###############################################################################


def split(utils_path, split_dir):
    
    print("Processing...")

    pickle_path = f"{utils_path}/originals.pkl"   #Contains the pickle file path
    merged_file_path = f"{utils_path}/merged.xliff"    #Contains the path of merged file        
    split_files_base_directory = split_dir         #Contains the path in which split files will be stored

    file_to_read = open(pickle_path, "rb")

    loaded_dictionary = pickle.load(file_to_read)   #Loading the dictionary stored in pickle file
    main_tree = etree.iterparse(merged_file_path, strip_cdata=False)  #In order to save the Merged file main tree

    #This loop is used to remove all the originals or source name from the tags in the file
    for _, el in main_tree:
        _, _, el.tag = el.tag.rpartition('}')

    main_root = main_tree.root

    #This loop will iterate over all the elements of the root
    for element in main_root.iter():

        if element.tag == 'body':

            trans_object_iterator = element.iterchildren()  #Will contains the iterator of 'body' element
            loaded_dictionary_values = loaded_dictionary.values()  #Stores all the values in the dictionary

            for value in loaded_dictionary_values:

                file_name = value[0]
                object_count = value[1]         #Number of children of the 'body' element
                current_root = etree.fromstring(value[2])   #Contains the root with body elements removed 

                for _, el in current_root:
                    _, _, el.tag = el.tag.rpartition('}')

                #Will iterate over all the elements in current_root
                for current_element in current_root.iter():
                    if current_element.tag == 'body':
                        #This loop will iterate over all the body elements that we retrived from the dictionary
                        for _ in range(object_count):
                            next_trans_object = trans_object_iterator.__next__()    #This will contain the reference of the 'body' element children and then traverse them one by one using next function
                            current_element.append(next_trans_object.__copy__())    #This will append all trans units or children of 'body element' that were removed during merging

                #Will create a new file with same name to store the split files after processing
                with open(os.path.join(split_files_base_directory, file_name), 'wb') as doc:
                    doc.write(etree.tostring(current_root, method='xml', encoding='utf-8', standalone=False, xml_declaration=True))

    print("Done!")
