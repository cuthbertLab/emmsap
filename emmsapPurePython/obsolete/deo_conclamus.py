# find a possible arrangment for the tenor O Excellent for Deo Gracias Conclamemus

from music21 import converter, metadata
c = converter.parse('/Users/cuthbert/Desktop/Deo Gracias Conclamemus.xml')
# Tenor O Excellent
#t = converter.parse('tinynotation: 3/4 D2. F#8 G4 A4 F#8 E2. D4 A A G F# E D2. d2. B8 d c4 B A2.~ A2. G4 F E G4 A4 r4').makeMeasures()
# Triplum ending...
t = converter.parse('tinynotation: 6/8 r4. c8 d4 e4. e4 g8 a f g a f e d e4 d c8 d2.~ d2.').makeMeasures()
t.priority = -100
tLength = len(t.getElementsByClass('Measure'))
print(tLength)

missingTenor = True


def consScore(chordObject):
    if len(chordObject) == 1:
        return 0
    elif chordObject.isConsonant():
        consScore = 0.5 * len(chordObject)
    elif missingTenor and len(chordObject) == 2 and chordObject.intervalVector in [[0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]]:
        consScore = 0.2
    elif len(chordObject) == 2:
        consScore = -1.0
    else:
        consScore = -0.5

    consScore *= chordObject.beatStrength
    return consScore

#for j in [8, 32, 56,  59, 66, 90]:
#    i = j - 7
for i in range(0, len(c.parts[0].getElementsByClass('Measure')) - tLength + 1):
    excerpt = c.measures(i + 1, i + tLength)
    excerpt.insert(0, t)
    excChord = excerpt.chordify()
    
    totalConsonanceScore = 0.0
    for chordObject in excChord.recurse():
        if 'Chord' not in chordObject.classes:
            continue
        totalConsonanceScore += consScore(chordObject)
    if totalConsonanceScore >= 6:
        excerpt.metadata = metadata.Metadata()
        excerpt.metadata.movementName = str(i+1) + " : " + str(totalConsonanceScore)

        print ("***********", i+1, totalConsonanceScore)
        #if totalConsonanceScore > 8:
        excerpt.show()
    else:
        print (i+1, totalConsonanceScore)
        #excerpt.show()