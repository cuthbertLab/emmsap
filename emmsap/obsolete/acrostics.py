'''
Display all possible acrostics...
'''
from emmsap import mysqlEM
from emmsap.files import emmsapBase
from music21.ext import more_itertools

def main():
    em = mysqlEM.EMMSAPMysql()
    em.cursor.execute('SELECT fn, text FROM texts WHERE language = "la" ORDER BY fn')
    allPieces = em.cursor.fetchall()
    with open(emmsapBase + '/emmsap/obsolete/acrostics_out_capitals.txt', 
              'w', 
              encoding='utf-8') as outFile:        
        for fn, text in allPieces:
            if 'gloria' in fn.lower():
                continue 
            if 'credo' in fn.lower():
                continue 
            if 'patrem' in fn.lower():
                continue 
            if 'terra' in fn.lower():
                continue 
            if 'kyrie' in fn.lower():
                continue 
            if 'sanctus' in fn.lower():
                continue 
            if 'agnus' in fn.lower():
                continue 
            if 'OMR' in fn:
                continue
            if 'OMF_PMFC' in fn:
                continue

            if not text:
                continue
            textAcrostic = doOneCaps(text)
            if not textAcrostic:
                continue
            
            #if 'us' not in textAcrostic and 'um' not in textAcrostic:
            #    continue            
            
            outputLine = "{:50s} {:100s}\n".format(fn, ''.join(textAcrostic))
            print(outputLine, end="")
            outFile.write(outputLine)
    
consonants = 'bcdfghjklmnpqrstwxz'    

def doOne(text):
    textSplit = text.split()
    textAcrostic = [t[0] for t in textSplit]
    for i, (j, k, l) in enumerate(more_itertools.stagger(textAcrostic, offsets=(0, 1, 2))):
        if j in consonants and k in consonants and l in consonants:
            textAcrostic[i] = ' '
        
    
    return ''.join(textAcrostic)


def doOneCaps(text):
    consonantsUpper = consonants.upper()
    textCaps = [t for t in text if t in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    for i, (j, k, l) in enumerate(more_itertools.stagger(textCaps, offsets=(0, 1, 2))):
        if j in consonantsUpper and k in consonantsUpper and l in consonantsUpper:
            textCaps[i] = ' '
    return ''.join(textCaps)
    



if __name__ == '__main__':
    main()
