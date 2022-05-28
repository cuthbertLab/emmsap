# -*- coding: utf-8 -*-
'''
Jason Stoessel has generously given EMMSAP permission to include his complete
transcriptions of the Chantilly and Modena codices (among others).

Stoessel transcribes according to his philosophy of preserving original
notation as closely as possible.  While I (MSC) have a different philosophy,
I would not change his transcriptions, except that this notation (with note values larger
than measures, hidden rests, etc.) can't be parsed without taking into account
the hidden notes, etc.

This program normalizes Stoessel's notation to fit EMMSAP/Cuthbert standards.
'''
import copy
import fractions
import os

from music21 import converter
from music21 import clef
from music21 import duration
from music21 import meter
from music21 import tie

from emmsap import files
from emmsap import mysqlEM
from emmsap import updateDB

def jasonPieces():
    '''
    returns all of the pieces JS transcribed as paths.
    '''
    return [f for f in files.allFilesWithPath() if 'Stoessel' in f]

def chantillyPieces():
    return [f for f in jasonPieces() if '_Ch_' in f]

def modenaPieces():
    return [f for f in jasonPieces() if '_Mod_' in f]

def fixClefs(s):
    '''
    standardizes clefs such that soprano -> treble; alto -> treb8vb; tenor -> bass
    '''
    def replaceIt(c, replacementClass):
        for site in c.sites:
            site.replace(c, replacementClass())
        
    for c in s.recurse().getElementsByClass('Clef'):
        if 'AltoClef' in c.classes:
            replaceIt(c, clef.Treble8vbClef)
        elif 'SopranoClef' in c.classes:
            replaceIt(c, clef.TrebleClef)
        elif 'TenorClef' in c.classes:
            replaceIt(c, clef.BassClef)
        elif 'TrebleClef' in c.classes:
            pass
        elif 'BassClef' in c.classes:
            pass
        else:
            print(s.filePath, c)
        
def fixTS(s):
    '''
    Most pieces have no time signatures in the MusicXML.  They do have these
    FiguraeMensuris representations of original mensuration signs.  Where they
    represent a time signature, replace with that time signature.
    
    Note that these are guesses.  I don't have a copy of FiguraeMensuris.
    '''
    # Stoessel_Ch_041-Si_con_ci_gist.xml -- will be separate...
#     for ts in s.recurse().getElementsByClass('TimeSignature'):
#         print(ts)
#         ts.style.hideObjectOnPrint = False
    knownContent = {'«': '6/8', 'Ç': '6/8', '¶': '6/8',
                    'ø': '3/4', '¯': '3/4', 
                    'Ë': '9/8', 'ÿ': '9/8',
                    'ß': '4/4',
                    'Á': '2/4', 'ç': '2/4', 
                    '’': '3/2',
                    
                    # '‰' 3/2 in 4/4
                    
                    'Ø' : None, # '3/4' or '9/8'
                    'Ω': None, # '3/4',
                    'c': None, 'd': None, 'ä': None, 'ñ  d': None, 'ò': None,
                    '[': None, ']': None, 'D': None, 'ã': None,
                    'â': None, 'ê': None, 'ì ì': None, 
                    'm': None, '@': None, 'ó': None, 'å': None, 'õ': None,
                    'è': None, '¥': None, '‰': None, 'Â': None,
                    
                    }
    for te in s.recurse().getElementsByClass('TextExpression'):
        if te.fontFamily == 'FiguraeMensuris':
            replacementTS = knownContent[te.content]
            if 'Ch_025' in s.filePath:
                replacementTS = '6/4' # screwy...
            m = te.getContextByClass('Measure')
            if replacementTS is not None:
                m.insert(0, meter.TimeSignature(replacementTS))
            m.remove(te)
        elif te.content in ('[', ']'): # brackets around notation sings.
            m = te.getContextByClass('Measure')
            m.remove(te)
                     
def delHiddenContent(s):
    '''
    It will be easier simply to delete hidden content and then
    to recreate from overflowed notes later.  For instance, in 2/4 if there's
    a dotted half(sic), in one measure, then a hidden quarter and a non-hidden quarter,
    we will delete the hidden quarter now.  Then later we will make the dotted half into
    a half and put a quarter at the beginning of the next measure.
    
    Surprisingly, the makeMeasures routine will do this!
    '''
    totRemoved = 0
    for n in s.recurse():
        if n.style.hideObjectOnPrint is True:
            m = n.getContextByClass('Measure')
            if m:
                m.remove(n)
                totRemoved += 1
    
    #print(totRemoved)

def clearStemDirection(s):
    '''
    after changing clefs, stemdirections should be cleared.
    '''
    for n in s.recurse().notes:
        n.stemDirection = None


def removeLineBreaks(s):
    '''
    these are never right...
    '''
    for layout in s.recurse().getElementsByClass('LayoutBase'):
        layout.getContextByClass('Stream').remove(layout)


def fillEmptyMeasures(s):
    '''
    If there is an empty measure followed by some sort of double barline, it's a tie from
    the previous measure 99% of the time.  JS records differences in lengths of endings.
    '''
    for m in s.recurse().getElementsByClass('Measure'):
        if (m.rightBarline is None 
                or m.rightBarline.style not in ('double', 'final') 
                or len(m.flat.notesAndRests) > 0):
            continue
        prevM = m.previous('Measure')
        if not prevM:
            continue
        if len(prevM.flat.notes) != 1: # whole measure!
            continue
        prevMNote = prevM.flat.notes[0]
        newNote = copy.deepcopy(prevMNote)
        prevMNote.tie = tie.Tie('start')
        newNote.tie = tie.Tie('stop')
        m.insert(0, newNote)

