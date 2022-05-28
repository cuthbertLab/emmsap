import pickle

from emmsap import mysqlEM
from emmsap.knownSkips import skipFilenames
from music21.ext.more_itertools import windowed
from music21.common import cleanpath

def storePickle(obj, filename):
    filename = cleanpath('~/git/emmsap/emmsap/', returnPathlib=True) / (filename + '.p')
    with filename.open('wb') as fileout:
        pickle.dump(obj, fileout)
    return filename

def loadPickle(filename):
    filename = cleanpath('~/git/emmsap/emmsap/', returnPathlib=True) / (filename + '.p')
    with filename.open('rb') as filein:
        obj = pickle.load(filein)
    return obj

class FancySet(set):
    def __init__(self, *args):
        super().__init__(*args)
        self.words = None
        self.allWords = []

def save():
    em = mysqlEM.EMMSAPMysql()
    q = """SELECT fn, textReg FROM texts WHERE language != 'la' AND 
            (fn not regexp 'patrem' AND fn not regexp 'credo' 
             and fn not regexp 'gloria' and fn not regexp 'terra'
             and fn not regexp 'sanctus' 
             and fn not regexp 'agnus')"""
    em.cursor.execute(q)
    ngramsByPiece = {}
    
    for fn, textReg in em.cursor:
        if not textReg:
            continue
        textSplit = textReg.split()
        for wordTuple in windowed(textSplit, 1):
            if None in wordTuple:
                continue
            
            wordTuple = tuple(x.replace('//', '') for x in wordTuple)
#             skipIt = False
#             for x in wordTuple:
#                 if len(x) < 4:
#                     skipIt = True
#             if skipIt:
#                 continue
            
            wordTuple2 = wordTuple # tuple([x[1:] for x in wordTuple])
            if wordTuple2 not in ngramsByPiece:
                f = FancySet()
                f.words = wordTuple
                ngramsByPiece[wordTuple2] = f
                
            ngramsByPiece[wordTuple2].add(fn)
            ngramsByPiece[wordTuple2].allWords.append(wordTuple)
                
    ngramsByPiece = {x: y for (x, y) in ngramsByPiece.items() if len(y) == 2}
    
    storePickle(ngramsByPiece, 'fileNGrams')

def load():
    ngramsByPiece = loadPickle('fileNGrams')
    pairedPieces = {}
    for ngram, files in ngramsByPiece.items():
        fileTuple = tuple(sorted(files))
        if fileTuple not in pairedPieces:
            pairedPieces[fileTuple] = []
        pairedPieces[fileTuple].append(files.allWords)
    
    for files, wordGroups in pairedPieces.items():
        skipIt = False
        for x in skipFilenames:
            numFound = 0
            for f in files:
                if f in x:
                    numFound += 1
                    
            if numFound == len(files):
                skipIt = True
                break
        if skipIt:
            continue
        if len(wordGroups) >= 10 or len(wordGroups) < 4:
            continue
        print(len(wordGroups), '\t', files, '\t\t', wordGroups)

def main():
    save()
    load()
    
if __name__ == '__main__':
    main()