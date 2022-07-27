import unicodedata
import re
import string

try:
    from Levenshtein import ratio as lvRatio
except ImportError as ie:
    raise ImportError(
        'No Levenshtein C program found -- will be much slower; \n'
          + 'run pip3 install python-Levenshtein') from ie

from music21 import text

from .models import Piece, Text


ld = text.LanguageDetector()

# noinspection SpellCheckingInspection
mistakes = {
    'PMFC_01_Tournai_6-Ite_Missa_Est.xml': 'la',
    'Ascoli_Piceno_Mater_Digna_Dei_Lux.xml': 'la',
    'Marchi_Notation_16-Virtute_sacquista_cum_grande_faticha.xml': 'la',
    'PMFC_01_Barcelona_1-Kyrie.xml': 'la',  # Kyrie should be gr...
    'PMFC_01_Tournai_1-Kyrie.xml': 'la',
    'Machaut_R01-Doulz_viaire_gracieus.xml': 'fr',
}


def main():
    all_texts = ''
    i = 0
    for p in Piece.objects.exclude(text__isnull=False):
        i += 1
        sc = p.stream()
        piece_text = get_text_from_score(sc)
        if len(piece_text) < 5:
            print(f'No text in {p}')
            language = 'na'
            text_reg = ''
            text_no_space = ''
        else:
            language = ld.mostLikelyLanguage(piece_text)
            language = mistakes.get(p, language)  # deal with known mistakes.
            text_reg, text_no_space = regularize_text(piece_text, language)

        all_texts += '--------------------\n'
        all_texts += '--- ' + p.filename + ' ---\n'
        all_texts += text_reg + '\n\n'

        t_obj = Text(
            piece=p,
            language=language,
            text=piece_text,
            text_reg=text_reg,
            text_no_space=text_no_space,
        )
        t_obj.save()

    print(all_texts)
    print(f'{i} text(s) added.')


def get_text_from_score(sc):
    all_texts = ''
    for p in sc.parts:
        this_text = text.assembleAllLyrics(p)
        if len(this_text) < 10:
            continue
        elif not all_texts:
            all_texts = this_text
        else:
            # if the second part has a text that is substantially
            # different from previous parts, then add it.
            r = lvRatio(all_texts, this_text)
            if r < 0.8:
                all_texts += '\n' + this_text
    all_texts = all_texts.strip()
    return all_texts


def regularize_text(text_in: str, language: str) -> tuple[str, str]:
    text_reg = re.sub('v', 'u', text_in.lower())
    text_reg = re.sub('j', 'i', text_reg)
    text_reg = re.sub('y', 'i', text_reg)
    if language == 'la':
        text_reg = re.sub('ae', 'e', text_reg)
        text_reg = re.sub('æ', 'e', text_reg)
        text_reg = re.sub('œ', 'e', text_reg)
    text_reg = re.sub(r'[#}{~/.:=;\-«»,*?\"!\'\[\]<>()\d_&$|]',
                      '',
                      text_reg)
    for punctuation_mark in string.punctuation:
        text_reg = text_reg.replace(punctuation_mark, '')  # partly redundant with above
    text_reg = text_reg.replace('…', '')
    text_reg = text_reg.replace('\n', ' ')
    text_reg = re.sub(r'(\s)\s+', r'\g<1>', text_reg)
    text_reg = unicodedata.normalize('NFKD', text_reg)
    text_reg = text_reg.encode('ascii', 'ignore').decode('UTF-8')
    text_reg = text_reg.strip()

    text_no_space = re.sub(r'\W+', '', text_reg)
    return (text_reg, text_no_space)
