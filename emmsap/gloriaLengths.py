
from __future__ import division

from emmsap import files
#from music21 import common
from music21 import expressions
from music21 import converter
from music21 import interval
from music21 import metadata
from music21 import stream
from music21.search import lyrics

import re
quiTollis = re.compile('qui t.*?rere nobis', re.IGNORECASE)
wholeGloria = re.compile('et in terra.*dei patris', re.IGNORECASE)
etToGra = re.compile('et in t.*gra', re.IGNORECASE)
laudamus = re.compile('laudamus.*?gratias', re.IGNORECASE)
quonium = re.compile('quoniam.*?tissimus', re.IGNORECASE)
quiSedes = re.compile('qui sedes.*?patris', re.IGNORECASE)


#credos
etInSpiritu = re.compile('et in spir.*hrist', re.IGNORECASE)
deumVero = re.compile('deum de.*vero', re.IGNORECASE)

firstSanctus = re.compile('sanctus\W+san', re.IGNORECASE)

searchRE = firstSanctus
searchTolerance = 3

def main():
    glor = sanctus()
    allParts = {}
    for g in glor:
        go = converter.parse(g)
        gShort = g.split('/')[-1][0:-4]
        for i, p in enumerate(go.parts):
            ls = lyrics.LyricSearcher(p)
            matches = ls.search(searchRE)
            if len(matches) > 0:
                m = matches[0]
                ts = m.els[0].getContextByClass('TimeSignature')

#                 intvStart = interval.Interval(m.els[0], m.els[1])
#                 if intvStart.generic.directed != 2:
#                     continue
#                 intvStart = interval.Interval(m.els[1], m.els[2])
#                 if intvStart.generic.directed != 3:
#                     continue

                
                passageApproxLength = searchTolerance * int((m.mEnd - m.mStart + 1)/searchTolerance)
#                if passageApproxLength < 14 or passageApproxLength > 17:
#                    continue
                pieceKey = ts.ratioString + "-" + str(passageApproxLength)
                if pieceKey not in allParts:
                    s = stream.Score()
                    s.metadata = metadata.Metadata()
                    s.metadata.title = pieceKey + " " + searchRE.pattern
                    s.numberOfPieces = 0
                    allParts[pieceKey] = s
                s = allParts[pieceKey]
                print(gShort, m.mStart, '-', m.mEnd, pieceKey)
                for i, pAgain in enumerate(go.parts):
                    pCopy = pAgain.measures(m.mStart, m.mEnd)
                    if i == 0:
                        s.numberOfPieces += 1
                        pCopy.getElementsByClass('Measure')[0].insert(0, expressions.TextExpression(gShort))
                    if len(pCopy.flat.notes) > 0:
                        s.insert(0, pCopy)
                if len(s.parts) > 16:
                    s.show()
                    del(allParts[pieceKey])
                break
    for k in allParts:
        s = allParts[k]
        if s.numberOfPieces > 0: #and s.parts[0].flat.notes[0].getContextByClass('TimeSignature').ratioString == '3/4':
            s.show()

def sanctus():
    fi = files.allFilesWithPath()
    sanctus = []
    for f in fi:
        if 'Sanctus'.lower() not in f.lower():
            continue
        sanctus.append(f)
    return sanctus

def glorias():
    fi = files.allFilesWithPath()
    glorias = []
    notGlorias = []
    for f in fi:
        if 'Gloria'.lower() not in f.lower() and 'Terra'.lower() not in f.lower():
            notGlorias.append(f)
            continue
        if 'Summa_Tua_Gloria' in f:
            notGlorias.append(f)
            continue
        glorias.append(f)
    return glorias
    
def credos():
    fi = files.allFilesWithPath()
    credos = []
    for f in fi:
        if 'Credo'.lower() not in f.lower() and 'Patrem'.lower() not in f.lower():
            continue
        if 'Non_Credo_Donna'.lower() in f:
            continue
        credos.append(f)
    return credos


    
if __name__ == '__main__':
    main()