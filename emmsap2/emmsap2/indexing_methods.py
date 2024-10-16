def translate_diatonic_intervals_and_speed(inputStream, returnMeasures=False):
    '''
    Like music21's translateIntervalsAndSpeed but with diatonic distances.
    '''
    b = []
    measures = []

    previousRest = False
    previousTie = False
    previousQL = None
    previousDNN = 29
    for n in inputStream:
        if n.isNote:
            previousDNN = n.pitches[0].diatonicNoteNum
            break

    for n in inputStream:
        mNum = None
        if returnMeasures:
            mNum = n.measureNumber
        if n.isRest:
            if previousRest is True:
                continue
            else:
                previousRest = True
                b.append(' ')
                measures.append(mNum)
                continue
        else:
            previousRest = False
        if previousTie is True:
            if n.tie is None or n.tie.type == 'stop':
                previousTie = False
            continue
        elif n.tie is not None:
            previousTie = True
        ql = n.duration.quarterLength
        if previousQL is None or previousQL == ql:
            ascShift = 27 + 14  # = 41
        elif previousQL > ql:
            ascShift = 27 * 2 + 14
        else:
            ascShift = 14
        previousQL = ql
        pitchDifference = previousDNN - n.pitches[0].diatonicNoteNum
        if pitchDifference > 13:
            pitchDifference = 13
        elif pitchDifference < -13:
            pitchDifference = -13
        previousDNN = n.pitches[0].diatonicNoteNum
        newName = chr(32 + pitchDifference + ascShift)
        measures.append(mNum)
        b.append(newName)

    joined = ''.join(b)
    if returnMeasures is False:
        return joined
    else:
        return (joined, measures)
