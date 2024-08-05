# emmsap
EMMSAP: Electronic Medieval Music Score Archive Project
Copyright (c) 2013-24, Michael Scott Asato Cuthbert

Access to this repository is subject to the signing of an access agreement.  
Please contact Michael Scott Asato Cuthbert (michael.asato.cuthbert@gmail.com) for more information.

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

