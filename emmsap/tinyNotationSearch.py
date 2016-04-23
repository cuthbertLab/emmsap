'''
Searches in the database for tinyNotation.

Began with searching the back of Bologna Q15 capitals for matches:

#9 = cantus I of Zachara Credo du Vilage (see #35 also); MB's identification of succession is correct
#35 = cantus II of Zachara Credo du Vilage (see #9 also); 
#37 ?? could be Credo Ciconia #10 top of R5r -- position is perfect, stems are not;
#44 = Ciconia Credo #4 -- previously known only from Warsaw 378 and Kras. "invisibilium" is the giveaway. two lines down is probably "omnia" [facta sunt]
#49 = Credo Perneth/Bonharde mm 54-55!!! strange, I know, but a perfect match. PMFC 23.51; in Padua 684 (Pad A), Grottaferrata 224 (olim 197) and Strasbourg, so possible!
'''

searches = {
    # q15 initial numbers
    'q15_2': ("rare. but no match", 'fn like "%kyrie%" AND intervals like "%4-22-4%"'),
    'q15_3': ("23 - no matches", 'intervals like "%-2222-24-2%"'),
    'q15_4': ("MB Found Piece: Zachara", 'intervals like "%-224-2-2-2%"'),
    'q15_5': ("MB Found Piece: Salinis", '(fn like "%credo%" OR fn like "%patrem%") AND intervals like "%-2-34%"'),
    'q15_9': ("MSC: Also Zachara! 35 total / latin / natum ante", 'intervals like "%2-422-3-2%"'),
    'q15_14': ("0 for glorias 65 for total", 'intervals like "%22-5322%"'),
    'q15_16': ("0 -- only match Ay si is not it", 'intervals like "%-2-4233-2-2%"'),
    'q15_17': ("agimus (none found)", '(fn like "%gloria%" OR fn like "%terra%") AND intervals like "%-_24-2-22%"'),
    'q15_18': ('om[a]mus te (none found)', '(fn like "%gloria%" OR fn like "%terra%") AND intervals like "%2-2-33%"'),
    'q15_23': ('pater omnipo', '(fn like "%gloria%" OR fn like "%terra%") AND intervals like "%-2-2-22-2%"'),
    'q15_24': ('none', 'intervals like "%3-453-2-2-2%"'),
    'q15_26': ('none', 'intervals like "%-3-26-22%"'),
    'q15_27': ('filio', '(fn like "%credo%" OR fn like "%patrem%") AND intervals like "%-44%"'),
    'q15_29': ('[common but 6/8 so easier but 537 so need TinyNotation]', 'intervals like "%-2-232-2%"'),
    'q15_30': ('[common but easier because of void...94 total none]', 'intervals like "%3-2-32-2%"'),
    'q15_33': ('resurrexit 36 pieces none match', '(fn like "%credo%" OR fn like "%patrem%") AND intervals like "%-21-221%"'),
    'q15_34': ('patre [too common]', '(fn like "%credo%" OR fn like "%patrem%") AND intervals like "%2-2%"'),
    'q15_35': ('et ex patre  -- Zachara, Credo, du Vilage', '(fn like "%credo%" OR fn like "%patrem%") AND intervals like "%2122-33%"'),
    'q15_36': ('Gloria "et in" [too common 270]','(fn like "%gloria%" OR fn like "%terra%") AND intervals like "%222%"'),
    'q15_37': ('credo -- visibilium [rare; Ciconia?]', '(fn like "%credo%" OR fn like "%patrem%") AND intervals like "%-2-21-224%"'),
    'q15_39': (' Gloria "amus te" [17; no match]', '(fn like "%gloria%" OR fn like "%terra%") AND intervals like "%22-2-232%"'),
    'q15_40': ('Credo et in sp [9; none]', '(fn like "%credo%" OR fn like "%patrem%") AND intervals like "%2222-52%"'),
    'q15_43': ('Gloria nedicamus [18 none]', '(fn like "%gloria%" OR fn like "%terra%") AND intervals like "%121-22%"'),
    'q15_44': ('Credo "filium" or "visibilium" or "invisibilium" [42]', '(fn like "%credo%" OR fn like "%patrem%") AND intervals like "%-23-5%"'),
    'q15_46': ('rculo (Verbum caro...) [12; none likely]', 'intervals like "%-2-21-23-2-2-2-2%"'),
    'q15_48': ('agnus or kyrie? [18 none]', '(fn like "%kyrie%" OR fn like "%agnus%") AND intervals like "%-2-2-225%"'),
    'q15_49': ('Credo natus est de spiri [9]','(fn like "%credo%" OR fn like "%patrem%") AND intervals like "%-321-4%"'),
    'q15_50': ('Gloria "tris qui toll" (rare, but not in Marchi 30; PMFC13.12)', '(fn like "%gloria%" OR fn like "%terra%") AND intervals like "%22-46%"'),
    'q15_51': ('Kyrie (first interval ?? -- rare, but no match)','fn like "%kyrie%" AND intervals like "%-42-32%"'),
    'q15_55': ('3/4 time rare; no match', 'intervals like "%-3-21-3-2%"'),
    'q15_62': ('rare no match','intervals like "%-22-333-2-2-2%"'),
    'q15_67': ('common [60] -- use hasRest -- not found','intervals like "%-2-2-34-2%"'),
    'q15_68': ('Credo et in unum [88 none]','(fn like "%credo%" OR fn like "%patrem%") AND intervals like "%32-4%"'),
    ##70 no in fine temporum -- no text match...
    'q15_75': ('only 10 matches','intervals like "%3-242-32%"'),
    'q15_77': ('19 rows combining both -3 5 always has a rest between it!','intervals like "%-3522%" AND intervals like "%-22-2-22%"'),
    'q15_78': ('sti [too common...3102; must filter text first]','intervals like "%-2-222%"'),
    'q15_81': ('very common (271)','intervals like "%-2-2-2222-3%"'),
    'q15_82': ('very common 327','intervals like "%-2-2-2-2-24%"'),
    'q15_83': ('[594] so combinin with Credo [71] and text search + rest[0]... minum or at least num...','(fn like "%credo%" OR fn like "%patrem%") AND intervals like "%-2-22-4%"'),
    'q15_85': ('"sericordie" -- misericordie -- Salve Regina or Magnificat (not Kyrie Rex Angelorum either)','intervals like "%-2-2-2-23-2%" AND (fn like "%alve%" or fn like "%agnific%")'),
    'q15_88': ('only source (Cividale 98 Philippcoctus Credo Tenor) not a match','intervals like "%-24-5232%"'),
    #89 -- text matches eliminate
    'q15_90': ('Credo et in unum','(fn like "%credo%" OR fn like "%patrem%") AND intervals like "%-352-2%"'),
    'q15_front': ('Q15 front cover gloria', '(fn like "%gloria%" OR fn like "%terra%") AND intervals like "%223-2-2-22-3%"'),
    
    # not Q15
    'avr': ('avranches 13 f. 1r', 'intervals like "%-41-251%"'),
    25406: ('paris 25406', 'intervals like "%-24-32-2-2-2%"'),
    'vat1969ct': ('', 'fn like "PMFC_21%" AND intervals like "%2-3-2222%"'),
    'vat1969more': ('search end', 'intervals like "%2-2-22-2"'),
    
    # SL
    'sl01v': ('', 'intervals like "%-25-432%"'),
    'sl22r': ('test to see if it can be found: Yes!', 'intervals like "%2211-2-2-2-25%"'),
    'sl29v': ('below nascoso el viso', 'intervals like "%15-2-45-2-4%"'),
    #'sl21v': ('test to see if it can find NOPE', 'intervals like "%-2-22-2-22-2222-2-2%"')
    'sl31v': ('','partId > 0 and intervals like "%2-54-22-2%"'),
    'sl33v': ('WHOOPS, matched piece above...common intervals, but clef is clear', 'intervals like "%123-21-21%"'),
    'sl34r': ('none yet; but generic', 'intervals like "%22221-2-2-2-2-22%"'), 
    'sl37v': ('','partId > 0 and intervals like "%3-44-2-2-3%"'),
    'sl38ra': ('whole page was la dolce cere -- mistake', 'intervals like "%-2222-3-2-2223-22-2%"'), 
    'sl39r': ('end of line','intervals like "%-2131-22-3-22%"'),
    'sl41vx': ('end of laurate chroma','intervals like "%-22-2-22-2-2-2-22%"'),
    'sl41v': ('secunda pars','intervals like "%-215-2-24-2-3-2%"'),
    'sl42r': ('','intervals like "%2-2-21-21-21-23%" and fn not like "%gloria%" and fn not like "%credo%"'),
    
    'sl72r': ('first end with C3', 'intervals like "%22-2-2-2-2-2%" and intervals like "%-222-21-2-2-2-23%"'),
    'sl75r': ('secunda pars; might be wrong intervals; virelai','intervals like "%3-44-33%"'),
    'sl78v': ('beginning of contratenor; none match', 'partId >= 1 and intervals like "%-2-22-322-22-32%"'),
    'sl79v': ('I fu gia usignolo -- main piece; at least it works', 'intervals like "%5-222-3-222-22%"'),
    'sl82r': ('Middle lines, all ligatures; 3/4?', 'intervals like "%-322-32%" and intervals like "%3-2-2-22-2%" and partId >= 1 and fn not like "%gloria%" and fn not like "%credo%" and fn not like "%kyrie%"'),
    'sl83v': ('might be the end of the Mazzuoli piece; no match', 'intervals like "%22-2-2-22-32-2-2-2-2%"'),
    'sl94r': ('', 'intervals like "%-2-2-2-23-232-222%"'),
    'sl99bisv': ('none match', 'partId >= 1 and fn not like "%gloria%" and fn not like "%credo%" and intervals like "%3-21-2222-2-22%"'),
    #'sl99ter': ('below Mazzuoli', ''),
    'sl109bisr': ('MSC: FOUND! Rosetta second section', 'intervals like "%2-414-2-22%"'),
    'sl111r': ("end", 'intervals like "%4-2-2-22-2"'),
    'sl137r': ('below amor de dimmi', {'lastNameWithOctave': 'G3'}, 'intervals like "%-2-2-2-2-2" and fn not like "%gloria%" and fn not like "%credo%"'),
    'sl137br': ('below amor de dimmi', {'hasRest': True, 'lastNameWithOctave': 'A3'}, 'intervals like "%-25-2-2-21%" and partId >= 1 and fn not like "%gloria%" and fn not like "%credo%"'),
    'sl139v': ('MSC: Paolo! Marticius qui fu de Rome', 'partId > 0 and fn not like "%gloria%" and fn not like "%credo%" and intervals like "%-222322-2-2-42-2-2%"'),
    'sl141v': ('', 'fn not like "%gloria%" and fn not like "%credo%" and fn not like "%sanctus%" and intervals like "%22-21-22-3-21%"'),
    'sl147r': ('second piece, tenor start', 'fn not like "%gloria%" and fn not like "%credo%" and intervals like "-2-2-25222%"'),
    'sl147br': ('second piece, tenor near 2nd pars', 'fn not like "%gloria%" and fn not like "%credo%" and intervals like "%-2-2-272-42%"'),
    'sl147cr': ('first piece, cttenor 3a pars', 'fn not like "%gloria%" and fn not like "%credo%" and intervals like "%311-2-2-232%"'),
    
    'sl155r': ('great tenor', 'intervals like "%-225-2-21-3%"'),
    'sl156r': ('end of cantus?','partId = 0 and intervals like "%-2-22-223-2%" and fn not like "%gloria%" and fn not like "%credo%" and fn not like "%kyrie%" and fn not like "%sanctus%" and fn not like "%patrem%"'),
    'sl159r': ('qui fault boyt tenor start','partId > 0 and intervals like "%-2-2-2-24-3%" and fn not like "%gloria%" and fn not like "%credo%" and fn not like "%kyrie%" and fn not like "%sanctus%" and fn not like "%patrem%"'),
    'sl159rb': ('qui fault boyt tenor end', {'lastNameWithOctave': 'D3'} ,'intervals like "%-2-44-2-2-2" and fn not like "%gloria%" and fn not like "%credo%" and fn not like "%kyrie%" and fn not like "%sanctus%" and fn not like "%patrem%"'),
    'sl160v': ('unknown', {'hasRest': True, 'lastNameWithOctave': 'E4'}, 'intervals like "%2-32122-2%"'),
    'sl177r': ('end of line -- white notation!', {'hasRest': True}, 'intervals like "%-2222-21-23"'),

    'utrecht1': ('','(fn regexp "credo" or fn regexp "patrem") and intervals like "%72-4%"'),
    'utrecht2': ('','(fn regexp "credo" or fn regexp "patrem") and intervals like "%22-3121%"'),
    'utrecht3': ('','intervals like "%-48-2-21%"'),
    'utrecht4': ('','intervals like "%-2-23141-2-2-2-2%"'),
    'utrecht5': ('no % at end is not a mistake', 'intervals like "%-2-3-2-2-2-2"'),
    
    'nur9aDv': ('palimpsest', 'intervals like "%-222-321%"'),
    'nur9a2': ('palimpsest', 'intervalsNoUnisons like "%-225-2-2-2-2-222-2%"'),
    'nur9a3': ('palimpsest', 'intervalsNoUnisons like "%-2-225-2-2-22-2%"'),
    'nur9a4': ('palimpsest', 'intervals like "%51-2-21-22%"'),
    'nur9a5': ('palimpsest', {'skip': ['PMFC_04_07-D_amor']}, 'intervalsNoUnisons like "%-2-222-252-2-2-22%"'),
    
    'ox56_81r': ('Oxford 56', 'intervals like "%-2-2-2-22222-422%"'),
    'ox56_80r': ('Ox56', 'intervals like "%2-2-222221%" AND (fn regexp "gloria" or fn regexp "terra")'),
    'ox56_80rb': ('Ox56', 'intervals like "%2-2-2-2-2223%" AND (fn regexp "gloria" or fn regexp "terra")'),
    'ox56_80rc': ('Ox56 tenor', 'intervals like "%4-42-25%" AND (fn regexp "gloria" or fn regexp "terra")'),
    'ox56_80rd': ('Ox56 tenor', 'intervals like "%522-2-2-22%" AND (fn regexp "gloria" or fn regexp "terra")'),
    'kobl1': ('Kobl other side', 'intervals like "%1-2-3-222%"'), # and (fn regexp "PMFC_01" or fn regexp "PMFC_02" or fn regexp "PMFC_03" or fn regexp "PMFC_05")'),
    'kobl2': ('Kobl other side', 'intervals like "%11-34%" and (fn regexp "PMFC_01" or fn regexp "PMFC_02" or fn regexp "PMFC_03" or fn regexp "PMFC_05")'),
    'kobl3': ('Kobl other side', 'intervals like "%1-34-3%" and (fn regexp "PMFC_01" or fn regexp "PMFC_02" or fn regexp "PMFC_03" or fn regexp "PMFC_05")'),
    'kobl4': ('Kobl other side', 'intervals like "%2-321-4%" and intervals like "%-2-3-222%"'), # and (fn regexp "PMFC_01" or fn regexp "PMFC_02" or fn regexp "PMFC_03" or fn regexp "PMFC_05")'),
    'kobl5': ('Kobl other side', {'hasRest': True}, 'intervals like "%2-321-4%" and (fn regexp "PMFC_01" or fn regexp "PMFC_02" or fn regexp "PMFC_03" or fn regexp "PMFC_05")'), 
    'kobl6': ('Kobl other side', {'hasRest': True}, 'intervals like "%-2221%" and intervals regexp "-22211+-34-3"'), # and (fn regexp "PMFC_01" or fn regexp "PMFC_02" or fn regexp "PMFC_03" or fn regexp "PMFC_05")'), 
    'koblB1': ('Kobl other side right', 
               'intervals like "%2-211-4%" and (fn regexp "PMFC_01" or fn regexp "PMFC_02" or fn regexp "PMFC_03" or fn regexp "PMFC_05")'), # and (fn regexp "PMFC_01" or fn regexp "PMFC_02" or fn regexp "PMFC_03" or fn regexp "PMFC_05")'), 
    'koblB2': ('Kobl other side right', 
               'intervals like "%1-4-21%" and (fn regexp "PMFC_01" or fn regexp "PMFC_02" or fn regexp "PMFC_03" or fn regexp "PMFC_05")'), # and (fn regexp "PMFC_01" or fn regexp "PMFC_02" or fn regexp "PMFC_03" or fn regexp "PMFC_05")'), 

    'cambraiI7v': ('Cambrai I--07v motet', {'skip': ['PMFC_23_a1-Credo']},
                   'intervals like "%-222212-2-2-23%"'),
    'cambraiI7vb': ('Cambrai I--07v motet try 2', {'hasRest': True, 'skip': ['PMFC_23_a1-Credo']},
                   'intervals like "%-22221-3-22%"'),
    'cambraiI7vtenor': ('Cambrai I--07v motet tenor', {'hasRest': True, 'skip': ['Deus_Tuorum_Militum']},
                   'intervals like "%-24231-2-23%"'),
    'cambraiI14vFlos': ('Cambrai I-13v Fors perversa rotam tenor (no matches w/o unisons either)', 
                        'intervals like "%2-22-21-2-35-222-2-2%"'),            
    'cambII1vtenor': ('Cambrai Vo douls regards, tenor', 'intervals like "%-2-224-2-48-32-32%"'),
    'cambII1vtenb': ('Cambrai Tristour et merancolie', 'intervals like "%2-2-2-2-29-2%"'),

}
from music21 import converter
from emmsap import files, mysqlEM
import os
import re

