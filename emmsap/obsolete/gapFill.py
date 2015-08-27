from music21 import corpus
from emmsap import files

def calculateAverageNote(s):
    sf = s.flat.pitches
    numsf = len(sf)
    if numsf == 0:
        return 0
    totsf = sum([p.ps for p in sf])        
    return round((totsf+0.0)/numsf)

def segmentByThrees(s):
    sf = s.flat.getElementsByClass('Note')
    sfLen = len(sf)
    tuples = []
    if sfLen < 3:
        return tuples 
    last2 = sf[0]
    last  = sf[1]
    last.lyric = ''
    last2.lyric = ''
    for i in range(2, sfLen):
        n = sf[i]
        n.lyric = ''
        if (n.ps == last.ps):
            continue
        t = (last2, last, n)
        tuples.append( t )
        last2 = last
        last = n
    return tuples

def filterListByRange(l, filterMin=5):
    tuples = []
    for t in l:
        if abs(t[0].ps - t[1].ps) >= filterMin:
            tuples.append(t)
    return tuples

def classifyTuples(l, avg):
    tuples = []
    totalGapFill = 0
    totalNonGapFill = 0
    totalRelevant = 0
    
    for t in l:
        if t[1].ps > t[0].ps:
            direction = 'ascending'
        else:
            direction = 'descending'
        
        if t[2].ps > t[1].ps:
            following = 'ascending'
        elif t[2].ps < t[1].ps:
            following = 'descending'
        else:
            following = 'same'
        
        if t[1].ps > avg + 1.1:
            position = 'above'
        elif t[1].ps < avg - 1.1:
            position = 'below'
        else:
            position = 'mid'
        
        if direction == following:
            gapfill = False
        elif following == 'same':
            gapfill = None
        else:
            gapfill = True

        if direction == 'ascending' and position != 'above':
            relevant = True
        elif direction == 'descending' and position != 'below':
            relevant = True
        else:
            relevant = False

        if relevant is True:
            t[1].lyric = str(gapfill)
            if gapfill is True:
                totalGapFill += 1
                totalRelevant += 1
            elif gapfill is False:
                totalNonGapFill += 1
                totalRelevant += 1
            # skip equal at end...
        
        richTuple = (t[0], t[1], t[2], direction, following, position, gapfill, relevant)
        tuples.append(richTuple)
    
    return (tuples, totalGapFill, totalNonGapFill, totalRelevant)

def runOne(s):
    avg = calculateAverageNote(s)
    ts = segmentByThrees(s)
    ts = filterListByRange(ts)
    return classifyTuples(ts, avg)
    
    
def allFiles():
    total = 2000
    
    stats = [[0,0,0] for i in range(30)]
    
    for s in files.FileIterator():
        for vNum in range(len(s.parts)):            
            sp = s.parts[vNum]
            unused_ts, gapFill, nonGapFill, relevant = runOne(sp)
            print (s.metadata.title, gapFill, nonGapFill, relevant)
            stats[vNum][0] += gapFill
            stats[vNum][1] += nonGapFill
            stats[vNum][2] += relevant
                
        total -= 1
        if total <= 0:
            break
        if total % 100 == 0:
            for i in range(10):
                print(stats[i], int(round((100*stats[i][0])/(stats[i][2]+.01))))

    return stats
    
if __name__ == '__main__':
    stats = allFiles()
    print("******")
    for i in range(10):
        print(stats[i], int(round((100*stats[i][0])/(stats[i][2]+.01))))
    #s = corpus.parse('luca/gloria')
    #sp = s.parts[2]
    #ts, totalGapFill, totalNonGapFill, totalRelevant = runOne(sp)
    #for t in ts:
    #    print(t)
    #print totalGapFill, totalNonGapFill, totalRelevant
    #sp.show()
    