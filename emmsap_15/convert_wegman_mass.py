# from send2trash import send2trash
from pathlib import Path
import shutil
import re

from music21 import *

WEGMAN = Path('/Users/Cuthbert/iCloud/EMMSAP/Wegman Masses Clean/')

def main():
    wegman_base_string = str(WEGMAN)
    xml_out = Path('/Users/Cuthbert') / 'Git' / 'emmsap' / 'emmsap_15' / 'xml15data'
    failures_out = xml_out.parent / 'wegman_not_convert'
    for s in sorted(WEGMAN.glob('**/*.nwc')):
        mine = str(s)[len(wegman_base_string):]
        mine = mine.replace('.nwc', '')
        mine = re.sub(r'\W', '_', mine)
        mine = mine[1:]
        p_out = Path(str(xml_out) + '/' + mine + '.musicxml')
        if p_out.exists():
            continue

        try:
            pp = converter.parse(mine)
        except Exception:
            try:
                pp = converter.parse(s.with_suffix('.mid'))
            except Exception:
                try:
                    pp = converter.parse(s.with_suffix('nwctxt'))
                except Exception:
                    print(f'Failure: {mine}')
                    shutil.copy2(s, failures_out / (mine + '.nwc'))
                    continue
        pp.write('musicxml', fp=p_out)
        print(p_out)
        # send2trash(s)

if __name__ == '__main__':
    main()
