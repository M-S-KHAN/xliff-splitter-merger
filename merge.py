from lxml import etree
import glob
import pickle
import os

###############################################################################
#################          MERGING LOGIC GOES HERE            #################
###############################################################################


def merge(path):

    base_dir = path
    file_paths = []

    for path in glob.glob(f'{base_dir}/*'):
        file_paths.append(path)

    originals_dict = {}

    ##########        GETTING HEADER TEMPLATE FROM SINGLE FILE        ##########

    main_tree = etree.iterparse(file_paths[0], strip_cdata=False)

    for _, el in main_tree:
        _, _, el.tag = el.tag.rpartition('}')

    main_root = main_tree.root
    main_body = None


    ##########        REMOVING BODY ELEMENTS FROM TEMPLATE        ##########

    source_lang = None
    target_lang = None

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

    for i, file_path in enumerate(file_paths):

        original_dict_items = []

        tree = etree.iterparse(file_path, strip_cdata=False)

        for _, el in tree:
            _, _, el.tag = el.tag.rpartition('}')

        root = tree.root

        file_ref = root.find('file')
        original_temp = None
        for pair in file_ref.items():
            if pair[0] == 'original':
                original_temp = pair[1]
        # import pdb; pdb.set_trace()
        original_dict_items.append(file_path.split('\\')[-1])

        for element in root.iter():

            if element.tag == 'file':
                for pair in element.items():
                    if pair[0] == 'source-language' and not pair[1] == source_lang:
                        raise Exception(f"ERROR: Source Language Mismatch in file {file_path.split('/')[-1]}")
                    elif pair[0] == 'target-language' and not pair[1] == target_lang:
                        raise Exception(f"ERROR: Target Language Mismatch in file {file_path.split('/')[-1]}")

            if element.tag == 'body':
                original_dict_items.append(len(element.getchildren()))
                for body_element in element.getchildren():
                    main_body.append(body_element.__copy__())
                element.clear()

        original_dict_items.append(etree.tostring(root.__copy__()))

        originals_dict[i] = original_dict_items

    if not os.path.exists('merged'):
        os.makedirs('merged')

    with open("merged/merged.xliff", 'wb') as doc:
        doc.write(etree.tostring(main_root, method='xml', encoding='utf-8', standalone=False, xml_declaration=True))


    with open("merged/originals.pkl", 'wb') as doc:
        pickle.dump(originals_dict, doc)
