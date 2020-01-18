typeToTn = {
    'breve': '0',
    'whole': '1',
    'half': '2',
    'quarter': '4',
    'eighth': '8',
    '16th': '16',
    '32nd': '32',
    '64th': '64',
    '128th': '128',
    'longa': '00',  # probably not...
}  # zero and complex durations current do not work

verbose = True  # do not abbreviate tiny notation


def convertOne(n, lastTNType):
    if (n.isNote):
        nName = n.name
        nStep = n.step
        nAccidentalModifier = ""
        if (n.pitch.accidental is not None):
            nAccidentalModifier = n.pitch.accidental.modifier
        nOctave = n.octave
        if (nOctave <= 3):
            nName = (nStep * (4-nOctave)) + nAccidentalModifier
        elif (nOctave >= 5):
            nName = nStep.lower() + ("'" * (nOctave - 4)) + nAccidentalModifier
        else:  # octave 4
            nName = nName.lower()
    elif (n.isRest):
        nName = 'r'
    else:
        nName = 'c'  # chords, etc.
    if n.tie is not None and (n.tie.type == 'start' or n.tie.type == 'continue'):
        nName += '~'

    nType = n.duration.type
    nTNType = typeToTn[nType]
    nDots = '.' * n.duration.dots
    nTNType += nDots
    if (lastTNType == nTNType):
        if (verbose is False):
            nTNType = ""
    else:
        lastTNType = nTNType
    return (nName + nTNType, lastTNType)


def convert(pNotes):
    tnList = []
    lastTNType = None
    for n in pNotes:
        if n.duration.type == 'complex':
            for nSub in n.splitAtDurations():
                nName, lastTNType = convertOne(nSub, lastTNType)
                tnList.append(nName)
        elif n.duration.type == 'zero':
            continue
        else:
            nName, lastTNType = convertOne(n, lastTNType)
            tnList.append(nName)
    return " ".join(tnList)
