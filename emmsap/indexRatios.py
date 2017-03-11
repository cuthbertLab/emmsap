from __future__ import print_function, division

#from music21.search import segment
from emmsap import mysqlEM
from functools import partial
from music21 import common

try:
    from Levenshtein import ratio as lvRatio # @UnresolvedImport
    difflib = None
except ImportError:
    lvRatio = None
    print("No Levenshtein C program found -- will be much slower; \n" 
          + "run pip3 install python-Levenshtein")
    import difflib # @UnusedImport

minSegmentLength = 15
segmentType = 'DiaRhy2' #'diaSlower1'

def adjustRatiosByFrequency(encodingType='IntRhy'):
    '''
    adjusts all ratios in the ratio table of encodingType according to how often the
    segment has a match, so that really common segments do not appear over and over and not great
    but extremely obscure matches are still found.
    
    See code for the formula.
    '''
    query = "SELECT segment1id, count(segment1id) as cs FROM ratios" + encodingType + \
        " GROUP BY segment1id"
    em = mysqlEM.EMMSAPMysql()
    em.cursor.execute(query)
    allSegments = [(x[0], x[1]) for x in em.cursor.fetchall()]
    numDone = 0
    for segId, segCount in allSegments:
        commitQuery = '''UPDATE ratios{encodingType} 
                         SET ratioAdjust = ratio - ((10000 - ratio)/10000 * 30*{segCount})
                         WHERE segment1id = {segId}'''.format(encodingType=encodingType, 
                                                         segCount=segCount,
                                                         segId=segId)
        #print(commitQuery)
        em.cursor.execute(commitQuery)
        if numDone % 1000 == 0:
            print('Done {numDone} of {total}'.format(numDone=numDone, total=len(allSegments)))
        numDone += 1
        
def updateRatioTableParallel(encodingType="DiaRhy2"):
    '''
    updates the ratio table in Parallel, 
    computing ratios for all segments (against all lower numbered segments)
    that do not have ratios computed
    '''
    missingSegments = findSegmentsWithNoRatios(encodingType)
    numMissingSegments = len(missingSegments)
    print(str(numMissingSegments) + " waiting to be indexed")
    #dbObj = mysqlEM.EMMSAPMysql()
    partialCommit = partial(commitRatioForOneSegment, encodingType=encodingType, searchDirection='down')
    common.runParallel(missingSegments, partialCommit, updateMultiply=3, updateFunction=True)

def updateRatioTable(encodingType="DiaRhy2"):
    '''
    updates the ratio table, computing ratios for all segments (against all lower numbered segments)
    that do not have ratios computed
    '''
    missingSegments = findSegmentsWithNoRatios(encodingType)
    numMissingSegments = len(missingSegments)
    print(str(numMissingSegments) + " waiting to be indexed")
    dbObj = mysqlEM.EMMSAPMysql()
    for i in range(numMissingSegments):
        segmentId = missingSegments[i]
        if i % 1 == 0:
            print("Done %d segments (of %d)" % (i, numMissingSegments))
        commitRatioForOneSegment(segmentId, dbObj, encodingType=encodingType)            

    

def findSegmentsWithNoRatios(encodingType='DiaRhy2'):
    '''
    returns a list of segmentIds which have no ratios in the ratio list 
    
    BUG: if updateRatioTable() was stopped in the middle then there may be segments 
    that have partial ratios.  yuk...
    Call deleteSparseSegmentRatios() to clean up.
    '''
    em = mysqlEM.EMMSAPMysql()
    query = "SELECT DISTINCT(segment1id) FROM ratios" + encodingType
    em.cursor.execute(query)
    allSegmentIdsWithRatios = [x[0] for x in em.cursor.fetchall()]
    print("Got " + str(len(allSegmentIdsWithRatios)) + " segment ids with ratios")
    query = 'SELECT id FROM segment WHERE LENGTH(segmentData) > %d AND encodingType = "%s"' % (
                                                            minSegmentLength, encodingType)
    em.cursor.execute(query)
    allSegmentIdsThatShouldHaveRatios = [x[0] for x in em.cursor.fetchall()]
    #print (113433 in allSegmentIdsThatShouldHaveRatios)
    print("Got " + str(len(allSegmentIdsThatShouldHaveRatios)) + 
                        " segment ids that should have ratios")
    missingSegmentIds = list(set(allSegmentIdsThatShouldHaveRatios) - set(allSegmentIdsWithRatios))
    return missingSegmentIds
    #print(missingSegmentIds)
    #print(getRatiosForSegment(missingSegmentIds[0]))

