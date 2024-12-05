# emmsap

EMMSAP: Electronic Medieval Music Score Archive Project
Copyright © 2013-24, Michael Scott Asato Cuthbert

Access to this repository before 5 December 2024 was subject to the signing of an access agreement
(Please contact Michael Scott Asato Cuthbert (michael.asato.cuthbert@gmail.com) for more information).

Data on 5 December 2024 is released (under the BSD 3-clause license) but subject to and with the 
understanding that some encoding relies on the concept of scholarly Fair Use of in-copyright transcriptions, 
and therefore is limited to use for transformative and research purposes and not for performances or for republishing 
purposes or for any other usage which would interfere with the rights of (a) composers (they're long dead! whew) (b) editors and/or (c) publishers.

To put it colloquially -- if you are using EMMSAP to find out how often minor sevenths
are used in Italy vs. France, you're probably in the legal and licensing clear.  If you're using
EMMSAP to create a Braille-music study package of Machaut's motets, you're probably in the
licensing clear (again, not a lawyer; just what seems to be correct).  If, on the other hand,
you're using an EMMSAP edition of a song for your next concert because even though you've
found the same song in a modern edition for $2.99 but you'd prefer not to pay, you might not
be in the clear.  If you are republishing many scores that were edited by others you should definitely consult a lawyer.  That's not what EMMSAP is for.

The Code for EMMSAP (everything not in the xmldata) folder is released under the BSD 3-clause license
without (to the best of my knowledge) any Fair Use encumberances.

The data and software are designed for teams that consist both of programmers and musicologists to use.
If your team has never worked with both large data models **and** music and need help from the "EMMSAP Team" (=Myke
Cuthbert) to get your group set up with the project, please contact us, but expect to pay consulting rates
and (to cut down on your costs) already have someone on your side who has worked with computer music data before.  :-)

## Citation

for now please cite EMMSAP as:

Cuthbert, Michael Scott Asato, "A.I., Similarity, and Search in Medieval Music: 
New Methodologies and Source Identifications," All Souls Oxford Medieval Symposium, 5 December 2024.


## Setup

Setup a Django database as with other Django systems.

Make the initial migration and migrate

Create a "country" entry of id 1 Unspecified

Create a "composer" entry of id 1 Unspecified in Country 1

## Usage

Still complex.  To index files in xmldata run:

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

## Directories

`emmsap2` has the latest version of the data.  `emmsap_purePython` has an older version.  `emmsap_15` has experimental data 
for later 15th century music (not yet licensed to work with this data).

