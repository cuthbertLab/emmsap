from django.db import transaction

from emmsapPurePython.knownSkips import skipFilenames

from ..models import Piece, SkipGroup, SkipPiece


def main():
    for group in skipFilenames:
        do_one(group)


@transaction.atomic
def do_one(group):
    skipGroup = SkipGroup()
    skipGroup.save()

    num_pieces = 0
    for p_fn in group:
        p_fn = p_fn.replace(' ', '_')
        try:
            p = Piece.objects.get(filename=p_fn)
        except Piece.DoesNotExist:
            print(f'No piece by name {p_fn} for group {group}')
            continue
        skipPiece = SkipPiece(
            skip_group=skipGroup,
            piece=p,
        )
        skipPiece.save()
        num_pieces += 1
    if not num_pieces:
        skipGroup.delete()

