# -*- coding: UTF-8 -*-

import logging
from optparse import OptionParser
import sys
import codecs
import operator

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}
    
    usage = "usage: %prog <words_per_id> <ids_in_class> [options]\n ."
    parser = OptionParser(usage=usage, version="%prog 1.0")
        
    #Defining options   
    parser.add_option("-l", "--log", dest="level_name", default="info", help="choose the logging level: debug, info, warning, error, critical")

    #Parsing arguments
    (options, args) = parser.parse_args()

    #Mandatory arguments    
    if len(args) != 2:
        parser.error(" incorrect number of arguments")
     
    #####Setting up logs!
    level_name = options.level_name
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(level=level)
    
    logging.info(" ---- {0} ----".format(__file__))
    
    infile = args[0]
    logging.info(" Words_per_id file   :  "+infile)  
    try:
       with open(infile) as f: pass
    except IOError as e:
       parser.error(infile+" does not exist!")
       
    infile2 = args[1]
    logging.info(" Lis of ids in class :  "+infile2)  
    try:
       with open(infile2) as f: pass
    except IOError as e:
       parser.error(infile2+" does not exist!")
       

    class_ids = set()
    total_ids = set()
    
    logging.info(" Loading CLASS IDs into memory...")
    numClass=0
    with codecs.open(infile2, "r", "utf-8") as f:
        for line in f:
            line = line.strip()
            class_ids.add(line)

    numClass = float(len(class_ids))

    logging.info(" Processing words count file...")
    
    N11 = {} # Number of docs in the class with the term
    N01 = {} # Number of docs in the class without the term 
    N10 = {} # Number of docs outside the class with the term
    N00 = {} # Number of docs outside the class without the term
    WORDS = {} # Total list (dictionary) of words
        
    i=0
    with codecs.open(infile, "r", "utf-8") as f:
        for line in f:
            i += 1
            line = line.strip()
            (eid, word, freq) = line.split('\t')
            #print "{0} {1} {2}".format(eid, word, freq)
            
            WORDS[word] = 0
            
            if eid in class_ids:
                count(N11, word, freq)
            else:
                count(N10, word, freq)
            
            if eid not in total_ids:
                total_ids.add(eid)
                
            bar(i)
    sys.stderr.write("\n")
    
    numNotClass = float(len(total_ids))
    
    logging.debug(" numClass: {0} \t numNotClass: {1}".format(numClass, numNotClass))

    for word in WORDS.iterkeys():
        if word in N11:
            N01[word] = numClass - N11[word]
        else:
            N01[word] = numClass
        
    for word in WORDS.iterkeys():
        if word in N10:
            N00[word] = numNotClass - N10[word]
        else:
            N00[word] = numNotClass


    logging.info(" Calculating Xi2 for every term...")
    for word in WORDS.iterkeys():
        logging.debug("{0} \t {1} \t {2} \t {3} \t {4}".format( g(N11,word), g(N10,word), g(N01,word), g(N00,word), word ) )
        WORDS[word]=((g(N11,word) + g(N10,word) + g(N01,word) + g(N00,word)) * (g(N11,word)*g(N00,word) - g(N10,word)*g(N01,word))**2)/((g(N11,word) + g(N01,word))*(g(N11,word) + g(N10,word))*(g(N10,word) + g(N00,word))*(g(N01,word) + g(N00,word)))
        
    
    logging.info(" Creating the Xi2 Term ranking...")
    sorted_list = sorted(WORDS.iteritems(), key=operator.itemgetter(1), reverse=True)
    k = 0
    for i in sorted_list:
        if i[1] > 11:
            sys.stdout.write("{0}\t{1}\n".format(i[0], i[1]))
            k+=1
        else:
            break
        if k >= 15000:
            break

    
def g(dictionary, key):
    if key is not "" and key:
        if key in dictionary:
            return float(dictionary[key])
        else:
            return float(0)
    else:
        logging.debug(">> ERROR! << key and value cannot be blank!" )    

def count (dictionary,key,value):
    if key is not "" and key and value is not "":
        if key in dictionary:
            dictionary[key] = dictionary[key] + 1
        else:
            dictionary[key] = 1
    else:
        logging.debug(">> ERROR! << key and value cannot be blank!" )

def bar(i):
    if i%10000 == 0:
        sys.stderr.write(".")

if __name__ == "__main__":
    main()
