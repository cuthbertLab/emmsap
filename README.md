# emmsap

EMMSAP: Electronic Medieval Music Score Archive Project
Copyright © 2013-26, Michael Scott Asato Cuthbert


(Access to this repository before 5 December 2024 was subject to the signing of an access agreement)

Data from 5 December 2024 onward released (under the BSD 3-clause license) but 
subject to and with the understanding that some encoding relies on the concept 
of scholarly Fair Use of in-copyright transcriptions, 
and therefore is limited to use for transformative and research purposes and not 
for performances or for republishing 
purposes or for any other usage which would interfere with the rights of 
(a) composers (they're long dead! whew) (b) editors and/or (c) publishers.

To put it colloquially -- if you are using EMMSAP to find out how often minor sevenths
are used in Italy vs. France, you're probably in the legal and licensing clear.  If you're using
EMMSAP to create a Braille-music study package of Machaut's motets, you're probably in the
licensing clear (again, not a lawyer; just what seems to be correct).  If, on the other hand,
you're using an EMMSAP edition of a song for your next concert because even though you've
found the same song in a modern edition for $2.99 but you'd prefer not to pay, you might not
be in the clear.  If you are republishing many scores that were edited by others 
you should definitely consult a lawyer.  That's not what EMMSAP is for.

The Code for EMMSAP (everything not in the xmldata) folder is released under the BSD 3-clause license
without (to the best of my knowledge) any Fair Use encumbrances.

The data and software are designed for teams that consist both of programmers and musicologists to use.
If your team has never worked with both large data models **and** music and need help from the 
"EMMSAP Team" (=Myke Cuthbert) to get your group set up with the project, please contact us, but 
expect to pay consulting rates
and (to cut down on your costs) already have someone on your side who has 
worked with computer music data before.  :-)

## Citation

for now please cite EMMSAP as:

Cuthbert, Michael Scott Asato, "A.I., Similarity, and Search in Medieval Music: 
New Methodologies and Source Identifications," All Souls Oxford Medieval Symposium, 5 December 2024.


## Setup

Install the root dependencies from `pyproject.toml` and the `emmsap2/requirements.txt` file.

```bash
uv sync
uv pip install -r emmsap2/requirements.txt
```

Create a file in your root directory called .emmsap_password with this format

    database=emmsap
    host=localhost
    username=username
    password=PASSWORD

Setup a Django database as with other Django systems.

```
CREATE USER 'username'@'%' IDENTIFIED BY 'PASSWORD';

GRANT ALL PRIVILEGES
ON emmsap.*
TO 'username'@'localhost'
WITH GRANT OPTION;
```

Run the initial migration:  `python manage.py migrate`

Create a "country" entry of id 1 Unspecified

Create a "composer" entry of id 1 Unspecified in Country 1

## Usage

Still complex.  Make a virtual environment for "emmsap2"

To index files in xmldata run:

```bash
python manage.py updateDB
```
This should take between 2 and 24 hours depending on the speed
of your computer.


## Searching similarities across pieces:

For basic similarity searches, run something like:

```bash
python manage.py updateDB --start 1 --end 100 min_threshold 8000
```
The threshold of 8000 is pretty good for separating out things that are very likely
quotations while missing very few.


For more sophisticated queries, start a Django shell

```bash
python manage.py shell
```
And then configure your SimilaritySearcher 

```python
from emmsap2.similarity_ratio import SimilaritySearcher
SimilaritySearcher(start_piece, end_piece + 1, min_ratio).run_pieces()
```

## Searching for Single Pieces

For the most part I've done searches for single pieces using an SQL editor
such as (on Mac) Sequel Ace.  Here are the queries I have found most useful:

### Searching intervals omitting unisons:

`SELECT p.id,p.filename, intv.part_id, intv.intervals, intv.intervals_no_unisons, tn.ts_ratio, tn.tn FROM emmsap2_intervals AS intv LEFT JOIN emmsap2_piece AS p ON intv.piece_id = p.id LEFT JOIN emmsap2_tinynotation AS tn ON p.id = tn.piece_id AND intv.part_id = tn.part_id WHERE intv.intervals_no_unisons REGEXP ''`

### Searching for a piece with intervals and text:

`SELECT * FROM emmsap2_piece LEFT JOIN emmsap2_text ON emmsap2_text.piece_id = emmsap2_piece.id LEFT JOIN emmsap2_intervals ON emmsap2_intervals.piece_id = emmsap2_piece.id WHERE text_reg REGEXP "^.{10,150}choisi" AND intervals_with_rests REGEXP "r12"`


## Directories

- `emmsap2` has the latest version of the data.  
- `emmsap_purePython` has an older version which you shouldn't use, but I haven't transferred all
  the files over yet.
