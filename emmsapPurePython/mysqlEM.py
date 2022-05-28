# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
import os
import getpass

from collections import namedtuple

import mysqlclient

from music21 import common
from music21 import converter
from music21 import expressions
from music21 import layout
from music21 import note
from music21 import stream

from emmsap import files


RatioMatch = namedtuple('RatioMatch', 'thisSegmentId otherSegmentId thisRatio')


class EMMSAPException(Exception):
    pass


def readEMMSAPPasswordFile(userdir=None):
    if userdir is None:
        username = getpass.getuser()
        # likely to be /Library/Webserver on Mac
        userdir = os.path.expanduser('~' + username)

    # logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    # logging.debug(username)

    mysqlPasswordFile = userdir + os.path.sep + '.emmsap_password'
    if not os.path.exists(mysqlPasswordFile):
        raise EMMSAPException(
            'Cannot read password file! put it in a file in the home directory '
            + 'called .emmsap_password. Home directory is: '
            + userdir
        )

    with open(mysqlPasswordFile) as f:
        pwContents = f.readlines()

    pwDict = {'password': None,
              'host': 'localhost',
              'username': 'emmsap_user',
              'database': 'emmsap',
              # 'awssmtpuser': None,
              # 'awssmtppw': None,
              # 'sslcert': None,
              # 'sslkey': None
              }
    for i, p in enumerate(pwContents):
        p = p.strip()
        if '=' in p:
            key, value = p.split('=', 1)
            pwDict[key] = value
        else:
            pwDict['password'] = p

    return pwDict


class EMMSAPMysql(object):
    def __init__(self):
        self.cnx = self.connect()
        self.cursor = self.getNewCursor()
        self.query = ''

    @staticmethod
    def connect():
        pw_dict = readEMMSAPPasswordFile()
        cnx = mysqlclient.connect(user=pw_dict['user'],
                                  password=pw_dict['password'],
                                  host=pw_dict['host'],
                                  database=pw_dict['database'])
        return cnx

    def commit(self):
        self.cnx.commit()

    def getNewCursor(self):
        cursor = self.cnx.cursor()
        self.cursor = cursor
        return cursor

    def getTableRowById(self, table='pieces', idKey=1):
        '''
        get all the info from a table row given a table and
        an id.

        >>> em = EMMSAPMysql()
        >>> row = em.getTableRowById('country', 1)
        >>> row
        (1, 'Unknown')
        '''
        preQuery = 'SELECT * FROM %s ' % table
        self.query = preQuery + 'WHERE id = %s'
        self.cursor.execute(self.query, [idKey])
        for row in self.cursor:
            # get first
            return row

    def getTableRowByColumnAndValue(self, table, column, value):
        '''
        get a single row from a table where the column equals a value.
        '''
        preQuery = 'SELECT * FROM %s ' % table
        preQuery = preQuery + 'WHERE %s = ' % column
        self.query = preQuery + '%s'
        self.cursor.execute(self.query, [value])
        for row in self.cursor:
            # get first
            return row

    def pieceByFilename(self, filename):
        '''
        return a new pieceObj given a filename

        >>> em = EMMSAPMysql()
        >>> p = em.pieceByFilename('Chi_caval_msc.xml')
        >>> p
        <__main__.Piece object at 0x...>
        >>> p.id
        1
        '''
        row = self.getTableRowByColumnAndValue('pieces', 'filename', filename)
        pieceObj = Piece(row, dbObj=self)
        return pieceObj

    def pieceById(self, pieceId=1):
        '''
        >>> em = EMMSAPMysql()
        >>> p = em.pieceById(1)
        >>> p
        <__main__.Piece object at 0x...>
        >>> p.filename
        u'Chi_caval_msc.xml'
        '''
        row = self.getTableRowById('pieces', pieceId)
        pieceObj = Piece(row, dbObj=self)
        return pieceObj

    def composerById(self, composerId=1):
        '''
        >>> em = EMMSAPMysql()
        >>> c = em.composerById(1)
        >>> c
        <__main__.Composer object at 0x...>
        >>> c.name
        u'Anonymous'
        >>> c.sortYear
        1390
        '''
        row = self.getTableRowById('composer', composerId)
        composerObj = Composer(row, dbObj=self)
        return composerObj

    def segmentById(self, segmentId=1):
        row = self.getTableRowById('segment', segmentId)
        segmentObj = Segment(row, dbObj=self)
        return segmentObj


