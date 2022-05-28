from music21 import converter
from emmsap import files
import os

# last run July 31, 2013 -- no matches (PMFC 12_11a / PMFC 23.50 / Credo Pellisson )
def findIncipitWroclaw():
    #tn = 'tinynotation:6/8 g2. a4. g4 f8'### Wroclaw 1955 Patrem (or 2/4 g2 a8 g4 f8)
    for fn in files.allFiles():
        fn2 = fn.lower()
        if 'credo' not in fn2 and 'patrem' not in fn2:
            continue
        fullFn = files.emmsapDir + os.sep + fn
        s = converter.parse(fullFn)
        #ts = s.flat.getElementsByClass('TimeSignature')[0]
        #if ts.ratioString != '2/4' and ts.ratioString != '6/8':  # tougher...
        #    pass
        for i,p in enumerate(s.parts):
            try:
                if p.flat.notes[0].name == 'G' and p.flat.notes[1].name == 'A':
                    print(fn,i)
            except:
                pass
        
if __name__ == '__main__':
    findIncipitWroclaw()
