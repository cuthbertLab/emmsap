'''
find one commonplace but particularly clear passage on Oxford 56, f. 80v
'''
from __future__ import print_function

from music21 import converter
#from music21 import corpus
from emmsap import files
import os

def searchOne(fn, sMeasures, maxErrors = 0):
    fullFn = files.emmsapDir + os.sep + fn
    c = converter.parse(fullFn)
    for partNum in range(len(c.parts)):
        c1 = c.parts[partNum]
    
        searchMeasureLen = len(sMeasures)
        mList = c1.getElementsByClass('Measure')
        lastMToSearch = len(mList) - searchMeasureLen + 1
        for i in range(lastMToSearch):
            transposeOffset = None
            totalErrors = 0
            for j in range(searchMeasureLen):
                thisM = mList[i+j].getElementsByClass('Note') # no chords...
                searchM = sMeasures[j].getElementsByClass('Note')
                #if len(thisM) != len(searchM):
                #    break
                if thisM.duration.quarterLength != searchM.duration.quarterLength:
                    break
                if transposeOffset is None:
                    transposeOffset = thisM[0].diatonicNoteNum - searchM[0].diatonicNoteNum
                allSet = True
                for k in range(max(len(thisM), len(searchM))):
                    try:
                        thisN = thisM[k]
                        searchN = searchM[k]
                    except:
                        totalErrors += 1
                        if totalErrors > maxErrors:
                            allSet = False
                            break
                        else:
                            continue
                        
                    if thisN.duration.quarterLength != searchN.duration.quarterLength:
                        totalErrors += 1
                        if totalErrors > maxErrors:
                            allSet = False
                            break
                    elif thisN.diatonicNoteNum - transposeOffset != searchN.diatonicNoteNum:
                        totalErrors += 1
                        if totalErrors > maxErrors:
                            allSet = False
                            break
                if allSet is False:
                    break
                if j == searchMeasureLen - 1:
                    print("**** Found a match for %s in part %d, measure %d, with %d errors" % (fn, partNum, i+1, totalErrors))
                    mStart = max(i, 0)
                    mEnd = min(i+10, len(mList))
                    c.measures(mStart, mEnd).show()
                
tn = 'tinynotation:6/8 g4 f8 e4 d8 f2. d4. f4.'
#tn = 'tinynotation:6/8 d2. e8 d4 B8 G4 G8 B4 d4 d8'
s = converter.parse(tn).makeMeasures()
sMeasures = s.getElementsByClass('Measure') # eliminate metadata

maxErrors = 2
for fn in files.allFiles():
    print(fn)
    try:
        searchOne(fn, sMeasures, maxErrors)
    except:
        print("----failed in parse")