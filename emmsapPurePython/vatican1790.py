'''
At the bottom of f.1v of Vatican 1790, there is a line of music that should be
identifiable based on its characteristics, but normal searches do not work on it.
'''
from more_itertools import windowed
from music21 import converter
from music21 import interval
from music21 import stream
from emmsap import files


def main():
    p = converter.parse('tinyNotation: 6/8 G4. G8 F8 G8 A4. A8 G4 G8 F4 E8 D4 G4. E4.')
    s = stream.Score()
    s.filePath = 'tinyNotation'
    s.append(p)
    check_for_vatican_1970(s)

    for i, s in enumerate(files.FileIterator()):
        if i % 25 == 0:
            print(i, s.filePath)
        try:
            check_for_vatican_1970(s)
        except Exception as e:
            print(s.filePath, e)


def check_for_vatican_1970(s):
    highestDnn, p = check_for_opening_intervals(s)
    if not highestDnn:
        return
    if not check_opening_for_lower_dnn(highestDnn, p):
        return

    print('***', s.filePath)


def check_for_opening_intervals(s):
    '''
    At or very close to the beginning of the piece are four notes
    that go -222, with the last note significantly longer than any of the previous
    if this is not the case, then return False.
    '''
    for p in s.parts:
        start_notes = p.flat.getElementsByClass('Note')[:8]
        if len(start_notes) < 4:
            continue
        for notes in windowed(start_notes, 4):
            longestNote = max(notes, key=lambda n: n.duration.quarterLength)
            if longestNote is not notes[-1]:
                continue
            i1 = interval.Interval(notes[0], notes[1])
            if i1.generic.directed != -2:
                continue
            i2 = interval.Interval(notes[1], notes[2])
            if i2.generic.directed != 2:
                continue
            i3 = interval.Interval(notes[2], notes[3])
            if i3.generic.directed != 2:
                continue
            return longestNote.pitch.diatonicNoteNum, p

    return 0, None


def check_opening_for_lower_dnn(highestDnn, p):
    notes = list(p.flat.getElementsByClass('Note'))
    if len(notes) < 9:
        return False
    for i, n in enumerate(notes):
        if i < 8:
            continue
        if i > 42:
            break
        if n.pitch.diatonicNoteNum >= highestDnn:
            return False
    return True


if __name__ == '__main__':
    main()
