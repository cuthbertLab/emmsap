'''
Convert all files to midi for similarity/quotation searching by Vladimir Viro.
'''
from music21 import converter
from emmsap import files
import os


def mainFunc():
    outDir = '/Users/cuthbert/Desktop/EMMSAP_Midi'
    emdir = files.emmsapDir
    print(emdir)
    for f in files.allFiles():
        fp = os.path.join(emdir, f)
        fMid = f[:-4] + '.mid'

        outfp = os.path.join(outDir, fMid)
        try:
            sIn = converter.parse(fp)
            sIn.write('midi', outfp)
        except:
            print("conversion failed for %s" % fp)


if __name__ == '__main__':
    mainFunc()
