from lxml import etree
import glob
import pickle
import os

###############################################################################
#################         SPLITTING LOGIC GOES HERE           #################
###############################################################################


def split(utils_path, split_dir):
    
    pickle_path = f"{utils_path}/originals.pkl"
    merged_file_path = f"{utils_path}/merged.xliff"
    split_files_base_directory = split_dir

    file_to_read = open(pickle_path, "rb")

    loaded_dictionary = pickle.load(file_to_read)
    main_tree = etree.iterparse(merged_file_path, strip_cdata=False)

    for _, el in main_tree:
        _, _, el.tag = el.tag.rpartition('}')

    main_root = main_tree.root

    for element in main_root.iter():

        if element.tag == 'body':

            trans_object_iterator = element.iterchildren()
            loaded_dictionary_values = loaded_dictionary.values()

            for value in loaded_dictionary_values:

                file_name = value[0]
                object_count = value[1]
                current_root = etree.fromstring(value[2])

                for _, el in current_root:
                    _, _, el.tag = el.tag.rpartition('}')

                for current_element in current_root.iter():
                    if current_element.tag == 'body':
                        for j in range(object_count):
                            next_trans_object = trans_object_iterator.__next__()
                            current_element.append(next_trans_object.__copy__())

                with open(os.path.join(split_files_base_directory, file_name), 'wb') as doc:
                    doc.write(etree.tostring(current_root, method='xml', encoding='utf-8', standalone=False, xml_declaration=True))
