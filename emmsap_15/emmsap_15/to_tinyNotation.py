import music21


type_to_tn = {
    'breve': '0',
    'whole': '1',
    'half': '2',
    'quarter': '4',
    'eighth': '8',
    '16th': '16',
    '32nd': '32',
    '64th': '64',
    '128th': '128',
    '256th': '256',
    '512th': '512',
    '1024th': '1024',
    'longa': '00',  # conversion from MEI
    'maxima': '000',  # found in some Fauvel pieces
}  # zero and complex durations current do not work

verbose = True  # do not abbreviate tiny notation


def convert_one_el(n, last_tn_type):
    if isinstance(n, music21.note.Note):
        note_name = n.name
        note_step = n.step
        accidental_modifier = ''
        if n.pitch.accidental is not None:
            accidental_modifier = n.pitch.accidental.modifier
        note_octave = n.octave
        if note_octave <= 3:
            note_name = (note_step * (4 - note_octave)) + accidental_modifier
        elif note_octave >= 5:
            note_name = note_step.lower() + ("'" * (note_octave - 4)) + accidental_modifier
        else:  # octave 4
            note_name = note_name.lower() + accidental_modifier
    elif isinstance(n, music21.note.Rest):
        note_name = 'r'
    else:
        note_name = 'c'  # chords, etc.
    if n.tie is not None and (n.tie.type == 'start' or n.tie.type == 'continue'):
        note_name += '~'

    dur_type = n.duration.type
    if dur_type == 'inexpressible':
        dur_type = 'maxima'  # as long as we can get.

    tn_dur_type = type_to_tn[dur_type]
    nDots = '.' * n.duration.dots
    tn_dur_type += nDots
    if last_tn_type == tn_dur_type:
        if not verbose:
            tn_dur_type = ''
    else:
        last_tn_type = tn_dur_type
    return (note_name + tn_dur_type, last_tn_type)


def convert(notes_and_rests):
    tn_list = []
    last_tn_type = None
    for n in notes_and_rests:
        # if not n.duration.linked:
        #     n.duration = music21.duration.Duration(n.duration.type, n.duration.dots)

        # TODO: inexpressible
        if n.duration.type == 'complex':
            for component_note in n.splitAtDurations():
                if component_note.duration.type == 'complex':
                    # https://github.com/cuthbertLab/music21/issues/1324
                    continue
                note_name, last_tn_type = convert_one_el(component_note, last_tn_type)
                tn_list.append(note_name)
        elif n.duration.type == 'zero':
            continue
        else:
            note_name, last_tn_type = convert_one_el(n, last_tn_type)
            tn_list.append(note_name)
    return ' '.join(tn_list)
