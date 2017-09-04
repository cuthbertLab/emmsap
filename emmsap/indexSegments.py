from emmsap import files
from emmsap import mysqlEM

from music21 import common
from music21 import search as searchBase
from music21.search import segment
import os

encodingsToAlgorithms = {
                      'diaSlower1': searchBase.translateStreamToString,
                      'DiaRhy2': searchBase.translateDiatonicStreamToString,
                      #'IntRhy': searchBase.translateIntervalsAndSpeed,
                      #'IntRhyJitter': searchBase.translateIntervalsAndSpeed,
                      'IntRhySmall': searchBase.translateIntervalsAndSpeed,
                      }

def findPieceIdsWithNoSegments(encodingType='diaSlower1'):
    '''
    finds all pieces in the database that do not have segments.  Returns their pieceIds
    '''
    em = mysqlEM.EMMSAPMysql()
    em.cursor.execute('SELECT id FROM pieces')
    allstuff = em.cursor.fetchall()
    allPieceIds = [x[0] for x in allstuff]
    query = 'SELECT * FROM segment WHERE piece_id = %s AND encodingType = %s LIMIT 1'
    missingPieceIds = []
    for thisPieceId in allPieceIds:
        em.cursor.execute(query, [thisPieceId, encodingType])
        hasSegments = False
        for dummy in em.cursor:
            hasSegments = True
        if hasSegments is False:
            missingPieceIds.append(thisPieceId)
    return missingPieceIds

def findFilenamesWithNoSegments(encodingType='diaSlower1'):
    '''
    uses findPieceIdsWithNoSegments to get filenames that have no segments
    '''
    noPieceIds = findPieceIdsWithNoSegments(encodingType)
    dbObj = mysqlEM.EMMSAPMysql()
    allFilenames = []
    for pid in noPieceIds:
        p = mysqlEM.Piece(pid, dbObj=dbObj)
        allFilenames.append(p.filename)
    #print(allFilenames)
    return allFilenames

def updateSegmentTable(encodingType='diaSlower1'):
    allMissingFilenames = findFilenamesWithNoSegments(encodingType)
    allMissingFilepaths = []
    for thisFn in allMissingFilenames:
        thisFp = files.emmsapDir + os.sep + thisFn
        allMissingFilepaths.append(thisFp)
    indexSegmentsAndStore(allMissingFilepaths, encodingType)

def indexSegmentsAndStore(allFilesWithPath=None, encodingType='diaSlower1'):
    '''
    Indexes the file paths given (or all files if none are given).
    '''
    if allFilesWithPath is None:
        allFilesWithPath = files.allFilesWithPath()[50:]
    indexedSegments = indexSegments(allFilesWithPath, encodingType)
    # indexedSegments is a dict of tuples (partNum, partInfo) where the key is the filename
    # partInfo is a dict of measureList, segmentList
    # each of those is a list of information
    em = mysqlEM.EMMSAPMysql()
    query = '''INSERT INTO segment 
        (piece_id, partId, segmentId, measureStart, measureEnd, encodingType, segmentData) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    for filename in indexedSegments:
        pieceObj = em.pieceByFilename(filename)
        pieceId = pieceObj.id
        for partNum, partInfo in enumerate(indexedSegments[filename]):
            numSegments = len(partInfo['measureList'])
            for segmentId in range(numSegments):
                measureStart = partInfo['measureList'][segmentId][0]
                measureEnd = partInfo['measureList'][segmentId][1]
                segmentData = partInfo['segmentList'][segmentId]
                em.cursor.execute(query, [pieceId, partNum, segmentId, measureStart, measureEnd, 
                                          encodingType, segmentData])
                #print(pieceId, filename, partNum, segmentId, measureStart, segmentData)
        em.cnx.commit()
        #addMeasureEndToSegments(pieceId, encodingType=encodingType)
    return indexedSegments

def addMeasureEndToSegments(pieceId=None, encodingType='DiaRhy2'):
    '''
    adds the value of the ending measure for each segment, assuming it's 50% more than the
    distance between the current start and the next start.  E.g., if segment 10 begins at m. 10
    and segment 11 begins at m. 16, we set the end of segment 10 to be 19 ((16-10) * 1.5); this
    takes into account overlap.

    if run without arguments, does it for all.  If run with a pieceId, just does that piece.

    SHOULD NOT BE NEEDED ANYMORE...
    '''
    em = mysqlEM.EMMSAPMysql()
    query = '''
        SELECT measureStart FROM segment 
        WHERE piece_id = %s AND partId = %s AND segmentId = %s AND encodingType = "%s"
    '''
    update = '''UPDATE segment SET measureEnd = %s WHERE id = %s'''
    if pieceId is None:
        em.cursor.execute('SELECT id, piece_id, partId, segmentId, measureStart FROM segment '
                          + 'WHERE encodingType = "%s"' % encodingType)
    else:
        em.cursor.execute('SELECT id, piece_id, partId, segmentId, measureStart FROM segment '
                          + 'WHERE piece_id = %s AND encodingType = "%s"' % (pieceId, encodingType))
    
    segmentData = em.cursor.fetchall()
    for row in segmentData:
        thisId = row[0]
        thisPieceId = row[1]
        thisPartId = row[2]
        thisSegmentId = row[3]
        
        thatSegmentId = thisSegmentId + 3
        #print row,
        executeQuery = query % (thisPieceId, thisPartId, thatSegmentId, encodingType)
        em.cursor.execute(executeQuery)
        endMeasure = None
        nextStartMeasure = None
        gotEm = em.cursor.fetchall()
        if gotEm:
            gotOne = gotEm[0]
            if gotOne is not None:
                nextStartMeasure = gotOne[0]
                endMeasure = nextStartMeasure
                #endMeasure = int((nextStartMeasure - row[4]) * 1.5) + row[4]
                print(endMeasure, update % (endMeasure, thisId))
                em.cursor.execute(update, [endMeasure, thisId])
                em.cnx.commit()


def _parseThenDump(fp):
    '''
    dummy parse function just for storing
    '''
    from music21 import converter
    try:
        converter.parse(fp)
    except Exception:
        pass

def preParseFiles(allFilesPath):
    common.runParallel(allFilesPath, _parseThenDump)
    
def indexSegments(allFilesPath, encodingType='DiaRhy2'):
    '''
    indexes the segments given a filepath and an algorithm.
    '''
    algorithm = encodingsToAlgorithms[encodingType]
    #preParseFiles(allFilesPath)
    indexedSegments = segment.indexScoreFilePaths(allFilesPath, segmentLengths=30, 
                                                  overlap=25, giveUpdates=True, 
                                                  algorithm=algorithm,
                                                  jitter=0,
                                                  failFast=False) # @UndefinedVariable
    print("done indexing")
    #fp = segment.saveScoreDict(indexedSegments)
    #print(indexedSegments)
    return indexedSegments

if __name__ == '__main__':
    pass
    #indexSegmentsAndStore(allFilesWithPath=None, encodingType='DiaRhy2')
    #updateSegmentTable('DiaRhy2')
#     for i in range(2500):
#         try:
#             addMeasureEndToSegments(pieceId=i, encodingType='IntRhy')
#         except Exception as e:
#             print(e)
    updateSegmentTable('IntRhySmall')
    
    #findFilenamesWithNoSegments()
    #findPieceIdsWithNoSegments()
    #addMeasureEndToSegments()
    #indexAndStore()