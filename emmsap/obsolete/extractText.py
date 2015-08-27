'''
Extract passages from a Stream that contain a given text
'''
from emmsap import files
from music21 import converter
#from music21 import text
from music21 import stream
from music21 import metadata
import os

def searchOne(filename, allStream, textSearch):
    c = converter.parse(os.path.join(files.emmsapDir, filename))
    foundTextMeasure = None
    for partNum in range(len(c.parts)):
        c1 = c.parts[partNum]
        #allLyrics = text.assembleLyrics(c1)
        #if 'qui sedes' not in allLyrics.lower():
        #    pass
        #else:
        c1flatNotes = c1.flat.notes
        c1NotesWithLyrics = []
        for n in c1flatNotes:
            if n.lyric is not None:
                c1NotesWithLyrics.append(n)
        lenNotes = len(c1NotesWithLyrics)
        for i in range(0, lenNotes - len(textSearch)):
            continueIt = True
            for j in range(len(textSearch)):
                if c1NotesWithLyrics[j+i].lyric.lower() != textSearch[j]:
                    #print c1NotesWithLyrics[j+i].lyric
                    continueIt = False
                    break
            if continueIt is True:
                foundTextMeasure = c1NotesWithLyrics[i].measureNumber
                break
        if foundTextMeasure is not None:
            print(fn)
            print(foundTextMeasure)
            foundIt = c.measures(foundTextMeasure, foundTextMeasure + 8)
            m = metadata.Metadata()
            m.title = filename
            foundIt.insert(0, m)
            allStream.insert(0, foundIt)
            foundIt.show('musicxml.png')
            break # gives better chance to find lyrics in all parts

    #if foundTextMeasure is None:
    #    c.measures(1,40).show()
#textSearch = ['qui','se','des']
#textSearch = ['da','mus']
textSearch = ['lo','cu','tus']  # grottaferrata 216

allStream = stream.Opus()
for i,fn in enumerate(files.allFiles()):
    if 'credo' not in fn.lower() and 'patrem' not in fn.lower():
        print("Skipping %s" % fn)
    else:
        print(fn)
        try:
            searchOne(fn, allStream, textSearch)
        except:
            print("----search failed")
#allStream.show()