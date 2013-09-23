#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    # http://stackoverflow.com/questions/6609895/efficiently-replace-bad-characters
    # http://csbruce.com/~csbruce/software/utf-8.html

    chars = {
        u'a' : 'a',
        u'b' : 'b',
        u'c' : 'c',
        u'd' : 'd',
        u'e' : 'e',
        u'f' : 'f',
        u'g' : 'g',
        u'h' : 'h',
        u'i' : 'i',
        u'j' : 'j',
        u'k' : 'k',
        u'l' : 'l',
        u'm' : 'm',
        u'n' : 'n',
        u'o' : 'o',
        u'p' : 'p',
        u'q' : 'q',
        u'r' : 'r',
        u's' : 's',
        u't' : 't',
        u'u' : 'u',
        u'v' : 'v',
        u'w' : 'w',
        u'x' : 'x',
        u'y' : 'y',
        u'z' : 'z'
    }

    charmays = {
        u'A' : 'A',
        u'B' : 'B',
        u'C' : 'C',
        u'D' : 'D',
        u'E' : 'E',
        u'F' : 'F',
        u'G' : 'G',
        u'H' : 'H',
        u'I' : 'I',
        u'J' : 'J',
        u'K' : 'K',
        u'L' : 'L',
        u'M' : 'M',
        u'N' : 'N',
        u'O' : 'O',
        u'P' : 'P',
        u'Q' : 'Q',
        u'R' : 'R',
        u'S' : 'S',
        u'T' : 'T',
        u'U' : 'U',
        u'V' : 'V',
        u'W' : 'W',
        u'X' : 'X',
        u'Y' : 'Y',
        u'Z' : 'Z'
    }

    tilde = {
        u'á' : 'á',
        u'é' : 'é',
        u'í' : 'í',
        u'ó' : 'ó',
        u'ú' : 'ú',
        u'à' : 'à',
        u'è' : 'è',
        u'ì' : 'ì',
        u'ò' : 'ò',
        u'ù' : 'ù',
        u'Á' : 'Á',
        u'É' : 'É',
        u'Í' : 'Í',
        u'Ó' : 'Ó',
        u'Ú' : 'Ú',
        u'À' : 'À',
        u'È' : 'È',
        u'Ì' : 'Ì',
        u'Ò' : 'Ò',
        u'Ù' : 'Ù',
        u'ç' : 'ç',
        u'Ç' : 'Ç',
        u'ñ' : 'ñ',
        u'Ñ' : 'Ñ'
    }

    punctuation = {
        u';' : ';',
        u',' : ',',
        u'.' : '.',
        u'!' : '!',
        u'"' : '"',
        u'·' : '·',
        u':' : ':',
        u'%' : '%',
        u'&' : '&',
        u'/' : '/',
        u'(' : '(',
        u')' : ')',
        u'=' : '=',
        u'?' : '?',
        u'¿' : '¿',
        u"'": "'",
        u'[' : '[',
        u']' : ']',
        u'*' : '*',
        u'{' : '}',
        u'-' : '-',
        u'_' : '_',
        u'<' : '<',
        u'>' : '>'
    }

    numbers = {
        u'0' : '0',
        u'1' : '1',
        u'2' : '2',
        u'3' : '3',
        u'4' : '4',
        u'5' : '5',
        u'6' : '6',
        u'7' : '7',
        u'8' : '8',
        u'9' : '9'
    }

    charspecial = {
        u'#' : '#',
        u'€' : '€',
        u'£' : '£',
        u'$' : '$',
        u'+' : '+',
        u'@' : '@',
        u'ü' : 'ü',
        u'Ü' : 'Ü',
        u'ï' : 'ï',
        u'Ï' : 'Ï'
    }

    i=0
    for utf8line in sys.stdin.readlines():
        utf8line=utf8line.rstrip()
        utf8line=utf8line.strip()
        i+=1
        unicodelist=list(utf8line.decode('utf-8'))
        cleanedlist = []
        for j, char in enumerate(unicodelist):
            if char in chars:
                cleanedlist.append(char)

            elif char == u' ':
                cleanedlist.append(char)

            elif char in charmays:
                cleanedlist.append(char)

            elif char in punctuation:
                cleanedlist.append(char)

            elif char in tilde:
                cleanedlist.append(char)

            elif char in numbers:
                cleanedlist.append(char)

            elif char in charspecial:
                cleanedlist.append(char)

            else:
                cleanedlist.append(u' ')
                sys.stderr.write(">> {0} << char at line {1} position {2} is not in list!\n".format(char, i, j) )

        #print utf8line
        print "".join(cleanedlist)

if __name__ == "__main__":
    main()
