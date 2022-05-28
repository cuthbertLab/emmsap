'''
Extract all texts from EMMSAP and place in database
'''
import difflib
import unicodedata  # @UnresolvedImport
import re
import os
import string

from emmsap import files
from emmsap import mysqlEM
from music21 import text, environment, converter

em = mysqlEM.EMMSAPMysql()
try:
    em.cnx.set_charset('utf8')
except AttributeError:
    # older version or mysql-connector
    pass
# print(em.cnx.charset)

query = '''REPLACE INTO texts (fn, language, text, textReg, textNoSpace) VALUES (%s, %s, %s, %s, %s)'''


environLocal = environment.Environment()

base = files.emmsapDir

ld = text.LanguageDetector()

allFN = set()


def exists(fn, table='texts'):
    if len(allFN) == 0:
        queryExists = '''SELECT fn FROM ''' + table
        em.cursor.execute(queryExists)
        rows = em.cursor.fetchall()
        for r in rows:
            allFN.add(r[0])
    if fn in allFN:
        return True
    else:
        return False


def runAll():
    allTexts = ""
    i = 0
    for fn in files.allFiles():
        if exists(fn):
            # print('Skipping %s' % fn)
            continue
        f = converter.parse(files.emmsapDir + os.sep + fn)
        fp = str(f.filePath)
        fp = fp.replace(base + os.sep, '')

        i += 1
        # if i > 10:
        #    break
        text = getFromFile(f)
        if len(text) < 5:
            print("No text in %s" % fn)
            language = 'na'  # not applicable
            textReg = ""
            textNoSpace = ""
        else:
            language = ld.mostLikelyLanguage(text)
            language = findLanguageMistakes(fp, language)
            textReg, textNoSpace = regularizeText(text, language)

        fshort = fp.replace('.xml', '')
        fshort = fshort.replace('.mxl', '')

        allTexts += '\n\n-----------------------'
        allTexts += fshort + '\n\n'
        allTexts += textReg

        em.cursor.execute(query, [fp, language, text, textReg, textNoSpace])
        em.commit()

        environLocal.warn(language, fp)

    print(allTexts)


def getFromFile(f):
    allTexts = ""
    for i in range(len(f.parts)):
        thisText = text.assembleAllLyrics(f.parts[i])
        if allTexts == "":
            allTexts = thisText
        else:
            if len(thisText) < 10:
                continue
            else:
                # add if substantially different from before.
                r = difflib.SequenceMatcher(a=allTexts, b=thisText).ratio()
                if r < 0.8:
                    allTexts += "\n" + thisText
    allTexts = re.sub('^\s+', '', allTexts)
    return allTexts


def regularizeText(text, language):
    textReg = re.sub('v','u', text.lower())
    textReg = re.sub('j','i', textReg)
    textReg = re.sub('y','i', textReg)
    if language == 'la':
        textReg = re.sub('ae','e', textReg)
    textReg = re.sub(r'[\#\}\{\~\/\.\:\=\;\-\«\»\,\*\?\"\!\'\[\]\<\>\(\)\d_\&\$\|]', '', textReg)
    for punct in string.punctuation:
        textReg = textReg.replace(punct, '')  # partly redundant with above
    textReg = textReg.replace('…', '')
    textReg = re.sub(r'(\s)\s+', r'\g<1>', textReg)
    textReg = unicodedata.normalize('NFKD', textReg)
    textReg = textReg.encode('ascii', 'ignore').decode('UTF-8')

    textNoSpace = re.sub('\W', '', textReg)
    return (textReg, textNoSpace)


mistakes = {
            'PMFC_01_Tournai_6-Ite_Missa_Est.xml': 'la',
            'Ascoli_Piceno_Mater_Digna_Dei_Lux.xml': 'la',
            'Marchi_Notation_16-Virtute_sacquista_cum_grande_faticha.xml': 'la',
            'PMFC_01_Barcelona_1-Kyrie.xml': 'la', # should be gr...
            'PMFC_01_Tournai_1-Kyrie.xml': 'la',
            'Machaut_R01-Doulz_viaire_gracieus.xml': 'fr',
}


def findLanguageMistakes(fp, language):
    if fp not in mistakes:
        return language
    else:
        return mistakes[fp]


if __name__ == '__main__':
    runAll()
