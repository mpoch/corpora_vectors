# -*- coding: UTF-8 -*-

import logging
import codecs
from optparse import OptionParser
import sys
import os.path
from os import walk
import operator
from math import log10

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}
    
    usage = "usage: %prog counter.py <input_input_folder> <output_input_folder> [options]\n ."
    parser = OptionParser(usage=usage, version="%prog 1.0")
        
    #Defining options   
    parser.add_option("-l", "--log", dest="level_name", default="info", help="choose the logging level: debug, info, warning, error, critical")    

    #Parsing arguments
    (options, args) = parser.parse_args()

    #Mandatory arguments    
    if len(args) != 1:
        parser.error("incorrect number of arguments")
     
    #####Setting up logs!
    level_name = options.level_name
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(level=level)
    
    ##### Mandatory arguments validation
    input_folder = args[0]
    if (os.path.isdir(input_folder)):
        logging.info(" input_folder :  "+input_folder)
    else:
        parser.error(" >> ERROR! << input_folder does not exist!   "+input_folder)

    output_folder = args[1]
    if (os.path.isdir(output_folder)):
        logging.info(" output_folder :  "+output_folder)
    else:
        parser.error(" >> ERROR! << output_folder does not exist!   "+output_folder)

    words={}
    
    output_byid = codecs.open('05-'+dirname+'-lemmas.byid', 'w')
    output_total = codecs.open('05-'+dirname+'-lemmas.total', 'w')
    #output_tfidf = codecs.open('05-'+dirname+'-tfidf', 'w')
    #output_col_tfidf = codecs.open('05-'+dirname+'-col-tfidf', 'w')
    #output_df = codecs.open('05-'+dirname+'-word-df', 'w')

    Nfiles=len([name for name in os.listdir(input_folder)])
    logging.info(" Number of documents: {0}".format(Nfiles))

    TF={}
    TFC={}
    appears={}

    for root, dirs, filenames in walk(input_folder):
        for f in filenames:
            #fileid=f.split('-')[0]
            fileid=f
            #fullpath=os.path.join(root, f)
            logging.debug("fullpath: {0}".format(fullpath))
            maxfreq="",""
            with codecs.open( fullpath, "r", "utf-8" ) as of:
                for line in of:
                    line=line.strip()
                    num,word = line.split()
                    if maxfreq[0]=="":
                        maxfreq=word,num
                    output_byid.write("{0}\t{1}\t{2}\n".format(fileid, word, num) )

                    # Term frequency = TF(ij) = freq of word i in document j
                    #TF[word,fileid] = float(num)/float(maxfreq[1])
                    TF[word,fileid] = log10( float(num) ) + 1
                    logging.debug("\tfileid: {0}\t\tnum:{1} \t\tmax: {2} \t\ttf: {3}".format(fileid, num, maxfreq[1], TF[word,fileid]))
                    
                    if word in words:
                        words[word] = words[word] + int(num)
                    else:
                        words[word] = int(num)

                    if word in appears:
                        appears[word] = appears[word] + 1
                    else:
                        appears[word] = 1


    output_byid.close()

    for key, value in TF.iteritems():
        word=key[0]
        TF[key] = value * log10(float(Nfiles) / float(appears[word]) )
        
        if word in TFC:
            TFC[word] = TFC[word] + TF[key]
        else:
            TFC[word] = TF[key]
        
    sorted_list = sorted(words.iteritems(), key=operator.itemgetter(1), reverse=True)
    logging.info(" total number of words:  "+str(len(sorted_list)))
    for i in sorted_list:
        output_total.write("{0}\tX\t{1}\n".format(i[1], i[0]))
    output_total.close()

    sorted_list = sorted(TF.iteritems(), key=operator.itemgetter(1), reverse=True)
    for i in sorted_list:
        output_tfidf.write("{0}\t{1}\t{2}\n".format(i[0][0], i[0][1], i[1]))
    output_tfidf.close()

    sorted_list = sorted(TFC.iteritems(), key=operator.itemgetter(1), reverse=True)
    logging.info(" total number of words (tfidf):  "+str(len(sorted_list)))
    for i in sorted_list:
        output_col_tfidf.write("{0}\t{1}\n".format(i[0], i[1]))
    output_col_tfidf.close()
    
    sorted_list = sorted(appears.iteritems())
    for i in sorted_list:
        output_df.write("{0}\t{1}\n".format(i[0], i[1]))
    output_df.close()
 
           
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False                


if __name__ == "__main__":
    main()