def deleteSparseSegmentRatios(maxSegments=30, 
                              minSegments=1, 
                              encodingType='DiaRhy2', 
                              runDelete=True):
    '''
    Clean up the ratios table after a failed commit.  Finds all pieces with number of ratios
    between minSegments (keep as 1) and maxSegments (30 is a conservative minimum that will
    not delete too much, but may still leave some incomplete; 200 will definitely get all
    of them, but may cause many complete segments to have to be reindexed).
    
    Remember that only ratios above minRatioToStore (default 5000) are stored, so it's
    possible for a segment to have been fully run but have few ratios in the ratio table.
    
    if runDelete is False, just show the number that would have been deleted, but don't delete them.
    '''
    em = mysqlEM.EMMSAPMysql()
    print("Finding sparse ratios.\nThis query can take 10-30 seconds...")
    query = "SELECT segment1id, count(segment1id) as cs FROM ratios" + encodingType + \
        " GROUP BY segment1id HAVING cs <= " + str(maxSegments) + " and cs >= " + str(minSegments)
    em.cursor.execute(query)
    allSegmentIdsThatShouldHaveMoreRatios = [(x[0],x[1]) for x in em.cursor.fetchall()]
    deleteRatiosQuery1 = '''DELETE FROM ratios''' + encodingType + ''' WHERE segment1id = %s'''
    deleteRatiosQuery2 = '''DELETE FROM ratios''' + encodingType + ''' WHERE segment2id = %s'''
    for sId, countSid in allSegmentIdsThatShouldHaveMoreRatios:
        print(sId, countSid)
        delQuerySub = deleteRatiosQuery1 % sId
        if runDelete is True:
            em.cursor.execute(delQuerySub)
        delQuerySub = deleteRatiosQuery2 % sId
        if runDelete is True:
            em.cursor.execute(delQuerySub)

    if runDelete is True:
        print("Deleted %d segments" % len(allSegmentIdsThatShouldHaveMoreRatios))
    else:
        print("Would have deleted %d segments" % len(allSegmentIdsThatShouldHaveMoreRatios))


def ratiosFromSegments(segment1, segment2):
    return ratiosFromSegmentData(segment1.segmentData, segment2.segmentData)
    
def ratiosFromSegmentData(segment1Data, segment2Data):
    if lvRatio is not None:
        return int(10000 * lvRatio(segment1Data, segment2Data))
    else:
        sm = difflib.SequenceMatcher(None, segment1Data, segment2Data)
        return int(10000 * sm.ratio())

_allSegmentData = {}

def storeAllSegmentData(encodingType):
    if encodingType in _allSegmentData:
        return _allSegmentData[encodingType]

    dbObj = mysqlEM.EMMSAPMysql()
    dbObj.cursor.execute('SELECT id, segmentData FROM segment WHERE encodingType = "%s"' % (encodingType))        
    sd = []
    print("Indexing segment data once...")
    for otherId, segData in dbObj.cursor:
        if len(segData) < minSegmentLength:
            pass
        tup = (otherId, segData)
        sd.append(tup) 
    print("Done indexing...")
    _allSegmentData[encodingType] = sd
    return _allSegmentData[encodingType]


