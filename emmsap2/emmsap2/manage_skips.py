from .models import Piece, SkipGroup, SkipPiece

def new_pair(p_id_1: int, p_id_2: int, reason: str = ''):
    p1 = Piece.objects.get(pk=p_id_1)
    p2 = Piece.objects.get(pk=p_id_2)

    sg = SkipGroup()
    if reason:
        sg.reason = reason
    sg.save()
    sp1 = SkipPiece(piece=p1, skip_group=sg)
    sp1.save()
    sp2 = SkipPiece(piece=p2, skip_group=sg)
    sp2.save()