class EMMSAPMysqlObject(object):
    table = 'country'
    rowMapping = ['column1', 'column2']

    def __init__(self, rowInfo=None, dbObj=None):
        if dbObj is None:
            self.dbObj = EMMSAPMysql()
        else:
            self.dbObj = dbObj
        self.cnx = self.dbObj.cnx
        if rowInfo is None:
            rowInfo = [None for _ in self.rowMapping]
        elif not common.isIterable(rowInfo):
            # print(self.table, rowInfo)
            rowInfo = self.dbObj.getTableRowById(self.table, rowInfo)
            if rowInfo is None:
                rowInfo = [None for _unused in range(len(self.rowMapping))]
        for i in range(len(self.rowMapping)):
            # attributeName = self.rowMapping[i]
            # attributeValue = rowInfo[i]
            # print(attributeName, attributeValue)
            setattr(self, self.rowMapping[i], rowInfo[i])


class Piece(EMMSAPMysqlObject):
    table = 'pieces'
    rowMapping = ['id', 'filename', 'piecename', 'composerId', 'frag']

    def __init__(self, rowInfo=None, dbObj=None):
        super(Piece, self).__init__(rowInfo, dbObj)
        if self.frag == 1:
            self.frag = True
        elif self.frag == 0:
            self.frag = False
        else:
            self.frag = None
        self._stream = None

    def stream(self):
        '''
        returns a music21 Score object from this piece
        '''
        if self._stream is not None:
            return self._stream
        if self.filename is not None:
            # noinspection PyBroadException
            try:
                s = converter.parse(os.path.join(files.emmsapDir, self.filename))
                self._stream = s
                return s
            except Exception:
                print('%s Failed in conversion' % self.filename)
                return None
        else:
            return None

    def numberOfVoices(self):
        '''
        returns the number of voices in the piece

        >>> p = Piece(4)
        >>> p.filename
        u'Ascoli_Piceno_Mater_Digna_Dei_Lux.xml'
        >>> p.numberOfVoices()
        2
        '''
        s = self.stream()
        if s is not None:
            return len(s.parts)
        else:
            return 0

    def composer(self):
        '''
        >>> em = EMMSAPMysql()
        >>> p = em.pieceById(1)
        >>> c = p.composer()
        >>> c.name
        u'Anonymous'
        '''
        return self.dbObj.composerById(self.composerId)

    def segments(self):
        '''
        return a list of all Segment objects associated with this piece

        this is too slow for iterating over the entire dataset, but good for examining
        one piece

        >>> p = Piece(664)
        >>> segmentObjList = p.segments()
        >>> segmentZero = segmentObjList[3]
        >>> (segmentZero.partId, segmentZero.measureStart,
        ...  segmentZero.measureEnd, segmentZero.id, segmentZero.segmentData)
        (0, 1, None, 114664, 'FEDCMSDIOBNRCDEMPIQKEDCIFBCB')
        >>> ratiosZero = segmentObjList[3].ratios()
        >>> ratiosZero[0]
        (114665, 7826)
        '''
        self.dbObj.cursor.execute('''SELECT id FROM segment WHERE piece_id = %s ORDER BY id''',
                                  [self.id])
        segmentRows = self.dbObj.cursor.fetchall()
        segmentObjs = []
        for s in segmentRows:
            sId = s[0]
            segmentObjs.append(Segment(sId, self.dbObj))
        return segmentObjs

    def ratiosAboveThreshold(self, threshold=5000, ignoreInternal=True,
                             segmentType='DiaRhy2', maxThreshold=None):
        '''
        find all segments with a ratio at or above a certain threshold
        (where 5000 = 0.5 similarity),
        optionally ignoring segments that are from the same piece (default True) or
        from the same piece and same part (set ignoreInternal to "`Part`" to use this;
        not yet implemented).

        Returns a list of 3-tuples in the form thisPieceSegmentId, otherPieceSegmentId, ratio

        >>> p = Piece(2)
        >>> highMatch = p.ratiosAboveThreshold(5000)
        >>> highMatch[0]
        RatioMatch(thisSegmentId=116456, otherSegmentId=108265, thisRatio=5755)
        '''
        if maxThreshold is None:
            maxThreshold = 100001

        if 0 < threshold < 1:
            # sanity check: I used to use between 0 and 1:
            threshold = int(threshold * 10000)
        # print(threshold)
        thisPieceId = self.id
        matchingSegments = []
        # self.dbObj.cursor.execute('''SELECT segment1id, segment2id, ratio FROM ratios
        #                             WHERE segment1id IN
        #                                (SELECT id FROM segment WHERE pieceId = %s)
        #                             AND ratio >= %s ORDER BY segment1id''',
        #                             [thisPieceId, threshold])
        # print('HI!')
        self.dbObj.cursor.execute(
            '''SELECT segment1id, segment2id, ratio FROM ratios''' + segmentType
            + '''
                WHERE
                ratio >= %s AND ratio < %s
                AND EXISTS
                   (SELECT 1 FROM segment WHERE piece_id = %s
                    AND segment.id = segment1id)
                ORDER BY ratio DESC''',
            [threshold, maxThreshold, thisPieceId]
        )
        # print('BYE!')
        for otherSeg in self.dbObj.cursor:
            otherSegNamedTuple = RatioMatch(*otherSeg)
            matchingSegments.append(otherSegNamedTuple)
        if ignoreInternal is True:
            matchingSegments2 = []
            for thisRow in matchingSegments:
                otherSegObj = Segment(thisRow.otherSegmentId, self.dbObj)
                if otherSegObj.piece_id != thisPieceId:
                    matchingSegments2.append(thisRow)
            matchingSegments = matchingSegments2
        return matchingSegments

    def partsFromSegmentPair(self, segment1id, segment2id, ratio=0):
        '''
        returns two labeled parts given the segmentIds that come
        from two different pieces, showing only the parts that
        are in the segments.  The ratio is optional and only to
        give a better label to the score.
        '''
        if hasattr(segment1id, 'ratios'):
            segment1 = segment1id
            segment1id = segment1.id
        if hasattr(segment2id, 'ratios'):
            segment2 = segment2id
            segment2id = segment2.id
        infoDict = self.infoFromRatio([segment1id, segment2id, ratio])
        s1 = converter.parse(os.path.join(files.emmsapDir, self.filename))
        if infoDict['otherFilename'] is None:
            return
        # noinspection PyBroadException
        try:
            s2 = converter.parse(os.path.join(files.emmsapDir, infoDict['otherFilename']))
        except Exception:
            return
        p1_id = infoDict['thisPartId']
        p2_id = infoDict['otherPartId']

        p1 = s1.parts[p1_id]
        p2 = s2.parts[p2_id]
        if infoDict['thisMeasureEnd'] is None:
            thisMeasureEnd = infoDict['thisMeasureStart'] + 6
            # len(p1.getElementsByClass('Measure'))
        else:
            thisMeasureEnd = infoDict['thisMeasureEnd']
        if infoDict['otherMeasureEnd'] is None:
            otherMeasureEnd = infoDict['otherMeasureStart'] + 6
            # len(p2.getElementsByClass('Measure'))
        else:
            otherMeasureEnd = infoDict['otherMeasureEnd']
        excerpt1 = p1.measures(infoDict['thisMeasureStart'], thisMeasureEnd)
        excerpt2 = p2.measures(infoDict['otherMeasureStart'], otherMeasureEnd)
        for el in excerpt1.recurse():
            if 'LayoutBase' in el.classes:
                el.activeSite.remove(el)
        for el in excerpt2.recurse():
            if 'LayoutBase' in el.classes:
                el.activeSite.remove(el)

        renumberMeasureOffset = thisMeasureEnd + 1

        excerpt2Measures = excerpt2.iter.getElementsByClass('Measure')
        for i, thisM in enumerate(excerpt2Measures):
            thisM.number = renumberMeasureOffset + i
        if excerpt2Measures:
            firstMeasure2 = excerpt2Measures[0]
        else:
            firstMeasure2 = excerpt2

        removeMe = []
        for el in excerpt2:
            if 'Measure' in el.classes or el.offset != 0:
                break
            if 'Spanner' in el.classes:
                continue
            removeMe.append(el)
        for el in removeMe:
            excerpt2.remove(el)
            firstMeasure2.insert(0, el)

        exp1 = expressions.TextExpression(
            f'({self.id}) {self.filename} part {p1_id}, '
            + f'mm. {infoDict["thisMeasureStart"]}-{thisMeasureEnd} -- ratio {ratio}'
        )
        exp2 = expressions.TextExpression(
            f'({infoDict["otherPieceId"]}) {infoDict["otherFilename"]} part {p2_id}, '
            + f'mm. {infoDict["otherMeasureStart"]}-{otherMeasureEnd}'
        )
        exp1.size = 12
        exp2.size = 12
        exp1.positionVertical = 40
        exp2.positionVertical = 40

        exp2.priority = 5
        pNewMeasures = excerpt1.iter.getElementsByClass('Measure')
        if pNewMeasures:
            firstMeasure = pNewMeasures[0]
        else:
            firstMeasure = excerpt1
        firstMeasure.insert(0, exp1)
        firstMeasure2.insert(0, exp2)

        return (excerpt1, excerpt2)

    def partFromSegmentPair(self, segment1id, segment2id, ratio=0):
        '''
        Given a pair of segmentIds, return a :class:`~music21.stream.Part`
        object that contains the first segment and the second segment, separated by a
        :class:`~music21.layout.SystemLayout` separator.

        >>> p = Piece(22)
        >>> part = p.partFromSegmentPair(8376, 105)
        >>> #_DOCS_SHOW part.show()
        '''
        excerpts = self.partsFromSegmentPair(segment1id, segment2id, ratio)
        if excerpts is None:
            return None

        excerpt1, excerpt2 = excerpts

        pNew = excerpt1

        # sysLayout1 = layout.SystemLayout()
        # sysLayout1.isNew = True
        # sysLayout1.leftMargin = 200.0
        # sysLayout1.distance = 200.0
        # sysLayout1.priority = 0

        # firstMeasure2.insert(0, sysLayout1)
        # lastMeasure = excerpt1.getElementsByClass('Measure')[-1]
        # lastMeasure.append(sysLayout)

        s = stream.Measure()

        r = note.Rest(type='whole')
        r.style.hideObjectOnPrint = True
        r.expressions.append(expressions.Fermata())
        sl = layout.SystemLayout(isNew=True)
        sl.priority = -1
        s.insert(0, sl)
        s.append(r)

        pNew.append(s)

        noLayoutAdded = True
        for el in excerpt2:
            if noLayoutAdded and 'Measure' in el.classes:
                sl = layout.SystemLayout(isNew=True)
                el.insert(0, sl)
                noLayoutAdded = False
            pNew.coreAppend(el)
        pNew.coreElementsChanged()
        return pNew

    def infoFromRatio(self, ratioInformation):
        '''
        utility function, uses objectsFromRatio to return a dictionary of:

        thisPartId: thisSeg.partId,
        thisMeasureStart: thisSeg.measureStart,
        thisMeasureEnd: thisSeg.measureEnd,
        otherPieceId: otherSeg.pieceId,
        otherFilename: otherSeg.piece.filename,
        otherPartId: otherSeg.partId,
        otherMeasureStart: otherSeg.measureStart,
        otherMeasureEnd: otherSeg.measureEnd
        ratio: ratio

        >>> p = Piece(22)
        >>> ratioInfo = (8376, 105, 7000)
        >>> infoDict = p.infoFromRatio(ratioInfo)
        >>> for x in sorted(infoDict.keys()):
        ...     print(x, infoDict[x])
        otherFilename Oxford_229_Sanctus_PMFC_13_A11.xml
        otherMeasureEnd 10
        otherMeasureStart 7
        otherPartId 0
        otherPieceId 63
        ratio 7000
        thisMeasureEnd 20
        thisMeasureStart 1
        thisPartId 1
        '''
        thisSeg, otherSeg, otherPiece, ratio = self.objectsFromRatio(ratioInformation)
        retDict = {'thisPartId': thisSeg.partId,
                   'thisMeasureStart': thisSeg.measureStart,
                   'thisMeasureEnd': thisSeg.measureEnd,
                   'otherPieceId': otherPiece.id,
                   'otherFilename': otherPiece.filename,
                   'otherPartId': otherSeg.partId,
                   'otherMeasureStart': otherSeg.measureStart,
                   'otherMeasureEnd': otherSeg.measureEnd,
                   'ratio': ratio,
                   }

        return retDict

    def objectsFromRatio(self, ratioInformation):
        '''
        utility function to return a 4-tuple of:

        the Segment for this piece that matched, the other Segment, the other Segment's
        associated Piece object, and the ratio again

        >>> p = Piece(22)
        >>> ratioInfo = (8376, 105, 7000)
        >>> thisSeg, otherSeg, otherPiece, ratio = p.objectsFromRatio(ratioInfo)
        >>> thisSeg.partId, thisSeg.measureStart, thisSeg.measureEnd
        (1, 1, 20)
        >>> otherSeg.partId, otherSeg.measureStart, otherSeg.measureEnd
        (0, 7, 10)
        >>> otherPiece.filename, ratio
        ('Oxford_229_Sanctus_PMFC_13_A11.xml', 7000)
        '''
        thisSeg = Segment(ratioInformation[0], self.dbObj)
        otherSeg = Segment(ratioInformation[1], self.dbObj)
        otherPiece = otherSeg.piece()
        ratio = ratioInformation[2]
        return (thisSeg, otherSeg, otherPiece, ratio)

    def deleteFileOnDisk(self):
        '''
        deletes the file on disk associated with the piece.
        '''
        if not self.filename:
            print('Piece did not exist')
            return

        fn = files.emmsapDir + os.sep + self.filename
        if os.path.exists(fn):
            os.remove(fn)
        else:
            print('File %s did not exist' % fn)

    def deletePiece(self, keepPieceEntry=False):
        '''
        Deletes this piece entirely from the database, including its segments and ratios.

        Does not delete any composers, etc. associated with it or the file on disk.
        use deleteFileOnDisk for that.

        keepPieceEntry makes it possible to reindex everything under the same pieceId number
        '''
        pieceSegments = self.segments()
        segment1TupleList = []
        for sObj in pieceSegments:
            segId1Tuple = (sObj.id, )
            segment1TupleList.append(segId1Tuple)
        print(segment1TupleList)

        for ratioTable in ('DiaRhy2', 'IntRhySmall'):  # ('diaSlower1','DiaRhy2'):
            print('deleting first ratios... from %s' % ratioTable)
            deleteRatiosQuery1 = ('''DELETE FROM ratios'''
                                  + ratioTable
                                  + ''' WHERE segment1id = %s''')
            for thisTuple in segment1TupleList:
                print('...deleting %s' % thisTuple[0])
                delQuerySub = deleteRatiosQuery1 % thisTuple[0]
                # print(delQuerySub)
                self.dbObj.cursor.execute(delQuerySub)
                self.dbObj.cnx.commit()
            # self.dbObj.cursor.executemany(deleteRatiosQuery1, segment1TupleList)
            print('deleting second ratios... from %s' % ratioTable)
            deleteRatiosQuery2 = ('''DELETE FROM ratios'''
                                  + ratioTable
                                  + ''' WHERE segment2id = %s''')
            for thisTuple in segment1TupleList:
                print('...deleting %s' % thisTuple[0])
                delQuerySub = deleteRatiosQuery2 % thisTuple[0]
                # print(delQuerySub)
                self.dbObj.cursor.execute(delQuerySub)
                self.dbObj.cnx.commit()

        # self.dbObj.cursor.executemany(deleteRatiosQuery2, segment1TupleList)
        print('deleting segments...')
        deleteSegmentsQuery = '''DELETE FROM segment WHERE id = %s'''
        for thisTuple in segment1TupleList:
            print('...deleting %s' % thisTuple[0])
            delQuerySub = deleteSegmentsQuery % thisTuple[0]
            # print(delQuerySub)
            self.dbObj.cursor.execute(delQuerySub)
        self.dbObj.cnx.commit()
        # self.dbObj.cursor.executemany(deleteSegmentsQuery, segment1TupleList)
        print('deleting texts...')
        self.dbObj.cursor.execute('''DELETE FROM texts WHERE fn = %s''', (self.filename, ))
        print('deleting tinyNotation')
        self.dbObj.cursor.execute('''DELETE FROM tinyNotation WHERE fn = %s''', (self.filename, ))
        print('deleting intervals')
        self.dbObj.cursor.execute('''DELETE FROM intervals WHERE fn = %s''', (self.filename, ))
        if keepPieceEntry is not True:
            print('deleting piece...')
            self.dbObj.cursor.execute('''DELETE FROM pieces WHERE id = %s''', (self.id, ))
        self.dbObj.cnx.commit()