def getRatiosForSegment(idOrSegment=1, dbObj=None, searchDirection='down', encodingType='DiaRhy2'):
    '''
    returns a list of tuples for a segment object (or segment id)
    which contain the id, otherId, and ratio * 10000 for every other segment
    that this matches.
    
    if searchDirection is 'up' then it ignores segments with lower numbers,
    since those were done earlier.  Use that for building the database.
    
    Use searchDirection = 'down' for adding to the database. Or 'both' is fastest.
    
    The full database looked like it was going to take 20GB, so now we're only storing
    those above 50% matches.

    '''
    minimumToStore = 5000
    if encodingType == 'IntRhySmall':
        minimumToStore = 6200
    
    if dbObj is None:
        dbObj = mysqlEM.EMMSAPMysql()
    if isinstance(idOrSegment, int):
        segmentObj = mysqlEM.Segment(idOrSegment, dbObj=dbObj)
    else:
        segmentObj = idOrSegment
    if len(segmentObj.segmentData) < minSegmentLength:
        return
    thisId = segmentObj.id
    thisSegmentData = segmentObj.segmentData
    #dl = segment.getDifflibOrPyLev(segmentObj.segmentData)

    storedRatios = []
    for otherId, otherSegmentData in storeAllSegmentData(encodingType):
        if len(otherSegmentData) < minSegmentLength:
            continue
        if searchDirection == 'up' and otherId <= thisId:
            continue
        if searchDirection == 'down' and otherId >= thisId:
            continue
        
        #dl.set_seq1(otherSegmentData)
        #ratioInt = int(10000 * dl.ratio())
        ratioInt = ratiosFromSegmentData(thisSegmentData, otherSegmentData)
        if ratioInt > minimumToStore:
            commitTuple1 = (thisId, otherId, ratioInt)
            commitTuple2 = (otherId, thisId, ratioInt)
            storedRatios.append(commitTuple1)
            storedRatios.append(commitTuple2)
        
    #import pprint
    #pprint.pprint(storedRatios)
    return storedRatios

def commitRatioForOneSegment(idOrSegment=1, dbObj=None, searchDirection='both', 
                             encodingType='DiaRhy2'):
    '''
    commit all the ratios from getRatiosForSegment into the database.
    '''
    if dbObj is None:
        dbObj = mysqlEM.EMMSAPMysql()
    storedRatios = getRatiosForSegment(idOrSegment, dbObj, searchDirection, encodingType)
    if not storedRatios:
        return 0 
    longQuery = ', '.join([str(ratioTuple) for ratioTuple in storedRatios])
    if longQuery == "":
        return 0
    commitQuery = '''INSERT INTO ratios%s (segment1id, segment2id, ratio) VALUES %s''' % (encodingType, longQuery)
    dbObj.cursor.execute(commitQuery)
    return len(storedRatios)

def commitRatiosForAllSegments(encodingType='DiaRhy2'):
    '''
    builds the database of ratios from segments.  Takes about 5-15 hours!
    '''
    dbObj = mysqlEM.EMMSAPMysql()
    dbObj.cursor.execute('SELECT id FROM segment WHERE encodingType = "%s" ORDER BY id' % encodingType)
    i = 0
    allRows = dbObj.cursor.fetchall()
    totalRows = len(allRows)
    for row in allRows:
        segmentId = row[0]
        if i % 25 == 0:
            print("Done %d segments (of %d ... it gets slower, sadly)" % (i, totalRows))
        i += 1
        commitRatioForOneSegment(segmentId, dbObj, encodingType=encodingType)            
    print("All done! :-)")

if __name__ == '__main__':
    pass
    #deleteSparseSegmentRatios(5, runDelete=True)
    updateRatioTableParallel('DiaRhy2')
    adjustRatiosByFrequency('DiaRhy2')
    #updateRatioTableParallel('IntRhy')
    #findSegmentsWithNoRatios()
    #commitRatioForOneSegment(100, searchDirection='down')
    #commitRatiosForAllSegments()
    #commitRatioForOneSegment(1)
    #rs = getRatiosForSegment(114664, searchDirection='down', encodingType="DiaRhy2")
    #for x in rs:
    #    if x[2] > 5000: print(x) 