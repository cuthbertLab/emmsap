import pathlib
import collections
import pickle

from bs4 import BeautifulSoup 

from emmsap.indexTexts import regularizeText
from emmsap import mysqlEM

from music21.common import cleanpath
from music21.ext.more_itertools import windowed

def storePickle(obj, filename):
    filename = cleanpath('~/git/emmsap/emmsap/exeter/', returnPathlib=True) / (filename + '.p')
    with filename.open('wb') as fileout:
        pickle.dump(obj, fileout)
    return filename

def loadPickle(filename):
    filename = cleanpath('~/git/emmsap/emmsap/exeter/', returnPathlib=True) / (filename + '.p')
    with filename.open('rb') as filein:
        obj = pickle.load(filein)
    return obj

class FancySet(set):
    def __init__(self, *args):
        super().__init__(*args)
        self.words = None
        self.allWords = []
        self.fromDb = False

TextTuple = collections.namedtuple('TextTuple', 'id title text textReg')

def main():
    # allTexts = getTexts()
    # storePickle(allTexts, 'allTexts')
    allTexts = loadPickle('allTexts')
    print(allTexts[-1])
    ngramsByPiece = index(allTexts)
    pairedPieces = {}
    for unused_ngram, files in ngramsByPiece.items():
        # if files.fromDb != 'mixed':
        #     continue
        fileTuple = tuple(sorted(files))
        if fileTuple not in pairedPieces:
            pairedPieces[fileTuple] = []
        pairedPieces[fileTuple].append(files.allWords)

    for files, wordGroups in pairedPieces.items():
        if len(wordGroups) < 2:
            continue
        
        numMatched = 0
        for i in range(len(wordGroups) - 1):
            if wordGroups[i][0][1] == wordGroups[i + 1][0][0]:
                numMatched += 1
        if numMatched == len(wordGroups) - 1:
            continue
        
        wordNames = [' '.join(x[0]) for x in wordGroups]
        hasSe = False
        for f in files:
            if '(Se' in f:
                hasSe = True
        if not hasSe:
            continue
        print(len(wordGroups), '\t', files, '\t\t', wordNames)

#     for p, v in ngramsByPiece.items():
#         print(' '.join(p))
#         vv = ' / '.join([x for x in v])
#         print(vv)
#         print()
    
def index(allTexts):
    ngramsByPiece = {}

    for piece in allTexts:
        if not piece.textReg.strip():
            continue
        textSplit = piece.textReg.split()
        for wordTuple in windowed(textSplit, 3):
            if None in wordTuple:
                continue
            wordTuple2 = wordTuple 
            # wordTuple2 = tuple([x[1:3] for x in wordTuple])
            if wordTuple2 not in ngramsByPiece:
                f = FancySet()
                f.fromDb = False
                f.words = wordTuple
                ngramsByPiece[wordTuple2] = f
                
            ngramsByPiece[wordTuple2].add(piece.title + ' (' + piece.id + ')')
            ngramsByPiece[wordTuple2].allWords.append(wordTuple)

    # All pieces in the DB with matches were already in Yolanda's db.
#     em = mysqlEM.EMMSAPMysql()
#     q = """SELECT fn, textReg FROM texts WHERE language != 'la' AND 
#             (fn not regexp 'patrem' AND fn not regexp 'credo' 
#              and fn not regexp 'gloria' and fn not regexp 'terra'
#              and fn not regexp 'sanctus' 
#              and fn not regexp 'agnus')"""
#     em.cursor.execute(q)
#     
#     for fn, textReg in em.cursor:
#         if not textReg:
#             continue
#         textSplit = textReg.split()
#         for wordTuple in windowed(textSplit, 7):
#             if None in wordTuple:
#                 continue
#             wordTuple = tuple(x.replace('//', '') for x in wordTuple)
# 
#             # wordTuple2 = wordTuple 
#             wordTuple2 = tuple([x[:2] for x in wordTuple])
#             if wordTuple2 not in ngramsByPiece:
#                 f = FancySet()
#                 f.fromDb = True
#                 f.words = wordTuple
#                 ngramsByPiece[wordTuple2] = f
#             elif ngramsByPiece[wordTuple2].fromDb is False:
#                 ngramsByPiece[wordTuple2].fromDb = 'mixed'
#                 
#             ngramsByPiece[wordTuple2].add(fn)
#             ngramsByPiece[wordTuple2].allWords.append(wordTuple)
        
    ngramsByPiece = {x: y for (x, y) in ngramsByPiece.items() if len(y) >= 2}
    return ngramsByPiece

def getTexts():    
    indir = pathlib.Path('/Users/cuthbert/Documents/misc/downloads/jechante.exeter.ac.uk')
    archivedir = indir / 'archive'
    
    allTexts = []
    for fn in archivedir.glob('text.xql-id*'):
        if '&' in fn.name:
            continue
        fileId = fn.name.replace('text.xql-id=', '').replace('.html', '')
        html = fn.read_text(encoding='utf-8', errors='replace')
        soup = BeautifulSoup(html, 'lxml')
        try:
            mainTitle = soup.findAll('div', {'class': 'mainTitle'})[0].text
        except IndexError:
            mainTitle = '[unknown]'
        lines = soup.findAll('td', {'class', 'lineText'})
        allText = ' '.join([l.text.strip() for l in lines])
        allText = allText.replace('\n', ' ')
        textReg = regularizeText(allText, 'fr')[0]
        print(fileId, mainTitle, '==>', textReg)
        allTexts.append(TextTuple(fileId, mainTitle, allText, textReg))
    
    return allTexts

if __name__ == '__main__':
    main()
    