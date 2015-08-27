'''
searching for the tenor of the Credo of London 29987
'''
from __future__ import print_function
from music21 import converter
#from music21 import corpus
from emmsap import files
import os

def searchOne(c):
    for p in c.parts:
        pf = p.flat.getElementsByClass('Note')
        lenPf = len(pf)
        for i in range(0, lenPf - 6):
            if pf[i].step != 'G':
                continue
            dnn = pf[i].diatonicNoteNum
            foundOne = False
            for j in range(1, 7):
                nj = pf[i+j]
                if nj.diatonicNoteNum != dnn - j:
                    break
                if j == 6:
                    foundOne = True
            if foundOne is True:
                startMeasure = pf[i].measureNumber
                p.measures(startMeasure - 1, startMeasure + 5).show()
            
        

for i,fn in enumerate(files.allFiles()):
    print(i, fn)
    try:
        fullFn = files.emmsapDir + os.sep + fn
        c = converter.parse(fullFn)
    except:
        print("----failed in parse")
    searchOne(c)