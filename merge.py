from lxml import etree
import glob
import pickle
import os

###############################################################################
#################          MERGING LOGIC GOES HERE            #################
###############################################################################


def merge(path):

    print("Processing...")

    base_dir = path    #path of the directory which contains all the files that need to be merged 
    file_paths = []

    #It will take all the paths from base_dir and append them in file_path list
    for path in glob.glob(f'{base_dir}/*'):
        file_paths.append(path)

    originals_dict = {}

    ##########        GETTING HEADER TEMPLATE FROM SINGLE FILE        ##########

    main_tree = etree.iterparse(file_paths[0], strip_cdata=False)

    #This loop is used to remove all the originals or source name from the tags in the file
    for _, el in main_tree:
        _, _, el.tag = el.tag.rpartition('}')

    main_root = main_tree.root
    main_body = None


    ##########        REMOVING BODY ELEMENTS FROM TEMPLATE        ##########

    source_lang = None
    target_lang = None

    #This loop will iterate over all the root elements and will store source and target language and will also remove the body element so that we can have a header template for merged file
    for element in main_root.iter():

        if element.tag == 'file':
            for pair in element.items():
                if pair[0] == 'source-language':
                    source_lang = pair[1]
                elif pair[0] == 'target-language':
                    target_lang = pair[1]

        if element.tag == 'body':
            main_body = element
            element.clear()

    ##########        REMOVING BODY ELEMENTS FROM TEMPLATE        ##########

    #enumerate allows us to return multiple values 
    for i, file_path in enumerate(file_paths):

        original_dict_items = []  #It will contain the filename, count of body element, and root of file with body elements removed and will store this list in dictionary with a unique key

        tree = etree.iterparse(file_path, strip_cdata=False)

        for _, el in tree:
            _, _, el.tag = el.tag.rpartition('}')

        root = tree.root

        # file_ref = root.find('file')

        # original_temp = None
        # for pair in file_ref.items():
        #     if pair[0] == 'original':
        #         original_temp = pair[1]
        
        #Used to get the filename from the file path
        original_dict_items.append(file_path.split('\\')[-1])

        for element in root.iter():
            
            #Here we are checking if source language and target language of all the provided files are same. If not give exception
            if element.tag == 'file':
                for pair in element.items():
                    if pair[0] == 'source-language' and not pair[1] == source_lang:
                        raise Exception(f"ERROR: Source Language Mismatch in file {file_path.split('/')[-1]}")
                    elif pair[0] == 'target-language' and not pair[1] == target_lang:
                        raise Exception(f"ERROR: Target Language Mismatch in file {file_path.split('/')[-1]}")
            
            
            if element.tag == 'body':
                #Get the children count of 'body' element and append it in the list
                original_dict_items.append(len(element.getchildren()))
                for body_element in element.getchildren():
                    #Copy the body elements and then append them in main root body
                    main_body.append(body_element.__copy__())
                element.clear()

        original_dict_items.append(etree.tostring(root.__copy__())) #Will append the root in 'original_dict_items' with body elements removed

        originals_dict[i] = original_dict_items  #Will store the list(Defined above) in the dictionary

    #Creating the directory to contain the merged file
    if not os.path.exists('merged'):
        os.makedirs('merged')

    #Creating the merged file to store the general header and bodies of all the input files
    with open("merged/merged.xliff", 'wb') as doc:
        doc.write(etree.tostring(main_root, method='xml', encoding='utf-8', standalone=False, xml_declaration=True))

    #Storing the dictionary(originals_dict) in a pickle file
    #Pickle file is used to store the object as it is and then the object can be easily retrived later
    with open("merged/originals.pkl", 'wb') as doc:
        pickle.dump(originals_dict, doc)

    print("Done!")

