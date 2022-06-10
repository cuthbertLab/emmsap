from pathlib import Path

from .models import Piece


def run(piece_id_or_fn: int|str, new_name: str|Path):
    p: Piece
    if isinstance(piece_id_or_fn, str):
        p = Piece.objects.get(filename__startswith=piece_id_or_fn)
    else:
        p = Piece.objects.get(pk=piece_id_or_fn)

    fn: Path = p.filepath

    new_path = Path(new_name)
    if not new_path.is_absolute():
        new_path = fn.parent / new_path
        if not new_path.suffix:
            new_path = new_path.with_suffix(fn.suffix)

    if fn.exists():
        fn.rename(new_path)
        p.filename = new_path.name
        p.save()
    else:
        raise FileNotFoundError(f'No file named {fn}')
