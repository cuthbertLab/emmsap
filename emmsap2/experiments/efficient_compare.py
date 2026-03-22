'''
Try to compare segments with higher accuracy.
'''
# from heap_class import Heap
from heapq import heappush, heappop
from collections import defaultdict, deque

from music21.search.base import translateDiatonicStreamToString

from ..models import Piece

segment_length = 32
segment_separation = 4
max_changes = 99

# to pad out to a multiple of 4 and up to 32, we use
# different characters so they count as misalignments
seg_1_pad = '*'
seg_2_pad = '.'

def pad_segment(seg: str, pad_ch: str = 'x') -> str:
    '''
    Return a new segment, where if it is shorter than segment_length
    it is padded with pad_ch to segment_length.
    
    Then if is is longer than segment_length but not a multiple of segment_separation,
    also pad that way.
    '''
    if len(seg) < segment_length:
        return seg + pad_ch * (segment_length - len(seg))
    elif len(seg) % segment_separation:
        return seg + pad_ch * (segment_separation - len(seg) % segment_separation)
    else:
        return seg

def main():
    # get two random pieces
    p1 = Piece.objects.get(pk=100)
    p2 = Piece.objects.get(pk=200)
    print(p1)
    print(p2)
    p1_seg = pad_segment(translateDiatonicStreamToString(p1.stream().recurse().notesAndRests), seg_1_pad)
    p2_seg = pad_segment(translateDiatonicStreamToString(p2.stream().recurse().notesAndRests), seg_2_pad)
    print(p1_seg)
    print(p2_seg)
    print(run_segs1(p1_seg, p2_seg))

def run_segs1(s1: str, s2: str) -> int:
    # KISS -- solve a simpler problem first.
    # first time, just do each 32 separately, and just compare 0-32 against 0-32, etc.

    # visited can also be a 2-dim numpy binary array or something else that is faster than hash lookup
    visited = set()
    same_dist = defaultdict(deque)
    # note: this can also be a list of deques of length
    # (segment_length * 2), since switching lists is much faster than dict indexing.
    cur_position = segment_length * 2
    same_dist[cur_position].append((0,0,0))
    visited.add((0,0))

    while True:
        if same_dist[cur_position]:
            print(cur_position, same_dist[cur_position])
            num_mistakes, p1, p2 = same_dist[cur_position].popleft()
            equal = 1 if (s1[p1] == s2[p2]) else 0  # or int(bool) whatever
            if not equal:
                num_mistakes += 1

            if p1 == len(s1) - 1 and p2 == len(s2) - 1:
                return num_mistakes
            if not equal and num_mistakes == max_changes:
                continue

            if (p1+1, p2+1) not in visited:
                # advance both -- should always not be in visited
                visited.add((p1+1, p2+1))
                same_dist[cur_position - 1 - equal].append((num_mistakes, p1+1, p2+1))
            if not equal and p2 <= len(s2) - 1 and (p1, p2+1) not in visited:
                visited.add((p1, p2+1))
                same_dist[cur_position - equal].append((num_mistakes, p1, p2+1))
            if not equal and p2 <= len(s2) - 1 and (p1+1, p2) not in visited:
                visited.add((p1+1, p2))
                same_dist[cur_position - equal].append((num_mistakes, p1+1, p2))
            cur_position = cur_position - 1 - equal
        else:
            print('hi')
            while not same_dist[cur_position]:
                print(cur_position, same_dist[cur_position])
                cur_position += 1
                if cur_position > (segment_length * 2):
                    return max_changes
    return max_changes

def run_segs1_heap(s1: str, s2: str) -> int:
    # KISS -- solve a simpler problem first.
    # first time, just do each 32 separately, and just compare 0-32 against 0-32, etc.
    visited = set()
    heap = []
    while heap:
        print(heap)
        mistakes, p1, p2 = heappop(heap)
        if mistakes == max_changes:
            return mistakes
        if p1 == segment_length and p2 == segment_length:
            return mistakes

        if s1[p1] == s2[p2]:
            visited.add((p1+1, p2+1))
            heappush(heap, (mistakes, p1+1, p2+1))
        else:
            if (p1+1, p2) not in visited:
                visited.add((p1+1, p2))
                heappush(heap, (mistakes + 1, p1+1, p2))
            if (p1, p2+1) not in visited:
                visited.add((p1, p2+1))
                heappush(heap, (mistakes + 1, p1, p2+1))
            if (p1+1, p2+1) not in visited:
                visited.add((p1+1, p2+1))
                heappush(heap, (mistakes + 1, p1+1, p2+1))
    return max_changes

if __name__ == '__main__':
    main()

