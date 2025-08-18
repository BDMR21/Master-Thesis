# \# README — Extraction \& Meta-Analysis Package

# 

# This folder contains the schema, templates, scripts, and docs to reproduce the NIDS meta-analysis.

# 

# \## Quick start

# 1\. Put PDFs in `./pdfs/`.

# 2\. Extract:

```bash

# &nbsp;  python extract\_nids\_meta.py --pdf\_dir ./pdfs --out\_csv extracted.csv --schema data\_extraction\_schema.json
```

3\. Validate \& normalize:

```bash

python validate\_and\_harmonize.py --in\_csv extracted.csv --out\_csv clean.csv --out\_jsonl clean.jsonl

```

4\. Meta-analyze (example: macro-F1 by dataset):

```bash 

python meta\_analyze.py --in clean.csv --metric performance.f1\_macro --group datasets --out meta\_summary.csv --json\_out meta\_summary.json

```

5\. Forest plot:

```bash

python forest\_plot.py --summary\_json meta\_summary.json --out\_png forest.png

```



## Notes



* The extractor is heuristic; manually complete IDs, titles, and missing values.



* Use the CODEBOOK to keep values consistent with the schema.



* Dependencies: PyPDF2, matplotlib.