class Composer(EMMSAPMysqlObject):
    table = 'composer'
    rowMapping = ['id', 'isCanonical', 'canonicalLink', 'name', 'sortYear', 'earliestYear',
                  'latestYear', 'country_id']

    def __init__(self, rowInfo=None,  dbObj=None):
        super(Composer, self).__init__(rowInfo, dbObj)
        if self.isCanonical == 0:
            self.isCanonical = False
        else:
            self.isCanonical = True


class Segment(EMMSAPMysqlObject):
    '''
    N.B. unlike Composer and Piece, there are enough
    segments that there are times when you'll want
    to work with the rowInfo directly

    >>> s = Segment(60)
    >>> s.segmentData
    'DDGFEGAFEDSFNABAFEDDACDABACDSM'
    >>> s.piece().filename
    'PMFC_24_32-Chi_nel_servir_antico.xml'
    '''
    table = 'segment'
    rowMapping = ['id', 'piece_id', 'partId', 'segmentId',
                  'measureStart', 'measureEnd', 'encodingType', 'segmentData']

    def __init__(self, rowInfo=None, dbObj=None):
        super(Segment, self).__init__(rowInfo, dbObj)

    def piece(self):
        '''
        return the pieceObject for the piece with this id
        '''
        p = Piece(self.piece_id, self.dbObj)
        return p

    def ratios(self):
        '''
        return all ratios associated with this segment

        Returns a list of 2-tuples ordered by segment2Id,
        where the first element is the other
        segmentId and the second entry is the ratio.

        >>> s = Segment(114664)
        >>> s.piece().filename, s.measureStart, s.measureEnd
        ('Paris_Lat_12409_f_243v.xml', 1, None)
        >>> ratios = s.ratios()
        >>> ratios[1]
        (123938, 5294)
        >>> s2 = Segment(ratios[1][0], dbObj=s.dbObj)
        >>> s2.piece().filename, s2.measureStart, s2.measureEnd
        ('PMFC_23_37-Gloria_Et_verus_homo_deus.mxl', 19, 53)
        '''
        segmentType = 'DiaRhy2'
        self.dbObj.cursor.execute('''SELECT segment2id, ratio FROM ratios''' + segmentType + '''
                                        WHERE segment1id = %s ORDER BY segment2id''', [self.id])
        segmentRatios = self.dbObj.cursor.fetchall()
        return segmentRatios


if __name__ == '__main__':
    # for i in [536]:
    #     p = Piece(i)
    #     p.deletePiece()
    # exit()
    import music21
    music21.mainTest('moduleRelative', 'verbose')
