# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
import csv
from music21.search import segment
from music21 import search as searchBase
from emmsap import files


def indexAndCache(filesToCache = 'All'):
    '''
    Indexes and caches all the files and returns
    '''
    if filesToCache == 'all':
        allFiles = files.allFilesWithPath()
    allFiles = allFiles
    indexedSegments = segment.indexScoreFilePaths(allFiles, giveUpdates = True,
                                                  algorithm=searchBase.translateDiatonicStreamToString) # @UndefinedVariable
    print("done indexing")
    fp = segment.saveScoreDict(indexedSegments)
    #print indexedSegments
    return fp, indexedSegments

def cacheSimilarity(fp = None, indexedSegments = None, writeCSV=True):
    if fp is not None and indexedSegments is None:
        indexedSegments = segment.loadScoreDict(fp)
    elif fp is None and indexedSegments is None:
        fp, indexedSegments = indexAndCache()
        print(fp)
    scoreSim = segment.scoreSimilarity(indexedSegments, giveUpdates=True) # @UndefinedVariable
    print("done similarity searching")
    if writeCSV is True:
        with open('/Users/cuthbert/Desktop/test2.csv', 'wb') as csvFile:
            similarityWriter = csv.writer(csvFile)
            for row in scoreSim:
                if row[0] != row[4]:
                    similarityWriter.writerow(row)
        print("done writing csv file")
    return scoreSim

def filterAverage(fp = '/Users/cuthbert/Desktop/test2.csv', threshold = 0.5, scoreSim = None):
    '''
    figure out the most similar pieces for any given piece in the .csv file.
    '''
    if scoreSim is None:
        csvFile = open(fp, 'rb')
        allRows = csv.reader(csvFile)
        print("done reading CSV file")
    else:
        allRows = scoreSim
        csvFile = None
    pieces = {}
    for i, row in enumerate(allRows):
        if i % 1000000 == 0:
            print("Done %d rows" % i)
        piece1, part1, segmentNumber1, measureNumber1, piece2, part2, unused_segmentNumber2, measureNumber2, ratio = row[:]
        if piece1 not in pieces:
            pieces[piece1] = {}
        if part1 not in pieces[piece1]:
            pieces[piece1][part1] = {}
        if segmentNumber1 not in pieces[piece1][part1]:
            pieces[piece1][part1][segmentNumber1] = {'measureStart': measureNumber1,
                                                     'totalComparisons': 0,
                                                     'totalRatio': 0.0,
                                                     }
        seg1Dict = pieces[piece1][part1][segmentNumber1]
        seg1Dict['totalComparisons'] += 1
        seg1Dict['totalRatio'] += float(ratio)


    totalOfAverages = 0.0
    totalSegments = 0
    for piece in pieces:
        for part in pieces[piece]:
            for segment in pieces[piece][part]:
                segDict = pieces[piece][part][segment]
                averageRatio = segDict['totalRatio']/segDict['totalComparisons']
                #print piece, part, segment, averageRatio
                segDict['averageRatio'] = averageRatio
                totalOfAverages += averageRatio
                totalSegments += 1

    averageSimilarityOfAllSegments = totalOfAverages/totalSegments
    print(totalSegments, averageSimilarityOfAllSegments)
    if csvFile is not None:
        csvFile.close()
        csvFile = open(fp, 'rb')
        allRows = csv.reader(csvFile)
        print("done reading CSV file")


    pieceSimilarities = {}

    for i, row in enumerate(allRows):
        if i % 1000000 == 0:
            print("Done %d rows" % i)
        piece1, part1, segmentNumber1, measureNumber1, piece2, part2, unused_segmentNumber2, measureNumber2, ratio = row[:]
        segDict = pieces[piece1][part1][segmentNumber1]
        averageRatio = segDict['averageRatio']
        scaledRatio = (float(ratio) - averageRatio)/(1 - averageRatio)
        #print "%3.3f %3.3f %3.3f" % (averageRatio, float(ratio), scaledRatio)
        if scaledRatio > threshold:
            print(scaledRatio, piece1, part1, measureNumber1,
                  piece2, part2, measureNumber2, float(ratio))
            if piece1 not in pieceSimilarities:
                pieceSimilarities[piece1] = {'TOTAL': 0}
            if piece2 not in pieceSimilarities[piece1]:
                pieceSimilarities[piece1][piece2] = 1
            else:
                pieceSimilarities[piece1][piece2] += 1
            pieceSimilarities[piece1]['TOTAL'] += 1

    import pprint
    pprint.pprint(pieceSimilarities)
    #print pieceSimilarities
    if csvFile is not None:
        csvFile.close()


def readCSV(fp = '/Users/cuthbert/Desktop/test2.csv'):
    '''
    return an array of lists for each row in the CSV file.
    '''
    allRows = []
    with open(fp, 'rb') as csvFile:
        similarityReader = csv.reader(csvFile)
        for row in similarityReader:
            allRows.append(row)
    return allRows

if __name__ == '__main__':
    scoreSim = cacheSimilarity()#fp='/var/folders/x5/rymq2tx16lqbpytwb1n_cc4c0000gn/T/music21/tmpnyRVLd.json')
    filterAverage(threshold = 0.6,scoreSim=scoreSim)
    #filterAverage(fp = '/var/folders/x5/rymq2tx16lqbpytwb1n_cc4c0000gn/T/music21/tmpcEtwn7.json', threshold=0.55)
    quit()
    cacheSimilarity('/var/folders/x5/rymq2tx16lqbpytwb1n_cc4c0000gn/T/music21/tmpVifOQV.json')
