from emmsap import knownSkips
from emmsap import mysqlEM

from music21.ext import more_itertools
from collections import defaultdict

minLength = 6
allTexts = defaultdict(list)
seenConnections = set()

def rejectFN(fn):
    fnl = fn.lower()
    for rejectName in ('gloria', 'credo', 'kyrie', 'et_in_terra', 'patrem', 'ite_missa_est',
                       'benedicamus_domino', 'sanctus', 'agnus', 'magnificat'):
        if rejectName in fnl:
            return True
    return False

textTreeSkip = [
    {810, 6, 1900, 2580}, # salve regina
    {70, 803, 2947, 3142}, # agnus not called agnus... (or gloria)
    {11, 918, 31}, # verbum caro
    {273, 14}, # verbum patris
    {2947, 1916, 2783}, # gloria not marked as such.
    {360, 2169, 2171}, # o rosa bella versions
    {2342, 276, 30}, # gaudeamus...
    {1105, 1107}, # ogelletto selvaggio
    {1112, 1127}, # si come al canto
    {152, 145}, # ita se n'era
    {217, 1334}, # la fiera testa
    {796, 877, 878}, # iste confessor
    {2276, 2277}, # iube domine
    {881, 907}, # Dulcis Jesu / Jesu Nostra
    {2354, 2355, 2342, 2351}, # gloria patri
    {2, 166}, # ave verum corpus
    {2747, 2710}, # credo not marked
    {1948, 142}, # ut re mi fa
    {68, 1596, 1598, 1399},# oci oci oci
    {1549, 2110}, # Grant pleysir...
    {1962, 1963}, # Machaut ii iii iu bi ii iii iv
    {738, 1557, 1437}, # se je ne suy
]


def main():
    em = mysqlEM.EMMSAPMysql()
    em.cursor.execute('SELECT filename, id FROM pieces')
    allFNMapping = em.cursor.fetchall()
    fnToId = {a: b for a, b in allFNMapping}
    
    em.cursor.execute('SELECT fn, textReg FROM texts ORDER BY fn')
    allPieces = em.cursor.fetchall()
    for fn, text in allPieces:
        if rejectFN(fn):
            continue
        doOnePiece(fn, text)
    
    for t in allTexts:
        if set(t).issuperset({'andare', 'uerto', 'chiuso'}):
            continue
        
        fns = allTexts[t]      
        if len(fns) < 2:
            continue
        fnstup = tuple(fns)
        if fnstup in seenConnections:
            pass
            # continue
        seenConnections.add(fnstup)
        
        fnsSet = set([fnToId[fn] for fn in fns])
        
        isKnownSkip = False
        for skipTuple in knownSkips.skipPieces:
            if set(skipTuple).issuperset(fnsSet):
                isKnownSkip = True
                break
        for skipSet in textTreeSkip:
            if skipSet.issuperset(fnsSet):
                isKnownSkip = True
                break                
            
            
        if isKnownSkip:
            continue
        
        
        print(fnsSet, allTexts[t], ' '.join(t))

iterRange = tuple(range(minLength))
        
def doOnePiece(fn, text):
    textSplit = text.split()
    for wordTuple in more_itertools.stagger(textSplit, offsets=iterRange):
        if fn in allTexts[wordTuple]:
            continue
        allTexts[wordTuple].append(fn)
            

if __name__ == '__main__':
    main()
