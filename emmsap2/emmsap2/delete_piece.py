from pathlib import Path
from send2trash import send2trash

from .models import Piece


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
    

