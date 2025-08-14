from pathlib import Path
from send2trash import send2trash

from .models import Piece
from .files import emmsapDir


def run(piece_id_or_fn: int|str):
    p: Piece
    if isinstance(piece_id_or_fn, str):
        p = Piece.objects.get(filename=piece_id_or_fn)
    else:
        p = Piece.objects.get(pk=piece_id_or_fn)

    fn: Path = p.filepath

    if fn.exists():
        send2trash(fn)
    p.delete()


def delete_missing_files():
    '''
    In case a file has been renamed/removed on another copy of EMMSAP, you might
    end up with phantom Piece objects with all their ratios etc.

    This deletes all Piece objects and their cascading parts
    if their file does not exist
    '''
    # little check.
    if not emmsapDir.exists():
        raise ValueError('Emmsap directory does not exist: would delete everything!')

    tot_deleted = 0
    for p in Piece.objects.all():
        if not p.filepath.exists():
            p.delete()
            tot_deleted += 1
    print(f'Deleted {tot_deleted} pieces.')

