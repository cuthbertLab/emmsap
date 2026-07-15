---
name: reindex-text
description: Re-index the sung text of a Piece that already exists in the emmsap database. Use when a musicxml/mxl file was updated or re-imported and its Text row is stale, or the user says "reindex the text(s) from piece <id>", "re-run text indexing for <piece>". The normal index_texts.main() only touches pieces with NO text, so an existing Piece must have its Text row deleted and rebuilt. Runs against the live DB via Django shell.
---

# reindex-text — rebuild the Text row for an existing Piece

`emmsap2.index_texts.main()` **skips any piece that already has a Text**
(`Piece.objects.exclude(text__isnull=False)`). So `updateDB` will not refresh a
piece whose file changed. To reindex, delete the stale `Text` row and re-run the
per-piece logic.

## Model facts (as of this writing — verify if models.py changed)

- `Text` has a **OneToOneField** to `Piece` (`on_delete=CASCADE`), fields:
  `language`, `text`, `text_reg`, `text_no_space`.
- Reusable functions live in `emmsap2/index_texts.py`:
  - `get_text_from_score(sc)` — assembles lyrics across parts, adding a later
    part's text only when it's <0.8 Levenshtein-similar to what's already there.
  - `regularize_text(text_in, language)` → `(text_reg, text_no_space)`.
  - module globals `ld` (LanguageDetector) and `mistakes` (filename→language overrides).
- Piece 3758 = `Krakow_2464_10_Celebris_dies_colitur.mxl` is a good smoke-test id.

## Procedure

Run with `uv run python manage.py shell -c "..."` from the repo root. Replace
`PK` with the piece id (or look it up by filename with
`Piece.objects.get(filename=...)`).

```python
from emmsap2.models import Piece, Text
from emmsap2 import index_texts as it

p = Piece.objects.get(pk=PK)

# show the old row so the change is auditable
old = Text.objects.filter(piece=p).first()
print('OLD language:', old.language if old else None)
print('OLD text_reg:', repr((old.text_reg or '')[:200]) if old else None)

# delete the stale Text and rebuild from the current file on disk
Text.objects.filter(piece=p).delete()

sc = p.stream()
piece_text = it.get_text_from_score(sc)
if len(piece_text) < 5:
    language, text_reg, text_no_space = 'na', '', ''
else:
    language = it.ld.mostLikelyLanguage(piece_text)
    language = it.mistakes.get(p.filename, language)   # known-mistake overrides
    text_reg, text_no_space = it.regularize_text(piece_text, language)

Text(piece=p, language=language, text=piece_text,
     text_reg=text_reg, text_no_space=text_no_space).save()

print('NEW language:', language)
print('NEW text_reg:', repr(text_reg[:300]))
```

## Notes

- This mirrors `index_texts.main()` exactly except (1) it deletes first so an
  existing piece is rebuilt, and (2) it keys `mistakes` by `p.filename` (a str),
  not the Piece object — `main()` passes the Piece, which never matches the
  string keys, so keying by filename here is the corrected behavior.
- Always print OLD vs NEW so the user can confirm the reindex actually changed
  something (e.g. extra voices' lyrics now included).
- To reindex several pieces, loop over the ids; each is independent.
- This only touches the `Text` table. If tinyNotation / segment / ratio indexes
  also depend on the changed file, those are separate re-runs
  (`index_tinyNotation`, `index_segments`, `index_ratios`).