def fixDotGroups(s):
    fixedDotGroups = 0
    for m in s.recurse().getElementsByClass('Measure'):
        nnotes = m.flat.notesAndRests
        if (len(nnotes) == 1 
                and nnotes[0].duration.dots == 1 
                and len(nnotes[0].articulations) == 1
                and 'Staccato' in nnotes[0].articulations[0].classes
                ):
            # meant to be a dotted dotted note
            nnotes[0].articulations = []
            nnotes[0].duration.dotGroups = (1,1)
            fixedDotGroups += 1
            
    if fixedDotGroups:
        pass
        #print("Fixed {} dot groups".format(fixedDotGroups))

def iterMeasureStacksBackwards(s):
    maxMeasureNum = len(s.parts[0].getElementsByClass('Measure'))
    for mNumber in range(maxMeasureNum - 1, 0, -1): # must go in reverse order since we will manipulate
        mStack = s.measure(mNumber, 
                         collect=['TimeSignature'], 
                         gatherSpanners=False, 
                         indicesNotNumbers=True)
        mStack.id = 'MeasureStack_{}'.format(mStack[-1][-1].number)
        yield mStack

def fixIncompatibleTimeSignatures(s):
    '''
    Fix time signatures with different lengths (such as 2/1 against 2/2 or 9/8 against 4/4)
    by making tuplets.
    '''
    for mStack in iterMeasureStacksBackwards(s):
        #print(mStack)
        tsSet = set()
        tsDict = {}
        for ts in mStack.recurse().getElementsByClass('TimeSignature'):
            tsQL = ts.barDuration.quarterLength
            tsSet.add(tsQL)
            tsDict[tsQL] = ts
        if len(tsSet) <= 1:
            continue
        
        #print(tsSet)
        minBarDuration = min(tsSet)
        minBarDurationTS = tsDict[minBarDuration]
        for p in mStack.parts:
            try:
                thisTS = p.recurse().getElementsByClass('TimeSignature')[0]
            except IndexError:
                continue
            
            thisTSBarDur = thisTS.barDuration.quarterLength
            if thisTSBarDur == minBarDuration:
                continue
            scaleAmount = minBarDuration / thisTSBarDur
            m = p.getElementsByClass('Measure')[0]
            if m.number == 23:
                pass
            if m.isFlat is False:
                print(mStack, " -- not flat! ")
                continue
            listNotes = list(m.notesAndRests)
            for i, n in enumerate(listNotes):
                nNewOffset = m.elementOffset(n) * scaleAmount
                m.remove(n)
                if scaleAmount in (0.5, 0.25, 0.125) or len(n.duration.dotGroups) > 1:    
                    if len(n.duration.dotGroups) > 1:
                        pass                    
                    n.duration.quarterLength *= scaleAmount
                else:
                    f = fractions.Fraction.from_float(1/scaleAmount).limit_denominator(1000)
                    t = duration.Tuplet(f.numerator, f.denominator)
                    if i == 0:
                        t.type = 'start'
                    elif i == len(listNotes) - 1:
                        t.type = 'stop'
                    
                    n.duration.appendTuplet(t)

                m.insert(nNewOffset, n)
            
            # remove TS if in measure
            if m.hasElementOfClass('TimeSignature'):
                m.timeSignature = copy.deepcopy(minBarDurationTS)
                
            #mStack.show('t')

def fixScrewyAccidentals(pp2):
    '''
    double flats are flats;  double sharps are sharps.
    '''
    for pObj in pp2.pitches:
        if pObj.alter > 1:
            pObj.accidental.alter = 1
        elif pObj.alter < -1:
            pObj.accidental.alter = -1
        
#-----------------
  
def fixAll():
#     continueIt = True
    for p in jasonPieces():
#         if 'Mod_62' in p:
#             continueIt = False
#         if continueIt:
#             continue
        fixOne(p, show=True)
        
def fixOne(p, *, show=False):    
    print(p)
    pShort = os.path.split(p)[-1]
    outdir = '/Users/cuthbert/desktop/StoesselOut/'
    pOut = outdir + pShort
    pp = converter.parse(p)
    #pp.show()
    fixDotGroups(pp)
    fixClefs(pp)
    fixTS(pp)
    fixIncompatibleTimeSignatures(pp)
    delHiddenContent(pp)
    clearStemDirection(pp)
    removeLineBreaks(pp)
    
    # this fixes a multitude of sins...
    pp2 = pp.makeNotation()
    #pp2.parts[2].measures(1, 8).show('t')
    fillEmptyMeasures(pp2)
    fixScrewyAccidentals(pp2)
    if show:
        print(pp2.write(fp=pOut))


def reindex():
    em = mysqlEM.EMMSAPMysql()
    for p in jasonPieces():
        pShort = os.path.split(p)[-1]
        pieceObj = em.pieceByFilename(pShort)
        if not pieceObj.id:
            print("***********", pShort)
            continue
        pieceObj.deletePiece(keepPieceEntry=True)
    updateDB.updateDatabase()

if __name__ == '__main__':
    #de_ce = chantillyPieces()[77] #  Stoessel_Ch_087-De_ce_que_foul_pense.xml # DONE!
    #fixOne(de_ce, show=True)
    #se_doit = chantillyPieces()[8] #  Stoessel_Ch_008-Se doit -- 9/8 vs 4/4 err.
    #fixOne(se_doit, show=True)

    #a_mon = chantillyPieces()[5] #  Stoessel_Ch_007-A mon
    #fixOne(a_mon, show=True)

    #je_ne = chantillyPieces()[22] #  Stoessel_Ch_029-Je ne puis avoir
    #fixOne(je_ne, show=True)


    #fixAll()
    reindex()