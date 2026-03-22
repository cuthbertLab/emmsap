# find all cases of parallel unisons between duplum and tenor in the
# Montpellier/Bamberg repertory.
from music21 import chord

from emmsap2.models import Piece


def run():
    montpellier = Piece.objects.filter(filename__startswith='mo_')
    for p in montpellier:
        most, most_measure = run_one(p)
        if most >= 2:
            print(p.filename, most, f'm. {most_measure}')


def run_one(p: Piece):
    sc = p.stream()
    if len(sc.parts) < 2:
        return 0, 0
    while len(sc.parts) > 2:
        sc.remove(sc.parts[0])
    chordified = sc.chordify(addPartIdAsGroup=True)
    # chordified.show()
    current_in_row = -1  # how many parallel unisons have been seen at this point?
    current_measure = 0
    most_in_row = 0  # most in piece.
    most_measure = 0
    for ch in chordified[chord.Chord]:
        if len(ch.pitches) == 1 and len(ch.pitches[0].groups) == 2:
            # print(ch, ch.measureNumber)
            current_in_row += 1
            current_measure = ch.measureNumber
        else:
            current_in_row = -1

        if current_in_row > most_in_row:
            most_in_row = current_in_row
            most_measure = current_measure
    return max(most_in_row, 0), most_measure


if __name__ == '__main__':
    run()
