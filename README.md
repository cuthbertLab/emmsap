# emmsap

EMMSAP: Electronic Medieval Music Score Archive Project
Copyright (c) 2013-24, Michael Scott Asato Cuthbert

Access to this repository before 5 December 2024 was subject to the signing of an access agreement
(Please contact Michael Scott Asato Cuthbert (michael.asato.cuthbert@gmail.com) for more information).
Data is released (under the BSD 3-clause license) subject to the understanding that it will be 
used for transformative and research purposes and not for performances or for republishing purposes or for any other usage which would interfere with the rights of (a) composers (they're long dead! whew) (b) editors and/or (c) publishers.

To put it colloquially -- if you are using EMMSAP to find out how often minor sevenths
are used in Italy vs. France, you're probably in the legal and licensing clear.  If you're using
EMMSAP to create a Braille-music study package of Machaut's motets, you're probably in the
licensing clear (again, not a lawyer; just what seems to be correct).  If, on the other hand,
you're using an EMMSAP edition of a song for your next concert because even though you've
found the same song in a modern edition for $2.99 but you'd prefer not to pay, you might not
be in the clear.  If you are republishing many scores that were edited by others you should definitely consult a lawyer.  That's not what EMMSAP is for.

The data and software are released for programming/data-oriented teams to use.  If you have
never worked with large data models with music and need help from the "EMMSAP Team" (=Myke
Cuthbert) to get your group set up with the project, please expect to pay consulting rates
and to have someone on your side who has worked with computer music data before.  :-)

## Usage

Still complex.  Set up a Django database etc. then to index files in xmldata run:

```bash
python manage.py updateDB
```

Then to search, run:

```bash
python manage.py shell
```

And run 

```python
from emmsap2.similarity_ratio import SimilaritySearcher
SimilaritySearcher(start_piece, end_piece + 1, min_ratio).run_pieces()
```

`emmsap2` has the latest version of the data.  `emmsap_purePython` has an older version.  `emmsap_15` has experimental data for later 15th century music.

