'''
Convert the database of .xml etc. files (streams) into TinyNotation text.

Eventually, this should be able to be done with .show('tinyNotation', verbose=False)
'''

from music21 import converter, meter
from emmsap import files
from emmsap import mysqlEM
from emmsap import toTinyNotation

import os
#from emmsap import async_dec

em = mysqlEM.EMMSAPMysql()
query = '''REPLACE INTO tinyNotation (fn, partId, tsRatio, tn, tnStrip) VALUES (%s, %s, %s, %s, %s)'''
queryInv = '''REPLACE INTO intervals (fn, partId, intervals, intervalsNoUnisons, intervalsWithRests, intervalsAbsolutes) VALUES (%s, %s, %s, %s, %s, %s)'''


def exists(fn, table='tinyNotation'):
    #if table == 'tinyNotation': # rebuild
    #    return False
    queryExists = '''SELECT * FROM ''' + table + ''' WHERE fn = %s'''
    if table == 'tinyNotation':
        queryExists += " AND tnStrip IS NOT NULL"
    elif table == 'intervals':
        queryExists += " AND intervalsWithRests IS NOT NULL"
    em.cursor.execute(queryExists, [fn])
    rows = em.cursor.fetchall()
    return bool(rows)


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
            print(str(fn) + " part " + str(i) + " could not be converted to interval: " + str(e))
            
        try:
            onePart(i, p, fn)
        except Exception as e:
            print(str(fn) + " part " + str(i) + " could not be converted to TN: " + str(e))

    print (fn + " tiny notation and interval indexed")

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
    em.cursor.execute(query, (fn, str(partNum), ts.ratioString, tn, tnst))
    em.commit()
    #p.show()

def toInterval(partNum, p, fn):
    pf = p.flat.stripTies().getElementsByClass('GeneralNote')
    last = None
    allInts = []
    allIntsNoUnisons = []
    allIntsRests = []
    allIntsAbs = []
    alphabet = '__BCDEFGHIJKLMNOPQRSTUVWabcdefghijklmnopqrs'
    
    for gn in pf:
        if hasattr(gn, 'pitches'):
            dnn = gn.pitches[0].diatonicNoteNum
        else:
            allIntsRests.append('r')
            allIntsAbs.append('r')
            continue
            
        if last is not None:
            intv = dnn - last
            if (intv >= 0):
                intv += 1
            else:
                intv += -1
                
            strIntv = str(intv)
            if intv == 10:
                strIntv = 'Z'
            elif intv == 11:
                strIntv = 'Y'
            elif intv >= 12:
                strIntv = 'X'
            
            allInts.append(strIntv)
            allIntsRests.append(strIntv)
            if intv > 0:
                allIntsAbs.append(strIntv)
            else:
                try:
                    allIntsAbs.append(alphabet[intv * -1])
                except IndexError:
                    allIntsAbs.append('X')
                    print("Extreme interval: ", intv, " in ", fn)
            
            if intv != 1:
                allIntsNoUnisons.append(strIntv)
        last = dnn
    allIntStr = ''.join(allInts)
    allIntStrNoUnisons = ''.join(allIntsNoUnisons)
    allIntStrRests = ''.join(allIntsRests)
    allIntStrAbs = ''.join(allIntsAbs)

    params = [fn, str(partNum), allIntStr, allIntStrNoUnisons, allIntStrRests, allIntStrAbs]
    em.cursor.execute(queryInv, params)
    em.commit()

def runAll(table='tinyNotation'):
    for fn in files.allFiles():
        onePiece(fn, table)
        try:
            onePiece(fn, table)
        except Exception as e:
            print(fn + " could not be converted: " + str(e))


if __name__ == '__main__':
    runAll('intervals')
    # from music21.ext.parmap import starmap
    # starmap(onePiece, files.allFiles())
    # onePiece('Assisi_187_frag_3.xml')
    # async_dec.runFuncAsync(onePiece, [('Assisi_187_fragment3.xml',)])
    # async_dec.runFuncAsync(onePiece, [(fn, ) for fn in files.allFiles()])
    # for fn in files.allFiles():
    #   print(fn, exists(fn))
       
