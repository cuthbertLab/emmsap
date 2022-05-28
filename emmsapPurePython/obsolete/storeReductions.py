'''
Convert the database of .xml etc. files (streams) into TinyNotation text.

Eventually, this should be able to be done with .show('tinyNotation', verbose=False)
'''

from music21 import converter, analysis
from emmsap import files, mysqlEM
import os
#from emmsap import async_dec

em = mysqlEM.EMMSAPMysql()
query = '''REPLACE INTO tinyNotation (fn, partId, tsRatio, tn) VALUES (%s, %s, %s, %s)'''


def reduceOne(fn):
    fullFn = files.emmsapDir + os.sep + fn
    s = converter.parse(fullFn)
    chordReducer = analysis.reduceChords.ChordReducer()
    print(" s parsed. reducing...")
    s2 = chordReducer(
        s,
        closedPosition=False,
        maximumNumberOfChords=3,
        )
    print(" s reduced....")
    p = s2.parts[0]
#     cr = analysis.reduceChordsOld.ChordReducer()
#     p = cr.multiPartReduction(s, maxChords = 3, closedPosition=False)
    retList = []
    for c in p.flat.notes:
        ll = c.annotateIntervals(returnList = True)
        if (len(ll) == 0):
            ll = ['1']
        retList.append(''.join(ll))
    print(' '.join(retList))
    s.insert(0, p)
    s.show()
    return retList

if __name__ == '__main__':
    #reduceOne('Cividale_63_Gloria_Amen.xml')
    reduceOne('Bologna_Q15_D_Luca_Gloria.xml')