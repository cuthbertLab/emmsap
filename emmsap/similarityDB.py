# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from __future__ import print_function, division

from emmsap import mysqlEM
#from music21.search import segment
from emmsap.knownSkips import skipFilenames as skipPieces

skipFileNames = [
                 ('Poi_che_da_te_3vv_Lucca.xml', 'PMFC_04_10-Poi_che_da_te_mi_convien.xml')
                 ]

class SimilaritySearcher(object): # 1322
    def __init__(self, startPiece=3007, endPiece=3500, minThreshold=8073, maxToShow=2):
        self.dbObj = mysqlEM.EMMSAPMysql()
        self.startPiece = startPiece
        self.endPiece = endPiece
        self.minThreshold = minThreshold
        self.maxThreshold = 10001
        self.segmentType = 'DiaRhy2'
        #self.segmentType = 'IntRhySmall'
        self.skipGroups = skipPieces
        self.maxToShow = maxToShow
        self.skippedMatchPenalty = 0 # 300 # after skipping one, the odds of a good match goes down.
        self.tenorThresholdAdd = 500
        self.tenorPartNumber = 2
        self.tenorOtherPartNumber = 2
        self.printOutput = True
        self.fragmentsOnly = False
        
    def runPieces(self, startPiece=None, endPiece=None):
        '''
        The main algorithm to search for pieces to match
        
        minThreshold, maxThreshold, and tenorThresholdAdd are numbers from 0 to 10,000+ which scale
        to 0 - 1 (by dividing by 10000) to find similarity.
        
        Because of their rhythmic similarity, tenors match far too often, so a crude metric is used
        to identify tenors and raise the minThreshold for those matches: basically, 
        parts 2+ (=3rd part
        and beyond) are considered tenors. Not very good, but the best so far. 
        '''    
        if startPiece is None:
            startPiece = self.startPiece
        if endPiece is None:
            endPiece = self.endPiece
        
        for pNum in range(startPiece, endPiece):
            self.runOnePiece(pNum)

    def runOnePiece(self, pNum):
        skippedPieces = []
        p = mysqlEM.Piece(pNum, dbObj=self.dbObj)
        if p.id is None:
            return
        
        
        if self.fragmentsOnly is True and p.frag is not True:
            return
        print("Running piece %d (%s)" % (pNum, p.filename))
        ratioMatches = p.ratiosAboveThreshold(self.minThreshold, 
                                              ignoreInternal=True, 
                                              segmentType=self.segmentType)
        totalShown = 0
        for ratioMatch in ratioMatches:
            returnCode = self.checkOneMatch(p, ratioMatch, totalShown, skippedPieces)
                
            if returnCode is not None:
                totalShown = returnCode

    def ratiosForPiece(self, pNum):
        p = mysqlEM.Piece(pNum, dbObj=self.dbObj)
        if p.id is None:
            return
        ratioMatches = p.ratiosAboveThreshold(self.minThreshold, 
                                              ignoreInternal=True, 
                                              segmentType=self.segmentType,
                                              maxThreshold=self.maxThreshold)
        return ratioMatches

    def checkOneMatch(self, p, ratioMatch, totalShown, skippedPieces):
        matches, info = self.checkForShow(p, ratioMatch, skippedPieces)
        if matches is False:
            return
        thisSegment, otherSegment, otherPiece = info
        totalShown += 1
        showInfo = "part %2d, m. %3d; (%4d) %30s, part %2d, m. %3d (ratio %5d)" % (
                                    thisSegment.partId, thisSegment.measureStart,
                                    otherPiece.id, otherPiece.filename, 
                                    otherSegment.partId, 
                                    otherSegment.measureStart, 
                                    ratioMatch.thisRatio)
    
        
        if totalShown > self.maxToShow:
            if otherPiece.id is not None: 
                # if segment matches but piece deleted... need to clean up orphen segments...
                print("   Not showing (too many matches): " + showInfo)
                return totalShown
        try:
            part = p.partFromSegmentPair(*ratioMatch)
        except TypeError:
            part = None
        if part is not None:
            print("   Showing -- " + showInfo)
            part.show()            
        else:
            if otherPiece.id is not None:
                print("  ERROR: not showing for lack of part: " + showInfo)
        return totalShown


    def checkForShow(self, p, ratioMatch, skippedPieces=None):
        if skippedPieces is None:
            skippedPieces = []
        myId = p.id
        if ratioMatch.thisRatio >= self.maxThreshold:
            return (False, "MaxThreshold")
        otherSegment = mysqlEM.Segment(ratioMatch.otherSegmentId, dbObj=self.dbObj)
        otherPiece = otherSegment.piece()
        #if otherPiece.id < myId:
        #    continue
        otherPieceId = otherPiece.id
        if (otherPieceId is None):
            #print("   Skipping match for segment (%d): piece not found." % otherSegmentId)
            return (False, "PieceNotFound")
        foundSkip = False
        for pieceGroup in self.skipGroups:
            if isinstance(pieceGroup[0], int):
                if myId in pieceGroup and otherPieceId in pieceGroup:
                    foundSkip = True
                    break
            if isinstance(pieceGroup[0], str):
                if p.filename in pieceGroup and otherPiece.filename in pieceGroup:
                    foundSkip = True
                    break
                
        if foundSkip is True:
            if otherPieceId not in skippedPieces:
                if self.printOutput:
                    print("   skipping all matches for (%d) %s: ratio %d" % 
                          (otherPiece.id, otherPiece.filename, ratioMatch.thisRatio))
                skippedPieces.append(otherPieceId)
            return (False, "SkipPiece")
        thisSegment = mysqlEM.Segment(ratioMatch.thisSegmentId, dbObj=self.dbObj)
        if (thisSegment.partId >= self.tenorPartNumber or 
                otherSegment.partId >= self.tenorOtherPartNumber):
            # tenor
            if ratioMatch.thisRatio - self.tenorThresholdAdd < self.minThreshold:
                return(False, "TenorBelowThreshold")
        totalPenalty = len(skippedPieces) * self.skippedMatchPenalty
        if ratioMatch.thisRatio - totalPenalty < self.minThreshold:
            print("   below threshold for (%d) %s: ratio %d (adjusted to %d)" % 
                          (otherPiece.id, otherPiece.filename, 
                           ratioMatch.thisRatio, ratioMatch.thisRatio - totalPenalty))
            skippedPieces.append(otherPieceId)
            return(False, "TooCommonPenaltyThreshold")
        
        return (True, (thisSegment, otherSegment, otherPiece))


if __name__ == '__main__':
    ss = SimilaritySearcher()
    ss.runPieces()
