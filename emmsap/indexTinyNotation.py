'''
Convert the database of .xml etc. files (streams) into TinyNotation text.

Eventually, this should be able to be done with .show('tinyNotation', verbose=False)
'''

from music21 import converter, meter
from emmsap import files, mysqlEM, toTinyNotation
import os
#from emmsap import async_dec

em = mysqlEM.EMMSAPMysql()
query = '''REPLACE INTO tinyNotation (fn, partId, tsRatio, tn, tnStrip) VALUES (%s, %s, %s, %s, %s)'''
queryInv = '''REPLACE INTO intervals (fn, partId, intervals, intervalsNoUnisons) VALUES (%s, %s, %s, %s)'''


def exists(fn, table='tinyNotation'):
    #if table == 'tinyNotation': # rebuild
    #    return False
    queryExists = '''SELECT * FROM ''' + table + ''' WHERE fn = %s'''
    if table == 'tinyNotation':
        queryExists += " AND tnStrip IS NOT NULL"
    elif table == 'intervals':
        queryExists += " AND intervalsNoUnisons IS NOT NULL"
    em.cursor.execute(queryExists, [fn])
    rows = em.cursor.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False


def onePiece(fn, table='tinyNotation'):
    if exists(fn, table):
        #pass
        return
    fullFn = files.emmsapDir + os.sep + fn
    
    s = converter.parse(fullFn)
    for i, p in enumerate(s.parts):
        try:
            toInterval(i, p, fn)
        except Exception as e:
            print(str(fn) + " " + str(i) + " could not be converted to interval: " + str(e))

        try:
            onePart(i, p, fn)
        except Exception as e:
            print(str(fn) + " " + str(i) + " could not be converted to TN: " + str(e))

    print (fn + " tiny notation indexed")

def onePart(partNum, p, fn):
    allTS = p.flat.getElementsByClass('TimeSignature')
    if len(allTS) > 0:
        ts = allTS[0]
    else:
        ts = meter.TimeSignature('4/4')
    pf = p.flat.notesAndRests.stream()
    tn = toTinyNotation.convert(pf)
    pfs = pf.stripTies()
    tnst = toTinyNotation.convert(pfs)
    #print(fn, partNum, ts.ratioString, tn)
    em.cursor.execute(query, [fn, str(partNum), ts.ratioString, tn, tnst])
    #p.show()

def toInterval(partNum, p, fn):
    pf = p.flat.stripTies().pitches
    last = None
    allInts = []
    allIntsNoUnisons = []
    
    for p in pf:
        dnn = p.diatonicNoteNum
        if last is not None:
            intv = dnn - last
            if (intv >= 0):
                intv += 1
            else:
                intv += -1
            allInts.append(str(intv))
            if intv != 1:
                allIntsNoUnisons.append(str(intv))
        last = dnn
    allIntStr = ''.join(allInts)
    allIntStrNoUnisons = ''.join(allIntsNoUnisons)
    em.cursor.execute(queryInv, [fn, str(partNum), allIntStr, allIntStrNoUnisons])

def runAll(table='tinyNotation'):
    for fn in files.allFiles():
        try:
            onePiece(fn, table)
        except Exception as e:
            print(fn + " could not be converted: " + str(e))

if __name__ == '__main__':
    runAll()
    #from music21.ext.parmap import starmap
    #starmap(onePiece, files.allFiles())
#    onePiece('Assisi_187_frag_3.xml')
    #async_dec.runFuncAsync(onePiece, [('Assisi_187_fragment3.xml',)])
    #async_dec.runFuncAsync(onePiece, [(fn, ) for fn in files.allFiles()])
#    for fn in files.allFiles():
        # print(fn, exists(fn))
       
    