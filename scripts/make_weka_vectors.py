# -*- coding: UTF-8 -*-

import logging
import codecs
from optparse import OptionParser
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')


def main():
    LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}
    
    usage = "usage: %prog data_file components_list [options]\n This script creates a vectors file\n based on the components list."
    parser = OptionParser(usage=usage, version="%prog 1.0")
    
    file_id = ""
    
    #Defining options   
    parser.add_option("-l", "--log", dest="level_name", default="info", help="choose the logging level: debug, info, warning, error, critical")
    parser.add_option("-r", "--rel", dest="relation", default="relation", help="choose the relation label for the arff file")
    parser.add_option("-c", "--class", dest="classfile", default="", help="File with input files name and their classes separated by tab.")
    parser.add_option("-b", action="store_true", dest="binary", help="Make binary vectors")
    parser.add_option("-i", action="store_true", dest="print_id", help="Print file id for each vector")
    parser.add_option("-n", "--nlimit", dest="limit", default="", help="limit the amount of vectors in the arff file")

    #Parsing arguments
    (options, args) = parser.parse_args()

    #Mandatory arguments    
    if len(args) != 2:
        parser.error("incorrect number of arguments")
     
    #####Setting up logs!
    level_name = options.level_name
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(level=level)

    relation = options.relation
    binary = options.binary
    print_id = options.print_id
    classfile = options.classfile

    if options.limit != "":
        limit = int(options.limit)
    else:
        limit = options.limit

    if classfile != "":
        classbool = True
    else:
        classbool = False
    
    ##### Mandatory arguments validation
    logging.info("---- MAKE_VECTORS ----")

    dataFilePath = args[0]
    logging.info(" data file       :  "+dataFilePath)
    try:
       with open(dataFilePath) as dataf: pass
    except IOError as e:
       parser.error(" data file       :  "+dataFilePath+" does not exist!")
	
    compFilePath = args[1]
    logging.info(" components list :  "+compFilePath)
    try:
       with open(compFilePath) as compf: pass
    except IOError as e:
       parser.error(" components list :  "+compFilePath+" does not exist!")

    classdict = {}
    classset = set()
    if classbool:
        logging.info(" Classfile :  "+classfile)
        try:
            with open(classfile) as f:
                for line in f:
                    line=line.strip()
                    fname,classname = line.split("\t")
                    classdict[fname] = classname
                    classset.add(classname)
        except IOError as e:
           parser.error(" classfile :  "+classfile+" does not exist!")        

    logging.info("Vectors amount limit: {0}".format(limit))

    vector = {}
    ## http://yuji.wordpress.com/2008/05/14/python-basics-of-python-dictionary-and-looping-through-them/

    #with open(compFilePath) as compf:
    with codecs.open(compFilePath, "r", "utf-8") as compf:
        logging.info("loading components file as a python dictionary...")
        for line in compf.readlines():
            line=line.strip()
	    if line is not '':
		if "\t" in line:
		    word = line.split('\t', 1)[0]
		    vector[word]=0  
		else:
		    vector[line]=0
		    #cols = line.split('\t')
		    #if len(cols) == 2:
		    #    vector[cols[2]]=0
		    #else
		    #    vector[cols[0]]=0

    now = datetime.datetime.now()
    print now.strftime("% ---- %Y-%m-%d %H:%M:%S ----")
    print "% data file :  "+dataFilePath
    print "% comp file :  "+compFilePath
    print "%"

    print "@RELATION {0}".format(relation)

    # print ATTRIBUTES ----------------------------------
    logging.info("printing ATTRIBUTES ...")
    
    # Attribute Id
    if print_id: print "@ATTRIBUTE id STRING"

    #for i,key in enumerate(vector.iterkeys()):
    #    print "@ATTRIBUTE "+str(i+1)+" NUMERIC"
    for key in vector.iterkeys():
        print "@ATTRIBUTE {0} NUMERIC".format(key)
    logging.info("Number of ATTRIBUTES: "+str(len(vector)))
    
    # Attirbute Id
    if print_id: print "@ATTRIBUTE id STRING"

    if classbool: print "@ATTRIBUTE class {1}{0}{2}".format(",".join(sorted(classset)),"{","}")

    # print DATA ----------------------------------------
    logging.info("printing DATA ...")
    num=0
    print "@DATA"
    #with open(dataFilePath) as dataf:
    with codecs.open(dataFilePath, "r", "utf-8") as dataf:
        for line in dataf.readlines():
            line=line.strip()
            if line is not '':
                cols = line.split('\t')	

                if file_id != cols[0]:
                    # print latest vector
                    if file_id != '':
                        print_vector(vector, file_id, print_id, classbool, classdict)
                        num += 1
                        logging.debug("Vectors in arff file: {0}\t limit: {1}".format(num, limit))
                        if num == limit:
                            break

		    # clean vector
                    for key in vector.iterkeys():
                        vector[key]=0
                    
                file_id = cols[0]
                #logging.warning("line:  "+line)
                if cols[1] in vector:
                    if binary:
                        vector[cols[1]]=1
                    else:
                        vector[cols[1]]=vector[cols[1]]+int(cols[2])
                #else:
                    #logging.warning(cols[1]+" is not in vector!")

    if num != limit:                                        	
        # print last vector
        print_vector(vector, file_id, print_id, classbool, classdict)
        num += 1
    
    logging.info("Number of DATA vectors: {0}".format(str(num)))

def print_vector(vector, file_id, print_id, classbool, classdict):
    if print_id: sys.stdout.write("'{0}',".format(file_id))
    sys.stdout.write(','.join(str(value) for value in vector.itervalues()))
    if print_id: sys.stdout.write("'{0}',".format(file_id))
    if classbool: sys.stdout.write(",{0}".format(classdict[file_id]))
    sys.stdout.write("\n")  

if __name__ == "__main__":
    main()