def runSearch():
    runOne('sl177r', True)
    #runAll()

def runAll():
    for k in searches:
        print("******************")
        print(searches[k][0])
        runOne(k)
    
def runOne(searchIndex, show=False):
    ##############
    print("Running: " + str(searchIndex))
    
    pieceMinimum = 0 # for searching only newly added pieces...
    
    intervalsLike = re.compile(r'intervals like\s"\%?([0-9\-]+)\%?"')
    intervalsNoUnisonLike = re.compile(r'intervalsNoUnisons like\s"\%?([0-9\-]+)\%?"')
    
    
    em = mysqlEM.EMMSAPMysql()
    
    searchTuple = searches[searchIndex]
    comment = ""
    if len(searchTuple) == 2:
        comment, searchQuery = searchTuple
        options = {}
    elif len(searchTuple) == 3:
        comment, options, searchQuery = searchTuple 
    else:
        raise("Incorrect tuple %s" % searchTuple)
    
    timeSigSearch = options.get('timeSignature')
    syllableSearch = options.get('syllable') # "sur" # "lo"
    pieceFracStart = options.get('pieceFracStart') #3.0 # first one third; for "mus te" etc.
    pieceFracEnd = options.get('pieceFracEnd')
    hasRest = options.get('hasRest') #
    partNum = options.get('partNum')
    lastNameWithOctave = options.get('lastNameWithOctave') # "A3" # "E4" # "A3" # pitch of last note
    skip = options.get('skip', [])
    
    intervalList = []
    intervalNoUnisonList = []
     
    for i, iLike in enumerate([intervalsLike, intervalsNoUnisonLike]):    
        foundInterval = iLike.search(searchQuery)
        intervalMatch = "9999999"
        if foundInterval:
            intervalMatch = foundInterval.group(1)
        intervalListRaw = re.split(r'(\-?\d)', intervalMatch)
        tempList = [int(r) for r in intervalListRaw if r != ""]
        if i == 0:
            intervalList = tempList
        else:
            intervalNoUnisonList = tempList
    
    ## capital 17 has a -_ wildcard
    ## intervalList = [2, 4, -2, -2, 2]
    print(intervalList)
    
    q = "SELECT fn, partId FROM intervals WHERE " + searchQuery
    em.cursor.execute(q)
    if comment != "":
        print(comment)
    print(em.cursor.rowcount, "Rows total")
    for rowCount, (fn, partId) in enumerate(em.cursor):
        found = False
        skipIt = False
        for s in skip:
            if s in fn:
                skipIt = True
        if skipIt:
            continue
        
        pieceObj = em.pieceByFilename(fn)
        if pieceObj.id < pieceMinimum: # searching new only...
            continue
        
        print(rowCount, fn, partId)
        #if pieceNum < 9:
        #    continue
        if partNum is not None and partNum != partId:
            print("wrong part..." + str(partId))
            continue
        fullFn = files.emmsapDir + os.sep + fn
        s = converter.parse(fullFn)
        part = s.parts[partId]
        numMeasures = len(part.getElementsByClass('Measure'))
        
        pn = part.flat.notes.stream()
        pn[0].lyric = "***"
        intervalListPiece = []
        last = None
        lastSyllableMatch = None
        
        goodCount = -1
        illen = len(intervalList)
    
        for i,n in enumerate(pn):
            if not hasattr(n, 'pitch'):
                continue # chord
            if n.tie is not None and n.tie.type != 'start':
                continue
            goodCount += 1
            dnn = n.pitch.diatonicNoteNum
            if last is not None:
                intv = dnn - last
                if (intv >= 0):
                    intv += 1
                else:
                    intv += -1
                #if n.duration.quarterLength != 0.5: # all eighth notes
                #    intv = 9
                intervalListPiece.append(intv)
            last = dnn
            if (n.lyric is not None and 
                    syllableSearch is not None and 
                    n.lyric.lower() == syllableSearch.lower()):
                lastSyllableMatch = goodCount
            if goodCount >= illen:
                intervalListSlice = intervalListPiece[goodCount - illen:]
                #print(intervalListSlice)
                if intervalListSlice == intervalList or intervalList == [9, 9, 9, 9, 9, 9, 9]:
                    if intervalList !=  [9, 9, 9, 9, 9, 9, 9]:
                        oldLyric = n.lyric or ""
                        n.lyric = oldLyric + "*!*!*"
                        mn = n.measureNumber
                        if mn is None: # after a strip tie
                            mn = n.next().measureNumber
                        pn[0].lyric += "_" + str(mn)
                        if (syllableSearch is not None and 
                                (lastSyllableMatch is None or lastSyllableMatch < (i - illen - 2))):
                            print("--not syllable")
                            continue
                        if pieceFracStart is not None and mn > numMeasures / pieceFracStart:
                            print("--not pieceFracStart")
                            continue # must be in first 1/3 of piece
                        if pieceFracEnd is not None and mn < numMeasures - (numMeasures / pieceFracEnd):
                            print("--not pieceFracEnd")
                            continue # must be in last 1/10th of piece if pieceFracEnd is 10.0
                        
                        if hasRest is not None:
                            foundRest = False
                            for measureSearch in range(mn - 2, mn):
                                thisMeasure = part.measure(measureSearch)
                                if thisMeasure is not None:
                                    if len(thisMeasure.flat.getElementsByClass('Rest')) > 0:
                                        foundRest = True
                            if hasRest is True:
                                if foundRest is False:
                                    print("--not foundRest")
                                    continue
                        if lastNameWithOctave is not None:
                            if n.pitch.nameWithOctave != lastNameWithOctave:
                                print("--not right step")
                                continue
                        
                        if timeSigSearch is not None:
                            ts = n.getContextByClass('TimeSignature')
                            if ts is not None and ts.ratioString != timeSigSearch:
                                print("--not timeSig")
                                continue
                        print("Part", partId, "Measure", mn)
                    found = True
            
        if show is True and found is True: # may be false because "23-4" matches "-23-4"
            s.show()
        elif found is False:
            print("Probably not found due to beginning with descending instead of ascending intervals")
        
if __name__ == '__main__':
    runSearch()
