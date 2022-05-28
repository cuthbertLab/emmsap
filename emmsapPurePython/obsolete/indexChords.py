from emmsap import files
from emmsap import mysqlEM

def findPieceIdsWithNoChords():
    '''
    finds all pieces in the database that do not have segments.  Returns their pieceIds
    '''
    em = mysqlEM.EMMSAPMysql()
    em.cursor.execute('SELECT id FROM pieces')
    allstuff = em.cursor.fetchall()
    allPieceIds = [x[0] for x in allstuff]
    query = 'SELECT pieceId,chordData FROM chords WHERE pieceId = %s LIMIT 1'
    missingPieceIds = []
    for thisPieceId in allPieceIds:
        em.cursor.execute(query, [thisPieceId])
        hasChords = False
        for dummy in em.cursor:
            if dummy[1] != "":
                hasChords = True
        if hasChords is False:
            missingPieceIds.append(thisPieceId)
    return sorted(missingPieceIds)

def findFilenamesWithNoChords():
    '''
    uses findPieceIdsWithNoChords to get filenames that have no chord information
    '''
    noPieceIds = findPieceIdsWithNoChords()
    dbObj = mysqlEM.EMMSAPMysql()
    allFilenames = []
    for pid in noPieceIds:
        p = mysqlEM.Piece(pid, dbObj=dbObj)
        allFilenames.append(p.filename)
    #print allFilenames
    return allFilenames

def updateChordTable():
    allMissingFilenames = findFilenamesWithNoChords()
    allMissingFilepaths = []
    for thisFn in allMissingFilenames:
        thisFp = thisFn
        allMissingFilepaths.append(thisFp)
    indexChordsAndStore(allMissingFilepaths)

def indexChordsAndStore(allFiles = None):
    '''
    Indexes the file paths given (or all files if none are given).
    '''
    if allFiles is None:
        allFiles = files.allFiles()[0:10]
    # indexedSegments is a dict of tuples (partNum, partInfo) where the key is the filename
    # partInfo is a dict of measureList, segmentList
    # each of those is a list of information
    em = mysqlEM.EMMSAPMysql()
    query = '''INSERT INTO chords 
        (pieceId, chordData) 
        VALUES (%s, %s)'''
    for filename in allFiles:
        pieceObj = em.pieceByFilename(filename)
        pieceId = pieceObj.id
        if pieceId == 0:
            continue
        else:
            chordData = getChordDataFromPiece(pieceObj)
            if chordData != "":
                em.cursor.execute(query, [pieceId, chordData])
        #print pieceId, filename, partNum, segmentId, measureStart, segmentData
    em.cnx.commit()

def getChordDataFromPiece(pieceObj = None):
    if pieceObj is None:
        pieceObj = mysqlEM.Piece(90)
    s = pieceObj.stream()
    if s is None:
        return ""
    #numVoices = pieceObj.numberOfVoices()
    chordified = s.chordify()
    chordDataList = []
    for c in chordified.recurse():
        if 'Chord' not in c.classes:
            continue
        c = c.sortAscending()
        numNotes = len(c.pitches)
        lowestMidi = c.pitches[0].midi
        allIntervals = []
        for i in range(1, numNotes):
            allIntervals.append(str(c.pitches[i].midi - lowestMidi))
        intervalStr = '-'.join(allIntervals)
        thisChord = str(numNotes) + "_" + str(lowestMidi) + "#" + intervalStr
        chordDataList.append(thisChord)
    chordData = ','.join(chordDataList)
    return chordData 


if __name__ == '__main__':
    pass
    #findFilenamesWithNoChords()
    #print getChordDataFromPiece()
    #indexChordsAndStore()
    #print sorted(findPieceIdsWithNoChords())
    updateChordTable()