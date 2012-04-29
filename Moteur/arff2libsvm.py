# convert an ARFF training set to a libSVM on
# stores the correspondence between labels and indexes in a table

import string
import time
import os

def multiple_replace(char_string, chars_to_replace, replacing_char) :
    for elem in chars_to_replace :
        char_string = char_string.replace(elem, replacing_char)
    return char_string

def convert(arff_file_name, libsvm_file_name, verbose=True, class_name = 'emotion') :
    arff_file = open(arff_file_name, 'r')
    # get total size of file and go back to the beginning
    arff_file.seek(0, 2)
    arff_file_size = arff_file.tell()
    arff_file.seek(0)
    libsvm_file = open(libsvm_file_name, 'w')
    attributes = ""
    attributes_mapping = dict()
    classes = ""
    classes_mapping_index = 1
    classes_mapping = dict()
    attributes_list = []
    class_index = 0
    lines = arff_file.readlines()
    if verbose :
        print "Input file read."
    line_count = 0

    # parse header of arff file
    for line in lines :
        if line != "" :
            line = multiple_replace(line, [",", "{", "}"], " ")
            words = line.split()
            line_count += 1
            if line.startswith("@attribute") :
                attributes_list.append(words[1:])
            elif line.startswith("@data") :
                break
    for i in range(len(attributes_list)) :
        if attributes_list[i][0] == class_name :
            class_index = i
            for j in range(1, len(attributes_list[i])) :
                classes += str(classes_mapping_index) + " : " + attributes_list[i][j] + "\n"
                classes_mapping[classes_mapping_index] = attributes_list[i][j]
                classes_mapping_index += 1
        elif attributes_list[i][-1] == "numeric" :   # get the numerical features
            attributes += "#\t" + str(i) + " : " + attributes_list[i][0] + "\n"
            attributes_mapping[i] = attributes_list[i][0]
    if verbose :
        print "Parsing of header done."

    ##print classes_mapping
    ##print attributes_mapping
    ##print attributes
    ##print attributes_list
    ##print class_index
    classes_inverse_mapping = dict((k,v) for v,k in classes_mapping.items())
    line_to_write = ""

    # write mapping in another file
    line_to_write += "########################\n# Class labels mapping #\n########################\n\n"
    for elem in classes_mapping.items() :
        line_to_write += "#\t" + str(elem[0]) + " : " + str(elem[1]) + "\n"
    line_to_write += "\n######################\n# Attributes mapping #\n######################\n\n"
    line_to_write += attributes + "\n"
    #mapping_file_name = string.join(libsvm_file_name.split('\\')[:-1], '\\') + "\\mapping_" + libsvm_file_name.split('\\')[-1][:-6]
    mapping_file_name = os.path.dirname(libsvm_file_name) + os.path.sep + r'mapping_' + os.path.basename(libsvm_file_name).split('.')[0]
    mapping_file = open(mapping_file_name, 'w')
    mapping_file.write(line_to_write)
    mapping_file.close()

    count = 0
    index = 0
    for line in lines[line_count:] :
        if int(100. * float(count)/float(len(lines) - line_count)) % 10 == 0 and int(100. * float(count)/float(len(lines) - line_count)) != index :
            index = int(100. * float(count)/float(len(lines) - line_count))
            if verbose :
                print "Processing: " + str(index) + "% done."
        if not line.isspace() :
            words = line.strip().split(",")
            line_to_write = str(classes_inverse_mapping[words[class_index]]) + " "
            for i in attributes_mapping.keys() :
                line_to_write += str(i) + ":" + words[i] + " "
            line_to_write += "\n"
            libsvm_file.write(line_to_write)
        count += 1
    ##print line_to_write
        
    arff_file.close()
    libsvm_file.close()
    
    while not (arff_file.closed and libsvm_file.closed) :
        time.sleep(0.1)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3 :
        convert(str(sys.argv[1]), str(sys.argv[2]))
    else :
        print "Wrong number of arguments."
