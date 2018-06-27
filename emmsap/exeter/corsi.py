import pathlib
import collections
import pickle
import re

from emmsap.indexTexts import regularizeText
from emmsap import mysqlEM

from music21.common import cleanpath
from music21.ext.more_itertools import windowed

def storePickle(obj, filename):
    filename = cleanpath('~/Documents/trecento/poetry/', returnPathlib=True) / (filename + '.p')
    with filename.open('wb') as fileout:
        pickle.dump(obj, fileout)
    return filename

def loadPickle(filename):
    filename = cleanpath('~/Documents/trecento/poetry/', returnPathlib=True) / (filename + '.p')
    with filename.open('rb') as filein:
        obj = pickle.load(filein)
    return obj

class FancySet(set):
    def __init__(self, *args):
        super().__init__(*args)
        self.words = None
        self.allWords = []
        self.fromDb = False

TextTuple = collections.namedtuple('TextTuple', 'id text textReg')

def main():
    allTexts = getTexts()
    for t in allTexts:
        print(t)
    storePickle(allTexts, 'allTexts')
    allTexts = loadPickle('allTexts')
    ngramsByPiece = index(allTexts)
    pairedPieces = {}
    for unused_ngram, files in ngramsByPiece.items():
        if files.fromDb != 'mixed':
            continue
        fileTuple = tuple(sorted(files))
        if fileTuple not in pairedPieces:
            pairedPieces[fileTuple] = []
        pairedPieces[fileTuple].append(files.allWords)

    for files, wordGroups in pairedPieces.items():
        numMatched = 0
        if len(wordGroups) > 2:
            for i in range(len(wordGroups) - 1):
                if wordGroups[i][0][1] == wordGroups[i + 1][0][0]:
                    numMatched += 1
        #if numMatched == len(wordGroups) - 1:
        #    continue
        
        wordNames = [' '.join(x[0]) for x in wordGroups]
        if len(wordGroups) > 3:
            print(len(wordGroups), '\t', files, '\t\t', wordNames)

#     for p, v in ngramsByPiece.items():
#         print(' '.join(p))
#         vv = ' / '.join([x for x in v])
#         print(vv)
#         print()
    
def index(allTexts):
    ngramsByPiece = {}

    windowLength = 3
    def getWordTuple2(wt):
        return tuple([x[:3] for x in wt])

    for piece in allTexts:
        if not piece.textReg.strip():
            continue
        textSplit = piece.textReg.split()
        for wordTuple in windowed(textSplit, windowLength):
            if None in wordTuple:
                continue
            wordTuple2 = getWordTuple2(wordTuple) 
            if wordTuple2 not in ngramsByPiece:
                f = FancySet()
                f.fromDb = False
                f.words = wordTuple
                ngramsByPiece[wordTuple2] = f
                
            ngramsByPiece[wordTuple2].add(piece.id)
            ngramsByPiece[wordTuple2].allWords.append(wordTuple)

    em = mysqlEM.EMMSAPMysql()
    q = """SELECT fn, textReg FROM texts WHERE language = 'it'"""
    em.cursor.execute(q)
     
    for fn, textReg in em.cursor:
        if fn == 'Poi_che_da_te_3vv_Lucca.xml':
            continue
        if not textReg:
            continue
        textSplit = textReg.split()
        for wordTuple in windowed(textSplit, windowLength):
            if None in wordTuple:
                continue
            wordTuple2 = getWordTuple2(wordTuple) 
            if wordTuple2 not in ngramsByPiece:
                f = FancySet()
                f.fromDb = True
                f.words = wordTuple
                ngramsByPiece[wordTuple2] = f
            elif ngramsByPiece[wordTuple2].fromDb is False:
                ngramsByPiece[wordTuple2].fromDb = 'mixed'
                 
            ngramsByPiece[wordTuple2].add(fn)
            ngramsByPiece[wordTuple2].allWords.append(wordTuple)
        
    ngramsByPiece = {x: y for (x, y) in ngramsByPiece.items() if len(y) >= 2}
    return ngramsByPiece

def getTexts():    
    indir = pathlib.Path('/users/cuthbert/Documents/trecento/poetry/')
    
    allTexts = []
    currentPoem = []
    currentAuthor = 'UNKNOWN'
    poemIndex = 0
    skipping = False

    def storePoem():
        allText = ' '.join(currentPoem)
        allText = allText.replace('\n', ' ')
        allText = allText.replace('\t', ' ')
        allText = allText.strip()
        if not allText:
            return
        allText = allText.replace('  ', ' ')
        allText = allText.replace('  ', ' ')
        textReg = regularizeText(allText, 'it')[0]
    
        allTexts.append(TextTuple(currentAuthor + ':' + str(poemIndex), allText, textReg))
    
    for fn in '01.txt', '02.txt', 'prud5.txt':
        archiveFn = indir / fn
    
        with archiveFn.open('r', encoding='utf-8') as f:
            allLines = f.readlines()
    
        for l in allLines:
            if l.startswith('AAA:'):
                currentAuthor = l[4:].strip().lower()
                poemIndex = 0
                continue
            
            if l.startswith('PPP:'):
                storePoem()
                currentPoem = []
                poemIndex += 1
                l = l[4:]
                skipping = False
    
            if l.startswith('XXX:'):
                storePoem()
                currentPoem = []
                skipping = True
        
            if not skipping:
                l = re.sub('^\d+\.?\s*', '', l)
                l = re.sub('^\s*I*V*I*X*\. ', '', l)
                currentPoem.append(l.strip())
                
    return allTexts

if __name__ == '__main__':
    main()
    